# Query 1 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 3, "get_document": 1}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I now have a comprehensive evidentiary basis. Here is my recommendation.

---

# Recommendation: Rescue via Emergency Liquidity, Structured to Protect Taxpayers — Modeled on the AIG Playbook

## Bottom line up front

Your scenario mirrors the 2008 rescue of **American International Group (AIG)** almost exactly: a globally significant, ~$1 trillion insurer suffered large losses, was downgraded by rating agencies, faced collateral calls and a run by short-term creditors and counterparties, and asked the government for help. The US government judged that a disorderly failure posed unacceptable systemic risk and ultimately committed $182.3 billion — and, critically, **recovered all of it plus a net profit of $22.7 billion for taxpayers** (Treasury 2013).

Based on that experience, my recommendation is: **do not let the firm fail disorderly, but do not simply hand over money either.** Provide emergency liquidity, but only after you have (1) confirmed the systemic case, (2) exhausted a private-sector solution, and (3) built in taxpayer protections and an exit. Below I lay out the decision framework and the specific design cautions the AIG record teaches.

---

## Step 1 — Verify that failure is genuinely systemic before committing anything

The government's strategy "was not predicated on saving every institution that might fail, but on addressing those whose failure could jeopardize the stability of the system" (Wiggins et al. 2021). Before acting, establish whether this firm's disorderly failure would threaten financial stability. In AIG's case the factors were:

- Size, reach, and name recognition creating **contagion risk**;
- A complex derivatives book concentrated among **the largest global banks**, whose capital would be hit by impaired contracts;
- **Retail dimension** — policyholders, pension plans, municipalities — making the failure potentially *more* systemic than a pure investment bank;
- Knock-on effects into **commercial paper and money-market** funding.

If your firm's failure clears this bar, intervention is justified. If it does not, resist the request.

## Step 2 — Push hard for a private-sector solution first

The Fed used its convening authority to try to assemble a private bank consortium (led by JPMorgan and Goldman) to lend AIG ~$75 billion. Only when that collapsed after Lehman's bankruptcy did the government step in. **Attempt the private solution first** — it conserves public funds and reduces moral hazard. But be prepared: private solutions frequently evaporate in an acute crisis when everyone is hoarding liquidity.

## Step 3 — If you must lend, lend against collateral — but calibrate the terms carefully

The Fed lent under emergency authority, secured by substantially all of AIG's assets, including the equity of its insurance subsidiaries. This is sound: **collateralized lending protects the public purse.** Two important cautions from the record, however:

**(a) Do NOT set a punitive "penalty rate."** The original RCF charged LIBOR + 850 bps (~12%) with an 8.5% commitment fee on undrawn funds. Intended to limit moral hazard and force quick repayment, these "onerous" terms **backfired**: they worsened AIG's leverage ratios, alarmed the rating agencies, and threatened *further downgrades* — the very thing you are trying to prevent. The Fed had to cut the rate by 550 bps within weeks. The YPFS survey of emergency liquidity programs concludes bluntly that for a rescue of a single, market-targeted institution, a penalty rate "is liable to instead accelerate the drain on the affected institution's financial resources (and be disfavored by the market and the rating agencies)." **Save moral-hazard discipline for later structural measures; price the initial liquidity to help the firm survive, not sink it** (Ad Hoc Emergency Liquidity survey 2025).

**(b) Do NOT demand haircuts from counterparties/creditors during the acute phase.** Treasury restructuring officer Jim Millstein warns that forcing a distressed exchange can trigger a rating-agency "D" (default) rating, "which can result in massive collateral calls and potential illiquidity of the already weak firm" — forcing you to put "good money after bad." Haircuts also signal insolvency, accelerating the run, and one arm of government is often on both sides of the deal (Millstein Lessons Learned). Counterintuitively, haircuts can *increase* total government spend.

## Step 4 — The rating agencies are the binding constraint — manage to them

The single most important operational lesson: **"a financial institution cannot operate without at least an investment-grade rating"** (Millstein). Every term you set — loan size, rate, tenor, balance-sheet impact — must be evaluated through the rating agencies' eyes. Much of the AIG restructuring (extending tenor from 2 to 5 years, cutting the rate, converting debt to equity, removing dividend-cumulation) was done specifically to shore up the balance sheet and forestall downgrades that would have triggered collateral calls and killed the firm despite the aid.

## Step 5 — Protect the taxpayer and capture upside

The AIG rescue was not a giveaway. Protections included:

- **Full collateralization** and a **senior secured position**;
- An **equity "kicker"** — a ~79.9% equity interest — to compensate taxpayers for the risk, penalize existing shareholders, and give the public a share of any recovery. (Capping at 79.9% avoided consolidating the firm's ~$1 trillion balance sheet onto the government's under accounting rules.)
- **Governance controls**: veto over dividends, ability to appoint directors, blocks on mergers/asset sales;
- Transactions with counterparties done **at market value** through special-purpose vehicles.

I recommend an equivalent structure. Note the caution: the equity mechanism drew heavy legal challenge (the *Starr* litigation) and charges of "nationalization." Ensure your legal authority is solid and, where you use a trust or SPV, that its independence can withstand scrutiny.

## Step 6 — Attack the *sources* of the cash drain, not just the symptoms

The initial liquidity line ($85bn) proved insufficient because it treated symptoms. Stabilization required purpose-built facilities to remove the two drains:
- The **securities-lending** collateral demands (addressed via a securities-borrowing facility and Maiden Lane II, which took the impaired RMBS off the balance sheet at market value);
- The **CDS collateral calls** (addressed via Maiden Lane III, which bought the underlying CDOs and cancelled the contracts, capping further losses).

Diagnose your firm's specific liquidity drains and design targeted tools to stop them.

## Step 7 — Coordinate, communicate, and plan the exit

- **Coordinate** monetary and fiscal authorities: the central bank supplied liquidity; the Treasury (once it had legislative authority) injected capital to reduce leverage. Liquidity alone cannot fix a capital hole.
- **Embed personnel** in the firm immediately — the government knew little about AIG and had to "learn the company as it was executing the rescue." Get monitors on-site to understand the (often opaque, decentralized) structure.
- **Communicate transparently** — publish terms and purpose; dedicate a communications team; expect intense scrutiny from legislators, oversight bodies, and courts.
- **Define an exit**: repay/terminate facilities, convert and then sell equity over time. AIG's assistance wound down completely by 2012–2013 at a profit.

---

## Important caveats

1. **Expect "whatever it takes" dynamics.** Once you commit an initial large sum, walking away becomes practically and politically impossible; the initial decision may bind you to escalating support. Size your first commitment and conditions with that in mind.
2. **Anticipate fairness criticism.** The AIG rescue was attacked for paying counterparties at par ("backdoor bailout"), permitting employee bonuses, and letting shareholders recover value while homeowners suffered. Consider (carefully) whether limited burden-sharing is feasible without triggering the downgrade/run dynamics described above — but recognize that in an acute, system-wide crisis, "shared sacrifice" may be neither possible nor desirable.
3. **Consider whether a resolution regime exists.** In 2008 the US lacked any orderly-resolution tool for a nonbank, leaving a "binary choice" between disorderly bankruptcy and rescue. If your jurisdiction has since adopted a special resolution/liquidation authority for systemic nonbanks, that may be a superior alternative to an ad hoc bailout — evaluate it first.

**In sum:** confirm the systemic threat, try the private market, then provide *collateralized* emergency liquidity at a *non-punitive* rate, manage relentlessly to the rating agencies, attack the actual sources of the cash drain, take equity and governance rights to protect and reward taxpayers, coordinate liquidity with capital, and plan a clean exit. Executed this way, the AIG precedent shows a systemic-insurer rescue can both preserve financial stability and ultimately turn a profit for the public.