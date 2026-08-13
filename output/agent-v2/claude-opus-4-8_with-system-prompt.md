I now have comprehensive material across all the key design dimensions. Here is your options paper.

---

# Summary of Core Design Dimensions

Your situation—a globally significant bank run that is starting to infect other banks—is a classic case for a **broad-based emergency liquidity (BBEL) facility**: a new or modified program available to all banks, layered on top of your existing standing facilities. The corpus material indicates the standing discount window/Lombard facility is the first line of defense, and that policymakers typically open new broad-based facilities precisely when the standing window proves inadequate—either because banks lack eligible collateral, or, critically in a run, because of **stigma** that suppresses window usage.

Before presenting archetypes, the recurring design levers your supervisor will need to decide on are:

1. **Eligible participants** – Stick to your existing depository counterparties (preserves supervisory knowledge), or broaden to nonbanks and foreign-bank subsidiaries/branches. Most jurisdictions agree solvent and viable banks should have access.
2. **Allocation mechanism** – Auction vs. on-demand bilateral (standing-style). This is the single biggest determinant of stigma.
3. **Pricing** – Penalty rate (Bagehot) vs. accommodative; fixed rate vs. auction-determined; minimum bid spread.
4. **Collateral and haircuts** – Narrow/high-quality vs. wide; haircut schedule; foreign-currency premiums.
5. **Term** – Overnight/short vs. one-to-three months and beyond; whether to extend term as stress persists.
6. **Size** – Fixed cap per auction/cycle vs. effectively unlimited (full-allotment).
7. **Stigma strategy** – The cross-cutting theme. Techniques observed: many participants, auction pricing, allotment limits, delayed settlement, and lagged/no name disclosure.
8. **Exit** – Use pricing as a natural exit so usage fades as markets normalize.

A central tension to flag up front: a **penalty rate** (Bagehot's "lend at a high rate") is the textbook design, but the corpus is explicit that penalty rates are *"a double-edged sword, particularly during the acute phase."* Several programs (Canada's Term PRA, Hong Kong 2008) saw negligible uptake until rates were cut. In an active run, deterring use can defeat the purpose.

---

# Program Archetypes

## Option 1: Auction-Based Term Facility (the TAF model)
**Best fit for: acute, stigma-driven runs where banks are afraid to be seen at the window.**

The US Term Auction Facility was designed expressly to deliver discount-window-type funding *without* the stigma. Core features and why they worked:

- **Single-price (Dutch) auction**: all winners pay the *stop-out rate* (the lowest accepted bid). The Fed chose single-price to simplify settlement and encourage aggressive bidding (United States: Term Auction Facility, vol4_iss2_63). Bids were subject to a minimum bid rate, a minimum bid size (originally USD 10 million), and a maximum (10% of the auction amount).
- **Anti-stigma engineering**: Because loans settled simultaneously (with a ~3-day delay) and the maximum-bid rule ensured at least ten banks won each auction, no single bank could be singled out. The minimum rate was set *below* LIBOR and the fed funds rate so that bidding did not itself signal distress. And distressed banks couldn't rely on it because not all bidders win (vol4_iss2_63).
- **Term**: started at 28 days (close to the existing DW maximum it substituted for), later added 84-day loans as stress persisted.
- **Size**: capped per cycle—initially USD 20bn per fortnightly auction, scaled up to USD 150bn per cycle.
- **Breadth**: notably permitted US branches/agencies/subsidiaries of foreign banks; that group became ~65% of borrowing.

**Tradeoffs**: Most effective tool against stigma the corpus documents, and the auction sets price endogenously. But it takes administrative setup (though the Fed repurposed existing DW infrastructure), and auctions on a multi-day cycle are less immediate than on-demand lending—if your run is moving in hours/days, the auction cadence may be too slow as a sole tool.

## Option 2: Contingent / On-Demand Term Repo Facility (the ECTR/CTRF model)
**Best fit for: providing system-wide liquidity insurance against wide collateral, activatable on the governor's authority.**

The Bank of England's Extended Collateral Term Repo (ECTR, later CTRF) facility *"allows the Bank to provide liquidity against the widest collateral at any time, term and price it chooses, in response to actual or prospective exceptional market-wide stress"* (United Kingdom: Extended Collateral Term Repo Facility, vol4_iss2_51).

- **Activation by governor**: the framework can sit dormant and be switched on when liquidity pressures emerge—useful if you want a pre-announced, ready instrument.
- **Widest collateral set**: accepted the same broad collateral as the Discount Window Facility—the widest in the Sterling Monetary Framework—which directly addresses banks that lack the high-quality collateral standing facilities require.
- **Auction with minimum spread**: banks bid a spread to Bank Rate, subject to a minimum (originally 125 bps), paying the lowest accepted spread; bids at the clearing spread received pro-rata allocation.
- **Flexibility in practice**: notably, when actually activated (2012, 2020), the Bank **deviated** from its own framework pricing and fixed-supply structure—reinforcing that you should build in discretion to relax penalty pricing in the acute phase.

**Tradeoffs**: Highly flexible and signals preparedness. But the original ECTR's high minimum spread was, like the UK DWF, criticized as an "extreme step-up in pricing"—an extreme backstop that may see little use unless pricing is relaxed on activation. Good as a contingent backstop; pair with willingness to flex pricing.

## Option 3: Modified Standing Window / On-Demand Fixed-Rate Facility (the DWF model)
**Best fit for: speed and simplicity when you want to act on existing authorities immediately.**

Rather than build a new auction, expand your existing window: broaden collateral, lengthen terms, and adjust the rate. The UK Discount Window Facility is the cautionary reference point.

- **Administratively simplest**: on-demand, bilateral, fixed-rate—no auction machinery.
- **The pricing trap**: a fixed rate risks *overpricing* (stigma + no usage) or *underpricing* (moral hazard + overuse). The UK DWF's high penalty rate is widely argued to have caused its persistent non-use, rendering it a "very extreme backstop" (vol4_iss2_3). It also charged more for larger requests.
- **Stigma is the core weakness**: a bilateral, on-demand window is precisely the structure that generated the discount-window stigma that the TAF was invented to escape. Bernanke's 2007 description—banks fearing that recourse to the window "might lead market participants to infer weakness"—is exactly your run scenario.

**Tradeoffs**: Fastest to stand up and good for immediacy, but the least effective against stigma. If you use it, lean on mitigants: no/lagged name disclosure (the Fed and BoE historically withheld names; Dodd-Frank later set a two-year disclosure lag thought sufficient to limit stigma) and avoid an off-puttingly high rate during the acute phase.

---

# Complementary Considerations

**Stigma is your central design problem.** Given a visible run on a G-SIB spreading to peers, banks will be acutely afraid of looking weak. The corpus's four documented anti-stigma techniques should be built into whichever archetype you choose: (1) many participants; (2) auction pricing (no one is "forced" to borrow); (3) allotment limits; (4) delayed settlement. Add lagged or no name disclosure. This is the strongest argument for **Option 1** as the primary tool.

**Pricing in the acute phase.** Bagehot's "high rate" is the default, and most LOLRs historically priced at a penalty. But the corpus repeatedly warns penalty rates can backfire in the acute phase, and documents multiple programs (Canada Term PRA, Hong Kong 2008) that had to cut rates to get uptake. Recommendation: set a *modest* minimum bid rate (the TAF set its minimum *below* market benchmarks precisely so bidding wouldn't signal distress), and reserve discretion to relax—as the BoE did when it actually activated the CTRF.

**Collateral breadth.** If banks have the collateral but won't use the window, the auction/stigma fix is the priority. If they *lack* eligible collateral, you must widen the collateral set (the ECTR/DWF wide-collateral approach). Consider tiered haircuts by quality and a premium haircut for foreign-currency collateral (the ECB used +8%, Norway +10%, the BoE +3%)—an option only if you accept a limited set of high-quality currencies.

**Eligible participants.** Decide deliberately on foreign banks. The contrast in the corpus is stark: most BBEL programs excluded foreign banks, and Greece's exclusion of foreign-owned banks contributed to a Cypriot parent's liquidation; conversely the TAF's inclusion of foreign-bank subsidiaries made them the largest user group. If foreign-bank subsidiaries are material to your system's plumbing, including them broadens the firewall.

**Term.** Start short (≈28 days, close to your existing window maximum) and pre-plan an extension to ~3 months if stress persists—mirroring the TAF's 28→84-day path and the BoE's adjustments.

**Exit strategy.** Build the exit in from the start via pricing. A premium (or premium haircut) means usage fades naturally as markets recover, making closure easy—the Norway Covered Bond program raised its minimum price step-by-step until auctions drew no bids and the facility lapsed. Note also that several temporary BBEL facilities (BoE ELTR→ILTR, Hong Kong's discretionary lending and swap facilities) were later folded into the standing framework—worth flagging as a possible end-state.

---

# Suggested Framing

For your supervisor, I'd recommend framing this as **a primary tool plus a contingent backstop**, rather than a single choice:

- **Primary: an auction-based term facility (Option 1 / TAF model)** as the workhorse against the run, because stigma is the dominant problem in a visible bank run and the auction structure is the best-evidenced antidote. Engineer it with multiple winners, delayed settlement, a minimum rate set at/below market benchmarks, and no/lagged name disclosure.

- **Backstop: a pre-framed contingent wide-collateral repo facility (Option 2 / ECTR-CTRF model)**, activatable on the governor's authority, to catch banks that lack the collateral the auction or standing window requires—with explicit discretion to relax penalty pricing on activation.

- **Treat a modified standing window (Option 3)** as the immediate stopgap you can deploy *today* on existing authorities while the auction facility is stood up—but recognize its stigma limits and don't rely on it alone.

Present the **penalty-rate decision** as the key live policy choice: textbook Bagehot pricing vs. the documented acute-phase risk that high rates kill uptake. And ask your supervisor to decide explicitly on **foreign-bank eligibility**, given how consequential that choice proved in the case record.

I can draft term-sheet-level specifications for any of these archetypes, or pull the full TAF or ECTR case studies if you'd like to see the complete design-decision detail. Would either be useful?