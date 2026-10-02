---
type: research
entity: [people]
status: active
updated: 2026-10-01
source: https://causaprima.ai/
---

# 05 — The sponsor: Causa Prima (and what it implies for the tournament)

_Scraped 2026-10-01: causaprima.ai (home, manifesto, FAQ), jobs.ashbyhq.com/causaprima, the `causa-prima-ai` GitHub org, organizers' LinkedIn posts, press on the funding round._

## Bottom line

**There is no public documentation of their negotiation protocol.** Their only open-source work (GitHub `causa-prima-ai/scribo*`) is Scribo, an e-invoicing generator unrelated to negotiation. We only learn the real rules on Friday at 18:45. What we *can* read is **how they think**, from two engineering job posts, and that likely shaped the challenge.

## The company

- *"The agent-to-agent network for finance teams"*: agents on the buyer side and the supplier side negotiate **early-payment discounts**, resolve invoice disputes and approve invoices across companies.
- **Founders:**
  - CEO Maex Ament: *"Invented dynamic discounting. Built Taulia (now part of SAP), moving $50B across 5M suppliers."*
  - COO Henrik Gebbing (Finoa).
  - CTO Philip Stanislaus (600+ security audits, Oak Security).
- **Funding:** pre-seed of €8.5M (~$10M) in June 2026, from Creandum, K-Fund, Calafia Iberia and others.
- **Location:** hubs in **Madrid** and Munich, in person.
- **Example on their homepage:** *"Found a $970 saving, 2% early payment discount with Atlas Freight"* on a $48,500 invoice.
- **Stack:** *"TypeScript · Python · LangGraph · LlamaIndex · Neo4j · PostgreSQL · Redis · React"*.

## What their job posts reveal (load-bearing)

> ⚠️ Exa's index returned both posts, but **they no longer appear among the 7 open roles on Ashby today**. Read them as how they thought a few months ago.

**Product Engineer, Agent Economics:**
> "when a buyer approves an invoice on Causa Prima, the supplier's agent, the buyer's agent, and potentially competing underwriters enter a sealed-bid, second-price auction that clears in seconds."
> "The mechanism has to make truthful behavior the smart play for every participant"
> "Stress-test adversarially. Information leakage in repeated play, collusion vectors, prompt-injection surfaces in agent decision functions."
> "the judgment to know where classical assumptions stop holding when the players are AI agents, not rational humans."

**Senior AI / LLM Agent Engineer:**
> "the separation between LLM reasoning and deterministic enforcement. LLMs inform; rules enforce."
> "structured output contracts via Pydantic schemas"
> "Agents operate within a zero-trust model. You'll design how agents verify independently against source data, how outbound content is reviewed, and how the system prevents cascading failures from prompt injection."

## What the organizers said

- Geoffrey Rolin Jacquemyns (organizer): *"Ranked on the value it captures. Nothing stops the agent across the table from lying to yours. The challenge was built with Causa Prima, who work on agent-to-agent systems, and stress-tested with Nova."*
- Nova: *"No rules against the other agent lying to yours. Only the value it captures counts."* Prizes: Nova lifetime memberships and cash.
- The CEO's own post (*"Cheat, trick, hack. 🦞 and 🤖…"*) **has been deleted** and is not in the Wayback Machine. Google keeps only the snippet: *"…Causa Prima based on its underlying technology with the help of Nova Talent."*

## Implications

1. **The scenario may be early-payment / invoice terms rather than a generic price haggle.** [Likely, unverified] The snippet says the challenge builds on their technology, and that technology is exactly this. If so, the negotiation is multi-variable: discount, days early, amount, maybe a financier.
   - **Know the math:** a 2% discount for paying 20 days early (2/10 net 30) = 2/98 × 365/20 = **37.2% annualized**.
   - The buyer pays early if that return beats its cost of capital. The supplier gives the discount while it is cheaper than its own financing.
   - The ZOPA sits between those two rates.
2. **They designed with prompt injection and information leakage in mind.** Expect both from other teams, and probably test cases from the organizers. Their own default defense is *LLM proposes, code enforces*.
3. **They know auction and mechanism design.** If the format includes sealed bids or a second-price rule, bidding your true value is optimal there, and haggling tactics stop applying.
4. **Domain edge for Lucas.** Kevel runs on second-price auctions, floors and runner-ups setting the price; so did Topsort. Aleksandar comes from audio adtech (Triton), so the auction language is shared.

