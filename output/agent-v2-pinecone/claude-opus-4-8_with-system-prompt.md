I now have a comprehensive grounding in the BBEL survey framework and the most relevant case studies. Let me present your options.

---

# Summary of Core Design Dimensions

Your situation maps cleanly onto the literature: a run on a globally significant bank ("G-SIB") with emerging contagion is a classic **acute-phase** systemic liquidity event. Your mandate is also clearly scoped — a **broad-based** facility *supplementing existing standing facilities* (not an ad hoc rescue of the single troubled bank, and not a standalone discount-window tweak).

Across the design decisions, every choice you make will be governed by the central trade-off the survey identifies: **moral hazard vs. stigma**. In an acute phase with a running G-SIB, the literature consistently weights this toward *speed, breadth, and stigma-minimization* over moral-hazard discipline. The key dimensions you must specify are:

- **Legal authority** — leverage existing authority for speed (the literature's strongest efficiency theme).
- **Delivery mechanism** — auction vs. fixed-rate/full-allotment standing facility.
- **Rate-setting** — penalty vs. market-clearing; auction format.
- **Collateral** — narrow (track standing facility) vs. wide (broader access).
- **Maturity** — extend beyond your standing overnight facilities (the single most common BBEL move).
- **Eligible counterparties** — banks only vs. broader; foreign bank branches.
- **Stigma strategy & disclosure** — participation limits, delayed/aggregate disclosure.
- **Size signaling & exit** — announcement effect; pricing-based wind-down.

Because the troubled bank is *globally significant*, you should also flag two cross-cutting issues early: (1) likely **foreign-currency** funding needs (consider standing swap lines as a complement), and (2) the value of **internationally coordinated announcement**, given how much announcement effects mattered in the GFC.

---

# Program Archetypes

## Option 1: Term Auction Facility (auction-based, stigma-minimizing) — recommended primary
A new, dedicated facility that auctions term funds against your existing standing-facility collateral schedule, deliberately designed to deliver discount-window-equivalent liquidity *without* the stigma of the window.

- **Mechanism:** Pre-announced auction amount; single-price (uniform) auction; settle with a short delay (e.g., a few days) so the facility cannot serve as an instant lifeline for a failing bank — both features directly attack stigma.
- **Rate:** Minimum bid rate set below interbank rates but above your overnight risk-free/reserve rate, letting the market clear the price.
- **Individual limits:** Cap any single bidder's share of an auction (the Fed used 10%) to guarantee broad participation and prevent identification of borrowers.
- **Disclosure:** Aggregate/auction results contemporaneously; withhold individual borrower identities until well after the acute phase.
- **Why it fits you:** This is the archetypal answer to "run on a major institution + spreading contagion + want broad availability + supplement to standing facilities." The Fed explicitly built the TAF because the stigmatized discount window went unused even after rate cuts; the auction format "arguably had a better chance of avoiding stigma . . . because the auction format implies that no institution was being forced to borrow" ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18]). Empirically, banks paid an average premium above the discount-window rate to borrow via TAF rather than the window — strong evidence the destigmatization worked ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18]).
- **Caveat:** Auctions can leave bidders underfunded if sized too small; the Fed's pre-October-2008 auctions were persistently oversubscribed. Build in the ability to scale auction size and frequency quickly (see Option 3 escape hatch).

## Option 2: Term Repo / Extended-Collateral Term Facility (collateral-flexibility variant)
Rather than a standalone auction, activate or create a **term repo facility against a widened collateral set** — a contingency facility designed precisely for "actual or prospective market-wide stress of an exceptional nature."

- **Mechanism:** Swap cash (or government securities) for a broad collateral pool at term, via auction. The UK's product-mix design used separate narrow/wide collateral pools with differentiated haircuts, which also gave the central bank an **early-warning indicator** as clearing spreads on wider collateral rose with stress ([vol4_iss2_3]... — note: survey, not cited; underlying case is the UK ILTR).
- **Why it fits you:** If the run is partly collateral-driven (e.g., the G-SIB and its peers hold assets that are becoming hard to fund), widening the eligible collateral beyond what your standing facilities accept is the targeted fix. The Bank of England's ECTR/CTRF was explicitly "a new contingency liquidity facility . . . designed to mitigate risks to financial stability arising from a market-wide shortage of short-term sterling liquidity," pre-positioned and then activated when stress materialized.
- **Strength:** Pre-positioning. If your central bank has (or can quickly stand up) a contingent facility with the governor empowered to activate it, you gain speed and a credible signal. The UK later made these permanent standing facilities — a model for your "supplement to standing facilities" framing.
- **Caveat:** Wider collateral = more central-bank risk; manage via haircuts, foreign-currency premiums, and overcollateralization cushions.

## Option 3: Fixed-Rate, Full-Allotment (FRFA) escalation — the "break-glass" overlay
Not a separate program so much as a **state you escalate into** if the run intensifies and contagion accelerates.

- **Mechanism:** Abandon the auction-clearing of price; set a fixed rate and satisfy *all* bids in full at that rate, in effectively unlimited size, against a broad collateral set.
- **Why it fits you:** The survey is explicit that full-allotment/unlimited strategies are reserved for "the most critical situations." Both the ECB (switching its term refinancing operations to fixed-rate full-allotment after Lehman — termed "the most significant non-standard measure") and the Fed (effectively providing full allotment by dramatically increasing TAF auction sizes after Lehman) escalated to this. The BoE pre-structured its reactivated CTRF in 2020 as "fixed price, full allotment, in unlimited size."
- **Strength:** Maximum announcement/confidence effect — designed to "reassure financial market participants that financing will be available against good collateral, lessening concerns about funding and rollover risk."
- **Caveat:** Strongest moral-hazard and monetary-transmission concerns; can signal the situation is worse than believed if deployed prematurely. Treat as a staged option, pre-designed but held in reserve.

---

# Complementary Considerations

- **Lead with your standing facilities, then layer.** The literature's first-move pattern is: lower the borrowing rate, lengthen maturity, expand eligible collateral on the *existing* facilities, then announce the dedicated BBEL program. Among 33 cases, 21 were built out of pre-existing facilities — using existing infrastructure, collateral schedules, and counterparty relationships is the dominant efficiency theme and the fastest path to operationalization.

- **Maturity extension is the single most common BBEL action.** Your standing facilities are presumably overnight/very short. Offer term funding (e.g., 28-day and 84-day tranches, as the TAF did, or 1-/3-month as the HKMA and ECB did) to address the maturity-shortening that defines a run.

- **Eligible participants.** Given a *globally significant* headquartered bank, decide deliberately on **foreign-bank branches/subsidiaries**. The TAF permitted them and they were ~65% of borrowing; the Greece ELA excluded them, which pushed a distressed foreign bank to seek help elsewhere and contributed to a parent's liquidation ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18]). For a globally significant system, inclusivity reduces cross-border contagion.

- **Avoid hard solvency tests in the acute phase.** The survey's restated dictum deliberately omits "solvent," and the UK Discount Window Facility's on-the-day solvency/viability test produced so much stigma it was *never drawn*. In the heat of a run, distinguishing illiquid from insolvent is impractical; rely on good collateral and haircuts instead.

- **Foreign-currency dimension.** A G-SIB run frequently carries cross-currency funding strain. Consider activating/establishing **central bank swap lines** as a parallel measure — the GFC's coordinated swap-line architecture is the precedent.

- **Other measures in the package.** In the acute phase, BBEL is commonly paired with **credit/deposit guarantees** to reassure short-term creditors; in any subsequent chronic phase, solvency must be addressed with fiscal tools (recapitalization, asset purchases) — *liquidity lending cannot fix a solvency problem*. Flag this to your supervisor so the liquidity program isn't asked to do work it cannot do.

- **Communication & coordination.** Clear, confident, consistent messaging drives utilization and can produce a stabilizing announcement effect even with little drawdown (Canada's TLF/PRA-PS; UK 1866). Given the global significance, consider a **coordinated announcement** with peer central banks, as in the December 2007 seven-central-bank action.

- **Stigma and disclosure.** Use auction pricing, broad participation, per-borrower caps, delayed settlement, and **aggregate-only / delayed disclosure** of individual borrowers. Disclosing names contemporaneously reliably triggers pullbacks (NYCH 1890; the RFC reading of borrower names on the House floor accelerated deposit flight at revealed banks).

- **Exit strategy.** Prefer a **pricing-based natural exit** (a premium that becomes unattractive as markets normalize) combined with wind-down by shrinking auction size/frequency. Consider whether to **fold the successful facility into your standing framework** afterward, as the BoE and HKMA did — directly consistent with your "supplement to standing facilities" mandate.

---

# Suggested Framing

For your supervisor, I would frame this as a **single primary recommendation with a built-in escalation ladder**, rather than three competing programs:

1. **Immediately:** Adjust standing facilities (rate down, maturity longer, collateral wider) to buy time — fastest possible action under existing authority.
2. **Primary new program (Option 1):** Stand up a **term auction facility** against your existing collateral schedule, with per-bidder caps, delayed settlement, and aggregate-only disclosure — designed to deliver liquidity broadly while neutralizing stigma. If collateral illiquidity is a driver, adopt the **wide-collateral term-repo variant (Option 2)** instead or in addition.
3. **Pre-position the break-glass (Option 3):** Have a **fixed-rate, full-allotment, effectively unlimited** escalation fully designed and ready, with clear governance for activation if contagion accelerates — but deploy only in the most critical state.
4. **Complements:** Consider swap lines (FX strain), a coordinated international announcement, and ensure the political/fiscal track for guarantees and recapitalization is open in case the crisis moves from acute to chronic.

The unifying principle, from the survey's modernized Bagehot: **in the acute phase, lend freely and broadly against good collateral, at rates set by auction, taking care not to disclose individual borrowers.** Build for speed by reusing existing authorities and infrastructure, and design the exit (and possible standing-facility conversion) in from the start.

Two clarifying questions would let me sharpen specific design parameters and pull the most directly comparable case studies for citation:
- Is the contagion you're seeing primarily **funding-market/interbank** (argues for Option 1) or **collateral-value-driven** (argues for Option 2)?
- Does your central bank already hold **contingent/emergency lending authority** that can be activated by the governor, or would any new facility require fresh legislative authority? (This materially affects how fast each option can be deployed.)