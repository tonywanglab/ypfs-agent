# Query 1 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: agent/system_prompt.md
Tool calls: {"search_corpus": 5}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I have strong precedents. Here is my recommendation.

---

# Summary of core design dimensions

Before recommending, let me reframe the question in the terms we use for this analysis. The company's problem is being described as "downgrade + investors fleeing + short-term liquidity crisis." The operative issue is **viability** — do markets and counterparties believe this insurer can continue as a going concern? A downgrade-driven run is a symptom of a viability judgment, not a standalone "liquidity" problem. So the first-order question isn't "is it illiquid or insolvent" but: *is the underlying insurance business viable once the disaster losses are absorbed, and can official support make that viability credible to the market?*

That distinction drives everything, because the disaster loss is a **one-time exogenous shock** to an otherwise potentially sound franchise — which is a materially better setup than a firm whose losses come from its own core business model.

The core design dimensions you will need to decide on:

1. **Viability triage** — is the going concern sound after the disaster hit, or is the disaster loss large enough to render the franchise nonviable?
2. **Instrument** — secured loan/credit line vs. capital injection vs. guarantee vs. a package.
3. **Collateral** — what can secure a loan; here the insurance subsidiaries are the key asset.
4. **Pricing** — critically, whether to price punitively.
5. **Conditionality and moral-hazard controls** — equity stakes, governance, asset sales, wind-down of the problem unit.
6. **Speed and legal authority** — a run is a clock; the response must be operational fast.

Two precedents in our corpus map almost directly onto this: **AIG (US, 2008)** — a globally significant insurer that suffered a ratings downgrade triggering collateral calls and a near-bankruptcy run, rescued by a secured revolving credit facility — and **Parex (Latvia, 2008)**, a systemic institution stabilized through collateralized liquidity plus a controlling equity stake and eventual good-bank/bad-bank split.

---

# Program Archetypes

## Option 1 — Secured revolving credit facility against the insurance subsidiaries (the AIG-RCF model)
If the disaster loss is contained and the core insurance subsidiaries continue to throw off strong cash flows, the cleanest tool is a large secured credit line. In AIG's case, the government took a security interest in the majority of AIG's assets — including equity in its insurance subsidiaries — precisely because those subsidiaries "were believed to be relatively sound and could continue to provide strong cash flows or could be sold to make up for any losses on the overall company and repay any federal assistance" ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]).

This is the key parallel to your situation: a disaster loss at the parent, with viable insurance subsidiaries underneath that can serve as collateral. The loan buys time and lets the firm meet obligations as they come due while it sells non-core assets in an orderly manner rather than a fire sale ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]).

**A caution from the same case, though:** AIG's facility was priced very punitively — LIBOR + 8.5% with a 3.5% floor and an 8.5% commitment fee, plus a 79.9% equity interest ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]). Those terms had to be restructured downward repeatedly (November 2008, March 2009) because they were too onerous to allow recovery. I would **not** replicate the punitive pricing (see Complementary Considerations).

## Option 2 — Collateralized liquidity + controlling equity stake + eventual restructuring (the Parex model)
If the disaster loss is large enough that the firm needs not just liquidity but a recapitalization and possibly a separation of good/bad exposures, the Parex template applies. Latvia provided liquidity by having the Treasury place securities the bank could pledge for central-bank cash, took a controlling stake (51%, later 85%), and ultimately split the institution into a good bank (Citadele) and a bad bank (Reverta) ([vol7_iss1_13][Latvia: Parex Bank Emergency Liquidity Program, 2008][case_study][2025-04-15]).

Two Parex lessons are directly relevant:
- **Liquidity alone did not stop the run.** "Deposit runs continued even after the announcement of the Treasury deposit, central bank liquidity facility, recapitalization measures, and the full takeover" ([vol7_iss1_13][Latvia: Parex Bank Emergency Liquidity Program, 2008][case_study][2025-04-15]). Liquidity support served "the purpose of keeping the bank afloat until the long-term restructuring (or liquidation) plan [was] drawn up." So if the franchise is impaired, plan for the follow-on structural intervention from day one.
- **A partial withdrawal freeze** was used to halt the run mechanically — a blunt tool, but available for a policyholder/creditor run if outflows are uncontrollable ([vol6_iss3_16][Latvia: Parex Bank Capital Injection, 2008][case_study][2024-10-09]).

## Option 3 — Facilitated orderly resolution / wind-down (the Anglo cautionary tale)
If triage shows the insurer is **not viable** even after absorbing the disaster loss, do not use emergency liquidity to indefinitely postpone that reckoning. The Anglo Irish case is the warning: ELA meant as a temporary bridge became the bank's primary funding source for nearly four years because authorities delayed the decision to wind it down, and the central bank found itself "locked into" the arrangement ([vol7_iss1_11][Ireland: Anglo Irish Bank Emergency Liquidity Assistance, 2009][case_study][2025-04-15]). The lesson: emergency liquidity should be calibrated with "incentives... in place for a timely exit" and should not substitute for a resolution decision ([vol7_iss1_11][Ireland: Anglo Irish Bank Emergency Liquidity Assistance, 2009][case_study][2025-04-15]).

---

# Complementary Considerations

- **Do not price punitively.** For a targeted single-firm rescue, only "lend freely" survives from Bagehot's dictum. A punitive rate has two damaging effects: it makes the firm reluctant to draw the liquidity it needs, and any draw brands the firm to the market as desperate — which can accelerate the very run you're trying to stop. AIG's punitive terms had to be walked back repeatedly. Where the collateral (the insurance subsidiaries) is good, solvency and moral-hazard concerns are largely moot for the *loan itself*, because you can realize the collateral. Price to allow recovery, not to "make it sting."

- **Handle moral hazard in the structural layer, not the loan.** Moral hazard is an incentive-design issue, not a moral judgment, and it is best addressed through the follow-on interventions: an equity stake, governance/management change, dividend and compensation restrictions, and mandated sale of non-core assets. Both AIG (79.9% equity via an independent trust) and Parex (controlling stake, wiping out prior majority shareholders) captured upside for the taxpayer and imposed discipline on owners this way ([vol3_iss1_7][The Rescue of American International Group Module F: The AIG Credit Facility Trust][case_study][2021-04-16]; [vol7_iss1_13][Latvia: Parex Bank Emergency Liquidity Program, 2008][case_study][2025-04-15]).

- **Watch the collateral-call channel.** AIG's near-death was driven not by policyholder claims but by a downgrade triggering mass *collateral calls* on its derivatives book ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]). Identify quickly whether your insurer has similar downgrade-triggered contractual outflows (reinsurance, derivatives, financing agreements); the size of your facility must cover those, not just claims.

- **Ring-fence the healthy insurance subsidiaries.** The recurring theme is that the *insurance operations* are the sound, cash-generative, saleable asset. Protect and, if needed, sell them in an orderly way rather than let a parent-level problem contaminate them.

- **Fiscal loop and sizing.** The Anglo case underscores recognizing the fiscal implications upfront so you don't create a sovereign–firm loop that is hard to exit ([vol7_iss1_11][Ireland: Anglo Irish Bank Emergency Liquidity Assistance, 2009][case_study][2025-04-15]).

- **Language matters.** Avoid public use of "insolvent." A disaster-driven, one-time loss at an otherwise viable insurer can be described accurately without terminology that itself fuels a run.

---

# Suggested Framing

I would frame this to decision-makers as a **two-step decision, not one**:

1. **Triage viability first (over a very short window):** Is the core insurance franchise viable once the disaster loss is absorbed? A natural disaster is an exogenous, largely one-time shock — meaningfully different from losses stemming from a broken business model — so the base case may well be "viable but running." Assess the downgrade-triggered contractual outflows to size the need.

2. **Then match the instrument to the triage result:**
   - **Viable franchise, contained loss →** a generously-sized, adequately-secured credit facility against the insurance subsidiaries (Option 1), priced to permit recovery, with moral-hazard controls in the conditionality rather than the rate.
   - **Viable but impaired, needs recap →** the Parex-style package: liquidity to stop the bleeding, a capital injection with a controlling stake, and a planned good/bad separation, recognizing that liquidity alone may not stop the run (Option 2).
   - **Nonviable →** use liquidity only as a bridge to an orderly, time-bound resolution, with a hard exit — explicitly avoiding the Anglo trap of open-ended support (Option 3).

The through-line: lend freely against the good collateral you have (the insurance subsidiaries), don't brand the firm with punitive pricing, and put the discipline in the structural conditions. You are the advisor here — these are the options and their tradeoffs; the sizing, fiscal appetite, and viability call are decisions for the principal, ideally informed by a rapid independent assessment of the disaster loss and the subsidiaries' standalone value.