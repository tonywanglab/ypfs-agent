# Summary of core design dimensions

For a contagious bank run involving a globally significant home-country bank, the objective should be framed narrowly: **provide systemwide liquidity against collateral to solvent/viable banks, reduce forced asset sales and rollover panic, and reduce stigma relative to existing standing facilities.** It should not be framed as a rescue of the troubled G-SIB or as a substitute for supervisory, resolution, deposit-insurance, or capital actions.

Core design choices:

1. **Eligibility**
   - Broadly available to all supervised banks, including subsidiaries and branches that already have access to central bank accounts or standing liquidity arrangements.
   - Require that borrowers be assessed as viable / not failing or likely to fail, with supervisory sign-off.
   - Decide explicitly whether domestic branches of foreign banks are eligible; the US TAF allowed US branches of foreign banks, which later became a major share of usage ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18T21:02:50Z]).

2. **Collateral**
   - Use pre-positioned collateral where possible for speed.
   - Options range from:
     - existing standing-facility collateral;
     - a wider collateral set, including loans and less-liquid securities;
     - a special high-quality-securities sleeve valued at par, if the panic is driven by unrealized losses on government or agency securities.
   - Haircuts and margining should remain conservative unless there is fiscal loss protection.

3. **Tenor**
   - Overnight liquidity is likely insufficient in a run. Offer **term funding**: 1 month, 3 months, 6 months, and possibly 1 year.
   - Longer terms reduce rollover anxiety but raise credit, collateral, and monetary-policy risks.

4. **Pricing**
   - Price high enough to preserve incentives to return to markets, but not so high that banks avoid the program due to stigma or cost.
   - In acute contagion, a fixed rate near policy rate plus a modest spread may be more stabilizing than a punitive rate.
   - Auctions can discover price and ration quantity, but may be too slow or uncertain during a fast run.

5. **Allotment / size**
   - In acute contagion, **fixed-rate full allotment** sends the strongest “cash is available” signal.
   - If the main concern is balance-sheet control or moral hazard, use capped auctions with the ability to scale up.

6. **Stigma management**
   - Aggregate disclosure only during the crisis.
   - Broad eligibility, many users, scheduled operations, and delayed borrower-level disclosure reduce stigma.
   - TAF’s auction format was explicitly designed to reduce discount-window stigma by making participation less individually identifiable ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18T21:02:50Z]).

7. **Risk controls**
   - Viability screen.
   - Overcollateralization / haircuts / daily margining.
   - Concentration limits by borrower, unless using full allotment.
   - Legal priority and enforceability of collateral.
   - Fiscal indemnity or Treasury backstop if collateral is valued above market or risk tolerance is exceeded.

8. **Communication**
   - Announce as a **systemwide liquidity insurance facility**, not a bailout.
   - State that the facility is available to meet deposit outflows and rollover needs, against collateral, for sound institutions.
   - Pair with deposit-insurance / resolution messaging if uninsured-depositor panic is central.

# Program Archetypes

## Option 1: Fixed-rate full-allotment term lending facility — “maximum confidence” option

**Design.** Offer term loans or repos to all eligible banks at a fixed spread over the policy rate or reserve remuneration rate. Eligible banks receive the full amount requested, subject to collateral and viability checks. Tenors could be 1 month and 3 months immediately, with a 6- or 12-month operation if market stress persists.

**Best for.**
- Fast-moving systemic run.
- Broad market uncertainty about liquidity availability.
- Situations where the supervisor wants to remove doubt that solvent banks can meet outflows.

**Precedents.**
- ECB shifted to fixed-rate, full-allotment term refinancing after Lehman, expanded collateral, and offered maturities up to one year; peak outstanding exceeded EUR 729 billion and loans were repaid ([vol4_iss2_38][European Central Bank: Term Refinancing Operations][case_study][2022-07-18T21:02:35Z]).
- Bank of England’s CTRF in 2020 used fixed-price, full-allotment, unlimited-size operations against the broad Sterling Monetary Framework collateral set ([vol4_iss2_51][United Kingdom: Extended Collateral Term Repo Facility][case_study][2022-07-18T21:02:43Z]).

**Advantages.**
- Strongest reassurance against contagion.
- Reduces rollover risk and panic selling.
- Operationally simple if built on standing-facility infrastructure.
- Avoids “auction failure” risk during a run.

**Tradeoffs.**
- Central bank balance sheet can expand unpredictably.
- If pricing is too cheap, banks may overuse facility.
- Full allotment puts more pressure on collateral valuation, haircuts, and viability screening.
- If collateral eligibility is widened aggressively, fiscal-loss protection may be needed.

**Possible parameter set.**
- Eligible borrowers: all supervised, viable banks with central bank accounts.
- Collateral: standing-facility collateral plus pre-approved wider collateral; conservative haircuts.
- Tenor: 1 month and 3 months at launch; 6 months if stress persists.
- Rate: policy rate / reserve rate + 25–50 bps; consider higher spread for weaker collateral.
- Size: full allotment subject to collateral.
- Disclosure: aggregate usage only during the program.

## Option 2: Term auction facility — “stigma-reducing but balance-sheet-controlled” option

**Design.** Conduct regular auctions of term central bank credit to eligible banks. Preannounce auction size, tenor, minimum bid rate, and collateral requirements. Successful bidders receive funds at a single clearing rate.

**Best for.**
- Severe funding stress, but not a full-speed digital run.
- A jurisdiction where discount-window stigma is a major impediment.
- Cases where the central bank wants to control the quantity of reserves added.

**Precedent.**
- The Federal Reserve’s TAF offered 28-day and later 84-day loans to primary-credit-eligible banks against discount-window collateral. It peaked at USD 493 billion outstanding and was designed specifically to reduce discount-window stigma ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18T21:02:50Z]).
- Canada’s TLF used weekly single-price auctions to provide one-month funding against non-mortgage loan portfolios, though usage was limited because other facilities were more attractive ([vol4_iss2_35][Canada: Term Loan Facility][case_study][2022-07-18T21:02:33Z]).

**Advantages.**
- Reduces stigma by encouraging multiple banks to participate simultaneously.
- Lets the central bank control size, timing, and reserve impact.
- Auction pricing helps reveal demand.
- Easier to taper as stress recedes.

**Tradeoffs.**
- Slower than full allotment.
- If auctions are undersubscribed, the signal may be adverse.
- Banks in an active run may need certainty, not a probability of allotment.
- If the troubled G-SIB needs immediate liquidity, it cannot rely solely on an auction schedule.

**Possible parameter set.**
- Frequency: twice weekly initially, then weekly.
- Tenor: 28 days and 84 days.
- Minimum bid: reserve rate or OIS-equivalent + modest spread.
- Auction size: large enough to ensure broad allotment; increase rapidly if bid-cover rises.
- Borrower cap: e.g., 10–20% of each auction to avoid one institution absorbing the facility.
- Collateral: standing-facility collateral, with additional collateral cushion.

## Option 3: High-quality securities term funding at par — “unrealized-loss / forced-sale backstop” option

**Design.** Offer term advances to banks secured by high-quality government and agency securities, potentially valued at par rather than market value, with a term up to one year. This is aimed at preventing banks from crystallizing mark-to-market losses to meet deposit outflows.

**Best for.**
- A run driven by concerns that banks hold large high-quality securities portfolios with unrealized losses.
- Banks that are solvent on a hold-to-maturity basis but face deposit outflows.
- Situations where forced sales could spread losses across the system.

**Precedent.**
- The Fed’s 2023 BTFP was made available to all depository institutions after SVB to prevent contagion; it provided advances up to one year, against high-quality securities, valued at par, with no haircut, and backed by Treasury credit protection ([vol6_iss4_1][The 2023 Banking Turmoil: Lessons for EU Resolution Authorities][article][2024-12-17T16:25:05Z]).

**Advantages.**
- Directly addresses a modern run channel: deposits leaving banks that hold underwater high-quality securities.
- Reduces forced-sale externalities.
- Simple message: banks need not dump safe assets into stressed markets.

**Tradeoffs.**
- Par valuation can transfer interest-rate risk to the central bank unless protected by fiscal backstop.
- If no haircut is applied, credit protection is important.
- Less useful for banks whose collateral is loans or lower-quality assets.
- May be seen as subsidizing poor interest-rate-risk management.

**Possible parameter set.**
- Eligible collateral: domestic sovereigns, central bank bills, agency securities, covered bonds of highest quality.
- Valuation: par only with fiscal indemnity; otherwise market value with modest haircut relief.
- Term: up to 1 year.
- Rate: 1-year OIS + 10–50 bps, floored at reserve remuneration rate.
- Borrowing limit: par value of eligible collateral owned before a cutoff date, to avoid arbitrage purchases after announcement.

## Option 4: Wide-collateral contingent term repo / loan facility — “liquidity insurance against illiquid but sound collateral”

**Design.** Activate a facility that lends term cash against the widest collateral set the central bank is willing to accept, including loans, securitized assets, covered bonds, and other less-liquid collateral, subject to haircuts. It can be auction-based or fixed-rate full allotment.

**Best for.**
- Banks have enough economic collateral, but not enough collateral eligible at standing facilities.
- Markets for normally fundable assets are frozen.
- The goal is to let banks use illiquid collateral at the central bank while preserving liquid collateral for markets and payments.

**Precedents.**
- Bank of England’s ECTR/CTRF was a contingent facility designed to provide liquidity against the widest collateral set in times of market-wide stress ([vol4_iss2_51][United Kingdom: Extended Collateral Term Repo Facility][case_study][2022-07-18T21:02:43Z]).
- Canada’s TLF accepted non-mortgage loan portfolios with a 40% haircut to let banks deploy liquid assets elsewhere ([vol4_iss2_35][Canada: Term Loan Facility][case_study][2022-07-18T21:02:33Z]).

**Advantages.**
- Addresses collateral scarcity at the standing facility.
- Useful for banks with strong loan books but limited marketable securities.
- Can be structured with strong haircuts and collateral cushions.

**Tradeoffs.**
- Operationally demanding: loan valuation, legal perfection, documentation.
- Slower unless collateral is pre-positioned.
- Greater valuation and credit risk.
- Haircuts must be conservative; otherwise fiscal protection may be needed.

**Possible parameter set.**
- Eligible collateral tiers:
  - Tier 1: sovereigns / central bank paper.
  - Tier 2: high-quality covered bonds, agency debt, high-grade ABS.
  - Tier 3: performing loan pools.
- Rate: higher spread for wider collateral.
- Tenor: 1–3 months initially; 6 months for pre-positioned collateral.
- Haircuts: stress-calibrated, with margin calls.
- Pre-positioning: require banks to pre-position collateral within 30 days as a condition for continued access.

## Option 5: Hybrid “announce full-allotment now, migrate to auctions later” program

**Design.** Launch immediately with fixed-rate full allotment for a short emergency window, then transition to auctions or capped operations once the panic phase passes.

**Best for.**
- A fast run with uncertain duration.
- Authorities want maximum confidence today but do not want a permanent open-ended balance-sheet commitment.
- Useful if political tolerance for unlimited lending is limited.

**Advantages.**
- Provides immediate reassurance.
- Preserves optionality.
- Allows calibration after observing demand.
- Natural transition to exit.

**Tradeoffs.**
- Communication must avoid making the shift to auctions look like withdrawal of support.
- If stress remains acute, reducing generosity too early could reignite the run.

**Possible parameter set.**
- Phase 1: 30–60 days of full allotment, fixed price, broad collateral.
- Phase 2: regular term auctions with large allotments and standing commitment to scale up.
- Phase 3: taper terms, raise pricing, narrow collateral, and close once market funding normalizes.

# Complementary Considerations

1. **Do not rely on liquidity alone if the G-SIB is insolvent or failing.**  
   The program should support solvent banks systemwide. The distressed G-SIB may require parallel supervisory, recovery, resolution, capital, or deposit-protection actions. Liquidity lending cannot restore confidence if markets believe the institution is fundamentally insolvent.

2. **Coordinate with deposit-insurance and resolution authorities.**  
   If the contagion is driven by uninsured depositors, a lending facility may slow outflows but may not stop them. The 2023 US episode combined liquidity support with a systemic-risk determination protecting all depositors at SVB and Signature; the BTFP was only one part of the package ([vol6_iss4_1][The 2023 Banking Turmoil: Lessons for EU Resolution Authorities][article][2024-12-17T16:25:05Z]).

3. **Prepare fiscal backstop if risk terms are relaxed.**  
   If the central bank accepts par valuation, low/no haircuts, or very wide collateral, seek Treasury indemnity or a loss-sharing arrangement. This protects central bank independence and clarifies fiscal responsibility.

4. **Pre-positioning matters.**  
   A key operational lesson from recent runs is that banks may not be ready to pledge collateral quickly. Require immediate collateral-prepositioning drills and daily reporting from large banks on available collateral, deposit outflows, and facility capacity.

5. **Disclosure and stigma strategy should be explicit.**
   - Publish aggregate facility usage.
   - Delay borrower-level disclosure to the maximum extent permitted by law.
   - Encourage broad participation by making the program attractive to healthy banks, not only stressed banks.
   - Consider scheduled operations so participation looks routine.

6. **Monetary-policy impact.**
   - If operating in an ample-reserves system, full allotment may be manageable through administered rates.
   - If reserve scarcity or exchange-rate pressures matter, pair the facility with sterilization tools or liquidity-absorbing operations.
   - Communicate separation between liquidity provision and the monetary-policy stance, as the ECB did during its crisis term refinancing operations ([vol4_iss2_38][European Central Bank: Term Refinancing Operations][case_study][2022-07-18T21:02:35Z]).

7. **Exit strategy.**
   - Announce that the facility is temporary and tied to market-functioning indicators.
   - Wind down by shortening maturities, reducing frequency, increasing spreads, narrowing collateral, and eventually returning borrowers to standing facilities.
   - Avoid a hard stop while deposit outflows remain unstable.

# Suggested Framing

I would present the supervisor with three actionable recommendations:

1. **Preferred immediate option:** launch a **fixed-rate full-allotment term lending facility** for all viable banks, using existing standing-facility infrastructure, broad but haircut-protected collateral, and 1- and 3-month tenors. This is the strongest anti-contagion design.

2. **Add-on if securities-loss concerns are central:** create a **high-quality securities term funding sleeve** with longer tenor, potentially up to one year. If collateral is valued at par or haircuts are waived, obtain a fiscal indemnity.

3. **Fallback / transition option:** once panic subsides, shift from full allotment to **regular term auctions** to reduce balance-sheet uncertainty and support orderly exit.

The message should be: **“The central bank will provide term liquidity to the banking system against collateral so that solvent banks can meet depositor and market funding needs without fire sales. This is a systemwide liquidity backstop, not a solvency rescue.”**