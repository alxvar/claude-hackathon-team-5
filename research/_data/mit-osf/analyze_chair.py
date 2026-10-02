# Re-analysis of the MIT AI Negotiation Competition, final round, chair (single-price) game.
# Source data: https://osf.io/yr9qv/overview?view_only=dafe4cc009fe4bffb0de2ed08d60334b
#   data/outcomes/round2_chair_wide_outcomes_deid.xlsx  (~100 MB)
#   data/prompts/round2_scored_deid.xlsx
# Run: uv run --with pandas --with openpyxl --with pyarrow --with statsmodels python analyze_chair.py
# Produces: chair_agent_ranking.csv, chair_offer_parse.parquet, and prints the tables used in 01-evidence.md §1b.
import ast, re, os
import numpy as np, pandas as pd, statsmodels.formula.api as smf

D = os.path.dirname(os.path.abspath(__file__))
pq = f"{D}/round2_chair_wide.parquet"
df = pd.read_parquet(pq) if os.path.exists(pq) else pd.read_excel(f"{D}/round2_chair_wide_outcomes_deid.xlsx")

# 1) Agent ranking: value claimed (price - BATNA; 0 if no deal), both roles averaged, self-play excluded.
rows = []
for s, o in ((1, 2), (2, 1)):
    rows.append(pd.DataFrame({"agent": df[f"prompt_name_{s}"] + "|" + df[f"name_deid_{s}"], "role": df[f"role_{s}"],
                              "vc": df[f"value_claimed_{s}"], "deal": df.deal_reached,
                              "self": df[f"name_deid_{s}"] == df[f"name_deid_{o}"]}))
L = pd.concat(rows); L = L[~L["self"]]
g = L.groupby(["agent", "role"]).agg(vc=("vc", "mean"), deal=("deal", "mean"), n=("vc", "size")).unstack("role")
g["vc_avg"] = (g[("vc", "buyer")] + g[("vc", "seller")]) / 2
g["deal_avg"] = (g[("deal", "buyer")] + g[("deal", "seller")]) / 2
g = g.sort_values("vc_avg", ascending=False)
g.columns = ["_".join(c) if isinstance(c, tuple) else c for c in g.columns]
g.to_csv(f"{D}/chair_agent_ranking.csv")
print("baseline buyer/seller vc:", L[L.role == "buyer"].vc.mean(), L[L.role == "seller"].vc.mean(), "deal:", L.deal.mean())
print(g.head(10)[["vc_avg_", "deal_avg_"]].round(2))

# 2) Offer parsing: last $ amount per message, excluding reference prices ($40 buyback, $200 original, $120 when 'store').
amt = re.compile(r"\$\s?(\d{1,4}(?:\.\d+)?)")
def parse(conv):
    msgs = ast.literal_eval(conv); seq = {"Seller": [], "Buyer": []}; first = None
    for m in msgs:
        mm = re.match(r"\s*(Seller|Buyer)\s*:", m)
        if not mm: continue
        if re.search(r"\n\s*1\.\s*(Agree|Disagree|Somewhat|Neither|Strongly)", m): break  # post-negotiation survey
        sp = mm.group(1)
        vals = [float(v) for v in amt.findall(m)]
        vals = [v for v in vals if v not in (40.0, 200.0) and not (v == 120.0 and "store" in m.lower()) and 0 < v < 400]
        if vals:
            seq[sp].append(vals[-1]); first = first or sp
        if "[DEAL REACHED]" in m: break
    return seq, first
out = []
for _, r in df.iterrows():
    seq, first = parse(r.conversation)
    for s in (1, 2):
        role = r[f"role_{s}"]; sp = "Seller" if role == "seller" else "Buyer"
        x = [v for j, v in enumerate(seq[sp]) if j == 0 or v != seq[sp][j - 1]]
        steps = [(a - b) if role == "seller" else (b - a) for a, b in zip(x, x[1:])]
        pos = [v for v in steps if v > 0]
        out.append(dict(agent=r[f"prompt_name_{s}"], role=role, vc=r[f"value_claimed_{s}"], deal=r.deal_reached,
                        open=x[0] if x else np.nan, nmoves=len(pos), mean_step=np.mean(pos) if pos else np.nan,
                        moved_first=(first == sp), noffers=len(x), selfplay=r.name_deid_1 == r.name_deid_2))
o = pd.DataFrame(out); o = o[~o.selfplay]; o.to_parquet(f"{D}/chair_offer_parse.parquet")

# 3) Step-size effect controlling for opening anchor (OLS, SE clustered by agent).
for role in ("seller", "buyer"):
    x = o[(o.role == role) & (o.nmoves > 0)]
    m = smf.ols("vc ~ open + mean_step + nmoves", data=x).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x.agent)[0]})
    print(role, m.params.round(3).to_dict(), m.pvalues.round(4).to_dict())
    z = o[(o.role == role) & (o.noffers > 0)]
    print(" never conceded:", z[z.nmoves == 0][["vc", "deal"]].mean().round(2).to_dict(), "| first mover:",
          z.groupby("moved_first")[["vc", "deal"]].mean().round(2).to_dict())
