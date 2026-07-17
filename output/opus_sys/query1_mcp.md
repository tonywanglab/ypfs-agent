# Query 1 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: agent/system_prompt.md
Tool calls: {"search_corpus": 4, "get_document": 1}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I now have a strong evidentiary base. Let me present the recommendation.

---

# Summary of Core Design Dimensions

Before design, a reframing per your framework. You describe this as a "short-term liquidity crisis," but a rating downgrade plus investor flight at a globally significant insurer is almost always the market rendering a **viability** judgment, not an isolated cash-management problem. The disaster caused a real capital loss; the run is the symptom. So two questions must be separated:

1. **Is the firm viable as a going concern** — inclusive of expected official support? A natural-disaster loss is a discrete, quantifiable, non-recurring shock (unlike AIG's structurally toxic CDS book), which is actually a favorable viability profile: the underlying insurance franchise may be sound once the one-time loss is absorbed.
2. **Is there good collateral?** A large insurer typically holds high-quality investment portfolios and valuable, cash-generative subsidiaries. Per the modernized Bagehot logic, if you can lend against good collateral, the accounting-solvency and moral-hazard debates recede — you can realize the collateral if needed.

The core dimensions you must decide across: **(a) legal authority/who lends** (central bank vs. treasury; insurers usually sit outside the central bank's normal LOLR perimeter); **(b) collateral and valuation** — the binding constraint, requiring rapid independent valuation of the investment book and subsidiary equity; **(c) sizing** — build in a cushion so you never have to publicly re-up; **(d) pricing** — "lend freely," avoid stigmatizing penalty rates on a targeted facility; **(e) conditions/compensation** — where moral-hazard concerns belong (equity, governance, dividend restrictions), not in the loan rate; and **(f) whether liquidity alone suffices** or a capital solution follows.

# Program Archetypes

## Option 1: Collateralized emergency revolving credit facility (the AIG-RCF template)
A secured revolving line sized to cover obligations as they come due, secured on the parent's assets and the equity of its regulated insurance subsidiaries. This is the closest precedent to your situation. In the AIG rescue, the Fed extended an $85 billion secured revolving facility, explicitly reasoning that AIG's insurance subsidiaries "were relatively sound and could continue to provide strong cash flows or could be sold," making the loan adequately securable — the exact distinction that let AIG be helped where Lehman could not ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]).

Key lessons to import and to *avoid*:
- **Do rapid, independent collateral valuation.** The FRBNY advanced funds in tranches (four demand notes over four days) while specialists updated valuations daily, easing into exposure — a sensible model when you cannot fully value the book overnight ([vol3_iss1_2][...Module A: The Revolving Credit Facility][case_study][2021-04-16]).
- **Size with a cushion.** The Fed added $10 billion over the private term sheet specifically so it would not have to increase the line later and signal weakness ([vol3_iss1_2][...Module A][case_study][2021-04-16]). This matters doubly for a disaster loss where ultimate claims are uncertain.
- **Do NOT price punitively.** The RCF's initial rate (LIBOR + 8.5%, ~12%) was internally called "loan shark" territory and criticized as "contrary to the idea of trying to sustain the firm"; it raised leverage and *worsened* downgrade risk, forcing a restructuring within two months ([vol3_iss1_2][...Module A][case_study][2021-04-16]). Per your framework, on a targeted facility only "lend freely" survives — a punitive rate on an already-downgraded firm can accelerate the very death spiral you are fighting.

## Option 2: Securities-collateralized term deposit / liquidity swap (the Parex template)
Rather than a cash loan, the sovereign injects high-quality government securities into the firm, which it then uses as collateral to borrow cash — leaving a term-deposit liability to the treasury. Latvia used exactly this for Parex when the bank faced maturing wholesale loans it could not roll and a deposit run: the Treasury deposited Treasury securities that Parex pledged to borrow from the central bank ([vol7_iss1_13][Latvia: Parex Bank Emergency Liquidity Program, 2008][case_study][2025-04-15]).

This is attractive when (i) the insurer's own collateral is illiquid or hard to value quickly (disaster-impaired assets), and (ii) the central bank lacks authority to lend directly to a non-bank insurer. It required a legal amendment (Latvia expanded the Treasury's power to make term deposits in commercial institutions) ([vol7_iss1_13][Latvia: Parex Bank Emergency Liquidity Program][case_study][2025-04-15]) — a live consideration since insurers typically sit outside standing LOLR authority. Note Latvia also took lower-quality collateral against the deposits, and the structure was designed to be *convertible to equity later* if the situation proved to be capital rather than liquidity — which it was.

## Option 3: Liquidity-plus-capital package with staged intervention
Treat the emergency loan as the first move in a sequence, with capital and restructuring following once the disaster loss is quantified. In both AIG and Parex, the initial liquidity line proved insufficient because the problem was ultimately capital, and both migrated to capital injections and restructuring ([vol3_iss1_2][...Module A][case_study][2021-04-16]; [vol6_iss3_16][Latvia: Parex Bank Capital Injection, 2008][case_study][2024-10-09]). If your viability diagnosis suggests the disaster impaired capital (not just cash flow), plan the sequence now: liquidity to stop the run today, capital to restore viability once losses crystallize.

This is where **moral-hazard tools belong** — in the structural follow-on, not the emergency loan. AIG's equity feature (79.9% via convertible preferred held in an independent trust) served to compensate taxpayers for risk, penalize shareholders, provide upside, and give control ([vol3_iss1_2][...Module A][case_study][2021-04-16]). The Parex sequence similarly wiped out and diluted existing shareholders through staged capital injections ([vol6_iss3_16][Latvia: Parex Bank Capital Injection, 2008][case_study][2024-10-09]).

# Complementary Considerations

- **Legal authority.** Insurers rarely fall under the central bank's ordinary lending perimeter. AIG required invoking emergency authority (Fed §13(3), "unusual and exigent circumstances," plus a collateralization test) ([vol3_iss1_2][...Module A][case_study][2021-04-16]); Latvia amended budget law to permit Treasury term deposits ([vol7_iss1_13][Latvia: Parex Bank Emergency Liquidity Program][case_study][2025-04-15]). Identify your enabling authority immediately — time is decisive, and drawn-out legislative debate undermines confidence.
- **Verbiage discipline.** Publicly, frame this as an isolated, quantifiable disaster loss at an otherwise viable franchise, and avoid the word "insolvent." Loose language can itself trigger runs. Note the Fed deliberately timed its AIG restructuring announcement to coincide with an earnings release precisely to get ahead of an anticipated downgrade ([vol3_iss1_2][...Module A][case_study][2021-04-16]) — communication sequencing matters.
- **Governance.** Requiring management change and dividend suspension (as with AIG) addresses accountability without pricing the firm to death.
- **Exit.** Design repayment through asset sales/subsidiary disposals and normalize before exiting — the FRBNY exited only once AIG "looked like a normal company," to avoid re-triggering failure ([vol3_iss1_2][...Module A][case_study][2021-04-16]).
- **Rating-agency feedback loop.** Every design choice (leverage added, rate charged, commitment fee) feeds the downgrade dynamic. Onerous terms *raise* leverage and *lower* interest coverage — the metrics agencies watch — and can provoke further downgrades ([vol3_iss1_2][...Module A][case_study][2021-04-16]).

# Suggested Framing

Recommend to your principal a **two-stage response**: (1) an immediate, generously-sized, non-punitively-priced secured liquidity facility to halt the run — structured as a revolving credit line (Option 1) if the firm's investment book and subsidiary equity can be valued and pledged quickly, or as a securities-for-collateral term-deposit swap (Option 2) if collateral is illiquid or direct central-bank lending authority is lacking; and (2) a pre-planned pivot to capital and restructuring (Option 3) once the disaster loss is quantified, with all moral-hazard/compensation features (equity stake, dividend freeze, governance change) placed in that stage rather than baked into the emergency loan.

The decisive analytical step remains yours: an independent, rapid valuation to establish whether this is a viable franchise absorbing a one-time hit (favors full support and likely recovery, as the disaster loss is discrete and non-recurring) or a fundamentally impaired institution. The former was effectively AIG's insurance-subsidiary story that justified lending; the latter is the Parex story that required eventual restructuring. I can draft term-sheet parameters (sizing logic, collateral haircuts, valuation-agent mandate) for whichever archetype you prefer.