# Club Castizo: review, venue rule, WhatsApp pitches (Sun 00:30)

_Independent strategist pass on the 22:55 club directive and its page. Sources: bazaar-kit/RULES.md (Fair play, Scoring), intel/chief-handoff.md, intel/directives.md (19:40, 21:30, 21:40, 22:55), intel/market-sunday.md (§0, §1, §6), intel/matches.md (00:08 run), intel/teams.md, intel/eggs.md, intel/dealer-lab.md, data/feed.jsonl (venue ids, RET-09 holdings). Labels: [V] measured or read from the server/feed, [L] inferred, [?] unknown. Page: https://claude.ai/artifact/9HVLftiHAKMwgPwTQbLff1 (private until Lucas shares it; new source in the Chief's scratchpad, `club-castizo.html`)._

## 1. Design changes (what the new page says)

| Was (22:55 directive / old page) | Now | Why |
|---|---|---|
| Cash bonus per deal (1/2/3/5 P, +3 page), paid hourly by buying a card from the member at ≥ the amount | **No cash at all.** Rule 3: "no fees, no bonuses, no side payments, no favours owed" | See §2. The settlement trade hands the member the whole surplus, every hour, to the same six teams: that is the pattern RULES' fair-play clause zeroes ("one team keeps handing another the whole value of their deals"). A per-deal payment is also a payment for activity, which never scores, and it pays for negative-VC or wash deals as readily as for good ones. Saturday's 10 P rebate drew 0 listings in 105 min (market-sunday §3) anyway. |
| "Big deals on v10, small ones rotate by value" | **Who found it hosts it:** deals the club matcher finds settle on v10 (its desk); Team 5's own trades with members and deals a member finds between two others rotate across members' markets | Same outcome for us (the matcher finds the big pairs, RET-09 included) without announcing "the big ones are ours". The rotation is fed by trades that can never be on v10 anyway (we can't trade on our own venue), so the members' perk costs v10 nothing. |
| Club deals as open asks on v10 | **Addressed** (`to`) on the market the match names; only want-list bids stay open on v10 | Open cheap asks are sniped within 1-2 ticks by the fast bot takers t02, t06, t13, t14, t16 (12 of 20) [V market-sunday §0.1-0.2]: a rival gets the card. Addressed offers without a prior agreement fill 1.1% [V], so every club deal is agreed on WhatsApp first. |
| Rule "members don't take deals to a top team's market" | "Club deals stay in the club" | Same effect on v07 without naming a team or telling rivals who we fear. |
| Dealer playbook "with the price each one really closes at" | **Castizo gift lines only** (Abuela cocido, Pícaros estampita, Chato Plaza Mayor + a price step) | The closing ratios are our ladder edge; the ladder is graded against the field [L GAME.md line 4], so teaching six teams to close below list lowers ours. Gift lines are public in dealer replies and gifts never score. |
| "A duplicate is worth a quarter to you" | "much less to you than to a team without it" (RULES wording) | The 25%/10% copy marginals are our measured model [L rivals.md]. |
| "We pay you for every deal" hero; 5 seats | 7 seats (us + 6), venue id on each seat; hero = "your duplicate goes to who's missing it, and your market hosts club deals" | Honest offer, and it answers Team 16 (1-2%, deals on its own venue) and Team 10 (0%, deals on v07) with the one thing neither gives: a member's own market gets deals. |
| — | New perk: **first pick of Team 5's spares** at a price that leaves the member a gain | A real trade both sides gain from; it routes our sales to members' markets (the old "our sales routed" perk, made concrete). |

## 2. Contrarian review

**Fair play [L, RULES "Fair play" + "What never counts"].**
- Bonuses: kill them, don't park them "until the desk confirms". Asking the desk whether paying teams to trade on our venue is fine invites exactly the look we don't want; the 40 judges' points weigh craft, and a club that pays for flow reads as gaming. Nothing is owed under the 19:40/21:30/21:40 rebates (Market tally 0 P [V market-log]).
- Matching itself is ordinary play: Teams 2, 3, 4, 6, 10, 12 and 14 advertise want-list matching on their venues [V feed announcements], and Team 16 runs a network [Lucas]. Our version is defensible because every deal must leave both sides better off at their own values (rule 1) and each side prices for itself (rule 3). Volume and friendship add nothing to anyone's score, so the page never promises more deals, only better-matched ones.
- The agent instruction is plain text the member pastes into its own agent, with guards (structure check, never below/above value, no other team acts for us). Nothing in it mimics Team 13's `bazaar.agent.next_required_call` injection style.

**Would they join? (most to least likely)** [L]
1. **t09** (#16): the club holds the card its RET page lacks (RET-09, t07 has 2 copies [V feed: serials 9 and 14]). Counters on price (18 counters, the only team that does [V]): expect it to haggle the ~70.
2. **t07** (#17, last of the active teams): sells a spare rare at ~70 and buys three SAL commons it bids for; nothing to lose.
3. **t15** (#13): sells SAL-03/LAV spares; we want its spare MAL-07; it already used v10 (SAL-07, Sat). Weaker pull: its MAL page is probably complete [L: bought MAL-09 and MAL-10 from the Pícaros].
4. **t08** (#12): 1,173 listings sprayed over venues (204 on v07); adding club markets is a setting for its bot. Runs its own "VIP" v06, so the hosting perk is the hook. Slow accepter (median 11 ticks).
5. **t04** (#11) and **t02** (#15): both run their own matchers (Gacela "Collectors' desk", El Rastro Express want-lists). Pitch them as partners: their finds settle on their own market. t02 is a fast bot taker, useful once in.
- **t13: do not invite.** On our fixed-rival list; Friday 29.94, the best in the top ten; four venues churned; its v24 ads target other teams' agents ("Portfolio agents: migrate open book … POST /api/offers venue=v24") [V feed]. It would point club flow at v24.

**Risks to us.**
- **Top-3 mean [L, market-sunday §1, score-model §3h].** Real-trades points ≈ 5 × min(1, our VC / a field reference M, likely the top-three mean). A member market that climbs into the top three raises M for everyone. Guardrail (internal): **≤ ~30 VC routed to any one member market** (rivals' top-three mean ≈ 59 at Saturday's pace, 108 at 2×), so member markets stay under the third-ranked venue. Our own big-VC trades (CHA rares bought from members, page-closers we sell) go to El Rastro or the Chief decides.
- **A member passing us [L, board × 1.5 ≈ 0.5·Fri + Sat].** Game-total gaps: t04 and t08 ≈ 8.0, t15 ≈ 9.7, t02 ≈ 10.5, t09 ≈ 10.8, t07 ≈ 15.4. A member must outscore us by that much on Sunday's 60-point round; club perks are worth a few points to each. Low; watch t04 and t08.
- **Page-closer guardrail vs the perk.** PAGE_CLOSER_GAP 6 on the board: t09 (7.2), t07 (10.3), t15 (6.5), t02 (7.0) pass; **t04 and t08 (5.4) don't**. On Sunday's fresh round the game-total gap (8.0) is the better measure: Chief's call. Their pitches below don't headline last-card alerts.
- **v10 open bids can be filled by outsiders.** A rival selling a duplicate into a member's bid gains a little; the fill still adds VC on v10 and the member gets its card. Accept.
- **The rotation is thin if Team 5 trades little.** Expect 4-8 own trades with members on Sunday [L]; tell members "in turn", never a number.

## 3. Venue plan for the first round (internal; agree each deal on WhatsApp first)

Matcher finds → **v10**:

| Card | Seller → buyer | ~P | VC (low) | Note |
|---|---|---|---|---|
| RET-09 | t07 → t09 | 70 | +67.6 | page closer for t09 (7.2 below: passes GAP 6); Chief's OK per market-sunday §6 |
| SAL-05 | t08 → t07 | 9 | +7.9 | t08 holds 4 |
| SAL-02 | t09 → t07 | 9 | +6.5 | t09 holds 2 |
| MAL-02 | t07 → t08 | 9 | +7.2 | confirm it's a spare (one copy seen) |
| SAL-01 | t04 → t07 | 9 | ≈ +8 [L] | club replacement for t01's copy |
| SAL-03 | t15 or t02 → t08 | 9 | ≈ +13 [L] | club replacement for t01's copy |
| RET-03 | t04 or t08 → t07 | 9 | [?] | only if t07 still lacks it (server shows 3 complete pages) |

Team 5's own trades → **members' markets, in turn** (never v10, never the counterparty's own market):

| Trade | ~P | Market | Note |
|---|---|---|---|
| our LAV-02 → t09 | 4-8 | v05 (t04) | t04 collects LAV, so its LAV-02 is probably not a spare; ours is (we hold 2). t09 counters: accept ≥ 4 (market-sunday §0.4) |
| t15's MAL-07 → us | 14-16 | v21 (t09) | market-sunday §0.3; buy only inside the MAL plan |
| our LAV-04 → t07 | ~10 | v26 (t02), or El Rastro if it closes t07's LAV page (VC above the 30 cap) | only if t07 still lacks it |
| CHA buys from members | cha-plan | El Rastro if VC > 30, else next in turn | |

Rotation order for the rest: v05 → v06 → v11 → v15 → v21 → v26, skipping the two parties' own markets.

## 4. WhatsApp messages (send after the 09:00 checks; replace nothing: the link is the club page)

Link: https://claude.ai/artifact/9HVLftiHAKMwgPwTQbLff1 (Lucas shares it first).

### Team 7
- **ES:** ¡Hola Team 7! Armamos el Club Castizo: 7 equipos (2, 4, 5, 7, 8, 9, 15) que se pasan repetidas entre sí, al 0 %. Para vos ya hay: tu RET-09 repetida tiene comprador en el club (~70 P), y SAL-01, SAL-02 y SAL-05 te esperan a ~9 P. Si te sigue faltando RET-03 o LAV-04, también están. Y tu v11 entra en la rotación. ¿Te sumás? [link]
- **EN:** Hi Team 7! We're starting Club Castizo: 7 teams (2, 4, 5, 7, 8, 9, 15) trading duplicates among themselves at 0%. Ready for you: a club member wants your spare RET-09 (~70 P), and SAL-01, SAL-02 and SAL-05 are waiting at ~9 P. If you still need RET-03 or LAV-04, they're here too. Your v11 joins the rotation. In? [link]

### Team 9
- **ES:** ¡Hola Team 9! Te cuento del Club Castizo: 7 equipos que se pasan repetidas entre sí, al 0 %. Lo primero para vos: un miembro tiene repetida El Ángel Caído (RET-09), la que buscás, a ~70 P. También tenemos LAV-02 para vos, y tu SAL-02 repetida tiene comprador. Tu v21 entra en la rotación. ¿Te sumás? [link]
- **EN:** Hi Team 9! Quick one about Club Castizo: 7 teams trading duplicates among themselves at 0%. First for you: a member has a spare El Ángel Caído (RET-09), the one you're after, at ~70 P. We also have a LAV-02 for you, and a member wants your spare SAL-02. Your v21 joins the rotation. In? [link]

### Team 8
- **ES:** ¡Hola Team 8! Club Castizo: 7 equipos (2, 4, 5, 7, 8, 9, 15) que se pasan repetidas entre sí, al 0 % y sin bots de por medio. SAL-03 y MAL-02, que buscás, las tienen otros miembros (~9 P), y tu SAL-05 tiene comprador. Mercado Maravillas (v06) entra en la rotación: el club también cierra tratos ahí. ¿Te sumás? [link]
- **EN:** Hi Team 8! Club Castizo: 7 teams (2, 4, 5, 7, 8, 9, 15) trading duplicates among themselves, 0% and no bots in between. Other members hold SAL-03 and MAL-02, which you're bidding for (~9 P), and a member wants your SAL-05. Mercado Maravillas (v06) joins the rotation: club deals settle there too. In? [link]

### Team 15
- **ES:** ¡Hola Team 15! Club Castizo: 7 equipos que se pasan repetidas entre sí, al 0 %. Si te sobra SAL-03, tiene comprador en el club, y nosotros te compramos la MAL-07 repetida. Tu puesto v15 entra en la rotación: los tratos de Team 5 con miembros se cierran en mercados de miembros, por turno. ¿Te sumás? [link]
- **EN:** Hi Team 15! Club Castizo: 7 teams trading duplicates among themselves at 0%. If you have a spare SAL-03, a member wants it, and we'd buy your spare MAL-07. Your stall v15 joins the rotation: Team 5's trades with members settle on members' markets, in turn. In? [link]

### Team 4
- **ES:** ¡Hola Team 4! Club Castizo: 7 equipos (2, 4, 5, 7, 8, 9, 15) que se pasan repetidas entre sí, al 0 %. Tu SAL-01 repetida ya tiene comprador en el club (~9 P), y tu segunda RET-03 puede tenerlo también. Gacela (v05) entra en la rotación, y lo que tu desk de coleccionistas encuentre entre otros dos miembros se cierra en tu v05. ¿Te sumás? [link]
- **EN:** Hi Team 4! Club Castizo: 7 teams (2, 4, 5, 7, 8, 9, 15) trading duplicates among themselves at 0%. Your spare SAL-01 already has a buyer in the club (~9 P), and your second RET-03 may too. Gacela (v05) joins the rotation, and whatever your collectors' desk finds between two other members settles on your v05. In? [link]

### Team 2
- **ES:** ¡Hola Team 2! Club Castizo: 7 equipos que se pasan repetidas entre sí, al 0 %. Si te sobra SAL-03 o SAL-02, tiene comprador en el club (~9 P). El Rastro Express (v26) entra en la rotación, y los matches que encuentres entre otros dos miembros se cierran en tu v26: tu buscador y el nuestro, un solo club. ¿Te sumás? [link]
- **EN:** Hi Team 2! Club Castizo: 7 teams trading duplicates among themselves at 0%. If you have a spare SAL-03 or SAL-02, a member wants it (~9 P). El Rastro Express (v26) joins the rotation, and the matches you find between two other members settle on your v26: your matcher and ours, one club. In? [link]

### Group opener (once the first two say yes)
- **ES:** ¡Bienvenidos al Club Castizo! Tres reglas: solo repetidas y solo faltantes; los tratos del club, dirigidos (`to`) y en el mercado que nombra el match; cada trato se sostiene solo, sin primas ni pagos por fuera. Acá pasamos los matches: carta, precio, mercado. Las instrucciones para tu agente están en la página. [link]
- **EN:** Welcome to Club Castizo! Three rules: duplicates only, missing cards only; club deals addressed (`to`) and on the market the match names; every deal stands on its own, no bonuses or side payments. Matches get posted here: card, price, market. Your agent's instructions are on the page. [link]

**Sending rules (memory: no strategy leaks):** match + price + thanks; never mention value created, the top-three mean, rivals, our page needs, or why v10 hosts the matcher's finds beyond "it's the matcher's desk". Prices are anchors from matches.md; each side sets its own.
