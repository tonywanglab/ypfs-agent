I now have comprehensive material to build a well-grounded set of options. Here is the plan.

---

# Summary of Core Design Dimensions

Your situation maps cleanly onto what the YPFS literature calls a **broad-based emergency liquidity (BBEL) program**: an emergency intervention targeted at a *wide range* of institutions during *systemwide stress*, distinct from ad hoc rescue of a single firm. You are in the **acute phase** of a crisis — a run on a globally significant bank with visible contagion — where the priority is to arrest runs and prevent fire sales, *not* to resolve solvency. The key principles from the survey that should anchor every option:

- **Speed and credibility over precision.** Strict solvency screening is impractical in the acute phase; early, credible deployment can stop the acute phase from becoming a chronic one.
- **The central tradeoff is moral hazard vs. stigma.** Penalty rates and restrictive terms curb abuse but can stigmatize users and suppress participation — defeating the purpose. Auctions are the single most important tool for achieving penalty-like pricing *with minimal stigma*.
- **Lean on existing infrastructure.** Programs built on standing-facility collateral schedules, counterparties, and operational plumbing deploy fastest.
- **Modernized Bagehot:** *lend freely and broadly, against good collateral, at rates set by auction, taking care not to disclose individual borrowers* during the acute phase.

The principal decision variables you must set for any archetype: **(1)** pricing mechanism (auction vs. fixed rate; penalty spread), **(2)** maturity (extend beyond your standing overnight facility), **(3)** eligible collateral (narrow vs. wide), **(4)** eligible counterparties (your existing bank counterparties vs. broader), **(5)** size (capped/auctioned vs. full-allotment), **(6)** individual participation limits, **(7)** stigma/disclosure strategy, and **(8)** exit.

---

# Program Archetypes

## Option 1: A Term Auction Facility (recommended primary tool for the acute phase)
A new facility that auctions term funding (e.g., 28- and 84-day) against your standing-facility collateral set, to a broad set of bank counterparties, at a rate set by competitive auction with a low minimum bid. This is the archetype that most directly solves the stigma problem you will face — the bank that is running needs to be *able to borrow without signalling distress*.

Design features drawn from the US Term Auction Facility, the most studied case:
- **Stigma mitigation by design.** The auction format meant "no institution was being forced to borrow"; bidding did not signal abnormal demand. Notably, more than half of TAF participants paid a *premium over* the discount window rate purely to avoid the stigma of being seen at the window — strong evidence the destigmatizing structure worked ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022]).
- **Broad participation and individual caps.** No single bidder could take more than 10% of an auction, so the market knew participation was broad and could not infer identities ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022]).
- **Delayed settlement** (loans settled days after the auction), which is "inconsistent with the needs of a failing institution" and further reduces adverse-selection signalling ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022]).
- **Use existing collateral plumbing.** TAF used the discount window's eligible-collateral set and haircuts but with an over-collateralization cushion (initially 100%, later 33%) — enabling fast operationalization ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022]).
- **Scalability.** Auction sizes can be raised in response to oversubscription; the Fed escalated from $40bn to $150bn per cycle and, after Lehman, effectively moved to full allotment.

*Fit for you:* Strong. You have an existing standing facility (analogous to a discount window) that is likely already stigmatized once a run is visible. A term auction is the proven supplement.

## Option 2: A Contingent / Extended-Collateral Term Repo Facility, activated and scaled to full allotment
A facility — ideally pre-framed in your liquidity toolkit — that the Governor can *activate* on a finding of "actual or prospective market-wide stress," lending cash against the *widest* eligible collateral at term, with terms set on activation. Given contagion is already spreading, you would activate immediately and, if stress is severe, run it **fixed-rate, full-allotment**.

Design features from the UK Extended Collateral Term Repo Facility (ECTR/CTRF):
- Explicitly designed "to provide liquidity against the widest collateral at any time, term and price it chooses, in response to actual or prospective exceptional market-wide stress" ([vol4_iss2_51][United Kingdom: Extended Collateral Term Repo Facility][case_study][2022]).
- It is a **contingency facility**: dormant until the Governor activates it on a market-wide sterling liquidity shortage, at which point the Bank sets the terms ([vol4_iss2_51][United Kingdom: Extended Collateral Term Repo Facility][case_study][2022]).
- When reactivated in March 2020, the BoE preemptively restructured it as **"fixed price, full allotment, in unlimited size"** — the configuration reserved for the most acute stress.

And from the ECB Term Refinancing Operations, the leading full-allotment precedent:
- After Lehman, the ECB switched from variable-rate auctions to **fixed-rate, full-allotment** — participants received whatever they requested at the policy rate — and simultaneously **widened eligible collateral** (lower-rated securities, foreign-currency-denominated instruments, subordinated debt) ([vol4_iss2_38][European Central Bank: Term Refinancing Operations][case_study][2022]). A member of the ECB board called this "the most significant non-standard measure" deployed.

*Fit for you:* Very strong if contagion is broad and accelerating. Full allotment delivers the strongest announcement effect ("financing will be available against good collateral"), but the survey is clear this configuration should be reserved for *the most critical circumstances*, because unlimited size can signal that the situation is worse than it is, and it heightens moral hazard.

## Option 3: An on-demand fixed-rate term facility with widened collateral (the "enhanced window" — use with caution)
Lower the rate, lengthen maturity, and broaden collateral on a bilateral, on-demand basis — essentially a souped-up standing facility offered as a named emergency program (e.g., HKMA's 2008 enhancements; the UK Discount Window Facility).

- The HKMA in 2008 extended discount-window maturities from overnight to three months and broadened collateral using existing authority — fast and simple.
- **Caution flag from the corpus:** the UK Discount Window Facility, designed to address stigma but priced at a high penalty with on-the-day solvency/viability tests, was **never drawn** — banks pre-positioned £265bn+ of collateral but would not use it for fear of signalling weakness ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022]). This is the cautionary counterpoint to Option 1.

*Fit for you:* Useful as a *complement* (a broad-collateral backstop for institutions that cannot access an auction window), but the survey evidence strongly warns that a bilateral, on-demand, penalty-priced facility tends to go unused precisely when a run is underway. It should not be your sole instrument.

---

# Complementary Considerations

- **Run multiple facilities, not one.** The survey's recurring theme is that persistent stress is met with *packages* of complementary BBEL programs — differentiated by maturity, collateral class, and counterparty type (Canada ran three GFC facilities alongside its Standing Liquidity Facility). A practical package: Option 1 (term auction, standard collateral, broad bank access) + Option 2 capability held ready to activate/scale + a wide-collateral backstop.

- **Pricing.** Favor an auction with a *low minimum bid* over a fixed penalty rate. Watch the arbitrage trap: the Fed had to re-peg the TAF minimum to the interest rate on reserves once banks could borrow and redeposit at a profit. Fixed-rate facilities risk either overpricing (stigma, no use — the DWF) or underpricing (moral hazard).

- **Collateral.** Anchor on your standing-facility schedule and haircuts for speed, but **build in administrative flexibility to widen collateral** — eight of the survey's cases expanded collateral mid-program, and the RFC's failure rates fell once it broadened collateral. Add foreign-currency haircut premiums (ECB +8%, Norway +10%, BoE +3%) if you accept non-domestic collateral.

- **Solvency.** Do *not* impose on-the-day solvency/viability tests in the acute phase. They are slow, may be impossible to perform credibly mid-panic, and were a direct cause of the DWF's zero usage. The modernized dictum deliberately omits "solvent."

- **Disclosure / stigma.** Disclose only in aggregate during the acute phase; release individual borrower data only on a substantial lag (the TAF did so years later, post-expiry). Premature naming reliably triggers depositor runs (NYCH 1890; Northern Rock).

- **Your G-SIB and foreign branches.** The TAF permitted US branches/subsidiaries of foreign banks (they were ~65% of borrowing). Given you host a globally significant bank, consider whether foreign-bank branches in your jurisdiction need access, and coordinate with peer central banks — GFC-era responses were highly coordinated (joint announcements, USD swap lines).

- **Legal authority and timing.** The fastest route is existing authority over your standing facilities; reserve new legislation only if you exhaust it. Have the operational work done *before* announcing — announcing and then failing to deliver (Overend-Gurney 1866) worsens panics, while a credible announcement can calm runs even with little drawdown (Canada TLF; UK 1866).

- **Exit.** Build in a natural exit via pricing (so usage falls as markets normalize), a stated (extendable) expiry, and/or wind-down by shrinking auction sizes. Consider retaining the successful facility as a *standing* contingency tool afterward, as the UK and Hong Kong did.

---

# Suggested Framing for Your Supervisor

Frame the choice as **a layered package calibrated to severity**, not a single program:

1. **Immediately deploy a Term Auction Facility (Option 1)** as the workhorse — it delivers broad, penalty-adjacent pricing while neutralizing the stigma that will otherwise cripple uptake during a visible run. This is the lowest-regret first move and is built on existing collateral plumbing for speed.

2. **Hold a full-allotment, wide-collateral term repo facility (Option 2) ready to activate**, escalating to fixed-rate/full-allotment only if contagion broadens — reserving this strongest configuration for the most acute conditions because of its size-signalling and moral-hazard costs.

3. **Add a wide-collateral backstop**, but do not rely on a bilateral penalty-priced window alone — the evidence (the never-drawn UK DWF) shows it will sit idle when you most need it.

Across all three: auction-based pricing, no acute-phase solvency tests, lean on existing collateral schedules with flexibility to widen, aggregate-only disclosure during the panic, and a pre-built operational capability so the announcement is credible the moment it is made.

I can draft term-sheet-level parameters for any of these archetypes, or pull the full ECTR or ECB TRO case studies for deeper design detail on the full-allotment activation mechanics. Just let me know which direction your principal wants to pursue.