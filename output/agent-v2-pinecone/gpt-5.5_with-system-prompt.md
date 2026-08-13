# Summary of core design dimensions

For a systemwide bank run with contagion risk, the supplemental facility should be framed as **liquidity insurance for the banking system**, not as support for the troubled G-SIB. The key design choice is whether the program’s binding constraint is **stigma**, **collateral usability**, **term funding**, or **confidence in unlimited liquidity availability**.

Core dimensions for your supervisor:

| Dimension | Design choice | Practical implication |
|---|---|---|
| **Objective** | Stop contagious runs; prevent fire sales; assure banks can meet depositor and wholesale outflows | Avoid describing the program as rescuing one bank. Announce broad availability and systemic-liquidity purpose. |
| **Eligibility** | All solvent/licensed banks, possibly including domestic branches/subsidiaries of foreign banks | Broad eligibility reduces stigma but may increase political scrutiny if foreign banks use heavily, as in the Fed’s TAF, where US branches of foreign banks ultimately accounted for roughly two-thirds of usage ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18T21:02:50Z]). |
| **Solvency screen** | “Generally sound” institutions; supervisor/central bank can exclude failing or likely insolvent banks | Essential to preserve lender-of-last-resort discipline and avoid disguised solvency support. |
| **Collateral** | Existing standing-facility collateral; high-quality securities; expanded collateral; raw loan pools; government-guaranteed instruments | The more collateral is accepted, the stronger the liquidity backstop—but the greater the valuation, operational, and credit-risk burden. |
| **Valuation / haircuts** | Market value with haircuts; par value for specific HQLA; additional collateral cushion; daily margining | Par valuation is powerful in rate-shock runs but creates subsidy and moral-hazard concerns. Haircuts protect the central bank but reduce usable liquidity. |
| **Term** | Overnight/7-day, 28/84-day, 3/6/12-month, or multi-year collateral swaps | Longer term reduces rollover risk; shorter term preserves discipline and exit flexibility. |
| **Rate** | Policy rate plus spread; auction-determined; OIS plus spread; penalty rate; rate floor to prevent arbitrage | Too high may fail to stop a run; too low risks subsidy and carry trades. |
| **Allotment** | Fixed total via auction; fixed-rate full allotment; uncapped subject to collateral; caps per borrower | Full allotment is strongest for confidence; auctions help control balance-sheet size and reduce stigma. |
| **Disclosure / stigma** | Aggregate reporting only during crisis; delayed borrower-level disclosure where law permits | Stigma can defeat a facility even when terms are attractive. The TAF was explicitly designed to overcome discount-window stigma ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18T21:02:50Z]). |
| **Risk sharing** | Central bank risk only; treasury indemnity; fiscal first-loss protection; resolution-fund guarantee | Government backstop can be decisive if collateral valuation is generous. The BoE SLS had a Treasury indemnity against net losses ([vol2_iss3_23][The United Kingdom's Special Liquidity Scheme (SLS) (U.K. GFC)][case_study][2020-10-08T20:49:21Z]). |
| **Exit** | Sunset date; drawdown window; declining auction sizes; spread that becomes unattractive in normal markets | Exit should be built in at launch to avoid dependence and cliff effects. |

# Program Archetypes

## Option 1: Term Auction Facility model — “stigma-reducing term liquidity auctions”

**Basic design**

- Eligible banks bid for term central bank loans.
- Loans are collateralized using the standing-facility collateral framework.
- Auctions occur on a preannounced schedule.
- Maturities could be 28 days and 84 days, with scope to extend to 3–6 months if stress persists.
- Rate is determined by single-price auction, subject to a minimum bid rate.
- Borrower identities are confidential during the crisis, with only aggregate results disclosed.

**Precedent**

The Federal Reserve’s Term Auction Facility was created after discount-window changes failed to generate sufficient usage because of stigma. It offered 28-day and later 84-day credit to banks eligible for primary credit, used discount-window collateral, peaked at USD 493 billion outstanding, and all loans were repaid ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18T21:02:50Z]).

**Strengths**

- Strong tool if the main problem is **discount-window stigma**.
- Auction participation by many banks makes usage less revealing.
- Preannounced auction sizes allow balance-sheet control.
- Uses existing collateral and operational infrastructure.
- Can be scaled up over time.

**Weaknesses**

- Less suitable if the run is moving faster than auction settlement.
- Fixed auction sizes may underwhelm markets unless very large.
- Individual banks cannot be certain they will receive full liquidity unless the auction is generously sized.
- If a G-SIB is facing immediate outflows, this may need to be paired with bilateral ELA or resolution funding.

**Best use case**

Use if the supervisor wants a **broad, stigma-reducing supplement** while preserving control over aggregate central bank exposure. It is especially useful once the immediate panic has been stabilized and the system needs term liquidity.

**Possible terms for today**

- Eligibility: all solvent banks eligible for standing facilities.
- Term: 28-day and 84-day loans; possible 6-month tranche if stress persists.
- Collateral: standing-facility collateral, prepositioned where possible.
- Rate: single-price auction; minimum rate at policy rate plus modest spread.
- Individual cap: e.g., percentage of auction size or percentage of eligible collateral.
- Disclosure: aggregate auction results only during the program.

---

## Option 2: Fixed-rate full-allotment term refinancing — “whatever solvent banks can collateralize”

**Basic design**

- Central bank announces that all eligible banks can obtain term funding at a fixed rate, subject to eligible collateral and supervisory soundness.
- No fixed aggregate program cap, or a very large announced ceiling.
- Maturities could include 1-month, 3-month, 6-month, and 12-month loans.
- Rate could be policy rate plus a spread, or the standing lending rate for shorter terms and a higher spread for longer terms.
- Collateral could start with existing eligible collateral and be temporarily expanded.

**Precedent**

After Lehman, the ECB moved from variable-rate fixed-allotment operations to fixed-rate full allotment, meaning banks received as much liquidity as they requested against eligible collateral. It also expanded collateral and added longer maturities, with more than EUR 729 billion outstanding at the peak and full repayment ([vol4_iss2_38][European Central Bank: Term Refinancing Operations][case_study][2022-07-18T21:02:35Z]).

**Strengths**

- Strongest broad-based signal: “liquidity will not run out for solvent banks with collateral.”
- Directly addresses systemwide hoarding and rollover risk.
- Reduces uncertainty about whether banks can access enough liquidity.
- Simple message for markets and depositors.

**Weaknesses**

- Central bank balance sheet can expand rapidly.
- If rate is too low, banks may borrow defensively or opportunistically.
- Full allotment may blur monetary-policy and financial-stability operations unless sterilization or reserve-management plans are clear.
- Requires strong collateral valuation and margining capacity.

**Best use case**

Use if contagion is accelerating and the overriding need is a **credible systemwide liquidity firewall**.

**Possible terms for today**

- Eligibility: all solvent banks subject to prudential supervision and standing-facility documentation.
- Tenors: 1 month, 3 months, 6 months; consider 12 months if deposit flight persists.
- Rate: policy rate plus 25–50 bps for 1–3 months; higher spread for 6–12 months.
- Collateral: standing-facility collateral plus temporary expansion to high-quality marketable instruments and selected loan pools.
- Allotment: full allotment against collateral.
- Risk controls: daily valuation, margin calls, supervisory exclusion, concentration limits by collateral issuer/type.
- Exit: sunset after 6–12 months, with review every 30 days.

---

## Option 3: High-quality securities term funding at par — “BTFP-style anti-fire-sale facility”

**Basic design**

- Banks can borrow for up to one year against high-quality securities.
- Eligible collateral is limited to sovereign debt, agency debt, agency MBS, covered bonds, or other central-bank-eligible HQLA.
- Collateral is valued at par or amortized cost rather than depressed market value.
- No haircut, or a minimal haircut, may be applied for the narrowest collateral set.
- Rate is fixed at a term benchmark plus a spread.
- Treasury or finance ministry provides a first-loss backstop if valuation is materially more generous than normal.

**Precedent**

The Fed’s 2023 Bank Term Funding Program was made available to all depository institutions as a supplement to the discount window. It provided advances of up to one year, accepted high-quality securities such as Treasuries and agency debt, valued them at par, applied no haircut, and charged a fixed rate based on one-year OIS plus 10 bps; Treasury provided up to USD 25 billion of credit protection ([vol6_iss4_1][The 2023 Banking Turmoil: Lessons for EU Resolution Authorities][article][2024-12-17T16:25:05Z]).

**Strengths**

- Directly addresses a run driven by unrealized losses on high-quality securities.
- Prevents forced sales of government and agency securities.
- Easy to explain: banks can meet withdrawals without crystallizing mark-to-market losses.
- Narrow collateral set limits credit risk.

**Weaknesses**

- Less helpful for banks whose liquidity need is backed by loans or non-HQLA assets.
- Par valuation is economically generous and may be criticized as masking interest-rate losses.
- If the rate is below market or below reserve remuneration, arbitrage risks arise.
- Does not solve underlying solvency or business-model problems.

**Best use case**

Use if contagion is being amplified by concerns that many banks have **large unrealized losses on high-quality securities** and may need to sell them into stressed markets.

**Possible terms for today**

- Eligibility: all solvent banks.
- Collateral: domestic sovereign securities, central bank bills, agency/official-sector securities, covered bonds, and other top-tier HQLA purchased before a cutoff date.
- Valuation: par or amortized cost, but only for securities expected to pay par at maturity.
- Term: up to 12 months, prepayable after an initial lockout period.
- Rate: one-year OIS or policy-rate expectation plus 10–50 bps; include a floor at reserve remuneration to prevent arbitrage.
- Backstop: finance ministry first-loss protection if no haircut/par valuation is used.
- Anti-abuse: collateral cutoff date; no financing of new carry trades; supervisory certification.

---

## Option 4: Collateral-swap / special liquidity scheme — “turn illiquid but good assets into liquid collateral”

**Basic design**

- Banks swap eligible illiquid but high-quality assets for government bills or central-bank liquid assets.
- Banks then use the liquid assets in private markets or with the central bank.
- The risk of losses on the underlying collateral remains with the banks through haircuts, fees, remargining, and recourse.
- Program has a defined drawdown window and long contractual maturity.

**Precedent**

The Bank of England’s Special Liquidity Scheme let banks and building societies exchange high-quality but temporarily illiquid assets for UK Treasury bills. It was open for nine months, 32 institutions participated, and £185 billion of eligible collateral was exchanged. The BoE applied haircuts, daily remargining, fees, and Treasury indemnity ([vol2_iss3_23][The United Kingdom's Special Liquidity Scheme (SLS) (U.K. GFC)][case_study][2020-10-08T20:49:21Z]).

**Strengths**

- Useful when banks have good assets but cannot fund them in private markets.
- Helps banks obtain marketable collateral without immediate asset sales.
- Can provide longer-term balance-sheet breathing room.
- If structured as a swap rather than outright lending, it may fit better with some legal or operational frameworks.

**Weaknesses**

- Operationally complex.
- May be too slow if collateral must be securitized or structured.
- Less effective for immediate deposit outflows unless paired with cash lending.
- Long maturity can create exit and refinancing cliffs if not managed.

**Best use case**

Use if the systemwide problem is a **market-liquidity freeze in asset-backed, mortgage, covered-bond, or loan-collateral markets**, rather than simply lack of reserves.

**Possible terms for today**

- Eligible borrowers: all solvent banks and building societies/credit institutions.
- Eligible collateral: high-quality securitized assets, covered bonds, sovereigns, agency debt, and potentially performing loan pools if operationally ready.
- Tenor: 1 year, renewable up to 3 years only at central bank discretion.
- Fee: spread over equivalent government repo rate, with minimum fee and usage-based surcharge.
- Risk protection: daily margining, conservative haircuts, substitution rights, treasury indemnity.
- Drawdown window: 3–6 months, extendable in disorderly markets.

---

## Option 5: Enhanced standing-facility overlay — “make the discount window usable at scale”

**Basic design**

- Rather than create a wholly separate mechanism, temporarily enhance the standing facility:
  - longer maturities,
  - wider collateral,
  - simplified access,
  - prepositioning drives,
  - aggregate-only disclosure,
  - possible stigma-reduction communications.
- This can be paired with any of the above options.

**Strengths**

- Fastest to implement if legal authority already exists.
- Uses existing infrastructure.
- Helps banks that need immediate liquidity outside auction dates.
- Encourages banks to preposition collateral and test operational readiness.

**Weaknesses**

- May not overcome stigma if the standing facility is already stigmatized.
- If the market can infer borrowers, usage may remain low.
- May be perceived as inadequate if the run is spreading from a G-SIB.

**Best use case**

Use as a **floor under all other options**. In an active run, the emergency program should not substitute for a fully functioning standing facility; both should operate together.

# Complementary Considerations

## 1. The emergency facility must not be the only response to a failing G-SIB

If the headquartered G-SIB is insolvent or losing franchise confidence, broad liquidity facilities may slow contagion but may not save the institution. The central bank should coordinate with the supervisor, resolution authority, deposit insurer, and finance ministry on:

- ELA for the specific bank, if solvent and collateralized.
- Recovery actions, including asset sales or capital raising.
- Resolution options if the bank is failing or likely to fail.
- Temporary public liquidity backstop in or after resolution.
- Communications to distinguish systemwide liquidity support from institution-specific solvency support.

## 2. Collateral readiness is as important as collateral eligibility

A generous facility can fail if banks cannot operationally pledge assets. The 2023 turmoil highlighted that some banks were not operationally ready to tap the discount window or mobilize collateral quickly ([vol6_iss4_1][The 2023 Banking Turmoil: Lessons for EU Resolution Authorities][article][2024-12-17T16:25:05Z]). Immediate steps:

- Require large banks to submit same-day collateral inventories.
- Preposition collateral at the central bank.
- Conduct live-fire borrowing tests.
- Establish legal documentation and settlement capacity over the weekend.
- Identify collateral trapped in subsidiaries or foreign branches.

## 3. Consider a treasury or fiscal-risk-sharing backstop if terms are generous

If the facility values assets at par, accepts hard-to-value loan pools, or offers long-dated funding, a fiscal indemnity or first-loss layer may be needed. The BoE SLS used Treasury indemnity ([vol2_iss3_23][The United Kingdom's Special Liquidity Scheme (SLS) (U.K. GFC)][case_study][2020-10-08T20:49:21Z]); the Fed’s BTFP had Treasury credit protection ([vol6_iss4_1][The 2023 Banking Turmoil: Lessons for EU Resolution Authorities][article][2024-12-17T16:25:05Z]).

## 4. Price the facility to stop the run, not to maximize penalty

Classic lender-of-last-resort logic argues for a penalty rate, but in a contagious run a rate that is too punitive may discourage use and intensify stigma. A workable compromise:

- Short tenors: policy rate plus modest spread.
- Longer tenors: higher spread.
- Par-value collateral facility: term benchmark plus spread, with a floor at reserve remuneration.
- Usage surcharge if borrowing becomes persistent after stress abates.

## 5. Manage disclosure carefully

Stigma can prevent take-up. The TAF used auctions and delayed borrower-level disclosure to reduce stigma ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18T21:02:50Z]). For a new program:

- Publish program terms immediately.
- Publish aggregate take-up regularly.
- Delay borrower-level disclosure as far as legally permissible.
- Avoid district-level or category disclosures that allow reverse engineering.
- Encourage broad early participation by strong banks.

## 6. Build exit from the start

Options:

- Fixed application window, as in the BoE SLS drawdown window ([vol2_iss3_23][The United Kingdom's Special Liquidity Scheme (SLS) (U.K. GFC)][case_study][2020-10-08T20:49:21Z]).
- Declining auction sizes, as used in TAF wind-down ([vol4_iss2_63][United States: Term Auction Facility][case_study][2022-07-18T21:02:50Z]).
- Rate step-ups after a defined period.
- No new drawings after systemic stress indicators normalize.
- Require borrower exit plans for large or persistent users.

# Suggested Framing

I would present three actionable packages to your supervisor:

## Package A — “Immediate firewall”

Best if contagion is accelerating now.

- Launch a **fixed-rate full-allotment term funding facility** for all solvent banks.
- Offer 1-month, 3-month, and 6-month funds, full allotment against eligible collateral.
- Temporarily broaden collateral beyond the standing facility where operationally feasible.
- Announce aggregate take-up only.
- Coordinate with finance ministry for indemnity if collateral is expanded materially.

**Rationale:** Most credible “no solvent bank need fail for lack of liquidity” message.

## Package B — “Securities-loss run stabilizer”

Best if the run is driven by fear of unrealized losses on high-quality securities.

- Launch a **BTFP-style par-value securities facility**.
- Eligible collateral: sovereigns, agency/official-sector securities, covered bonds, and other top-tier HQLA.
- Term: up to one year.
- Rate: one-year OIS plus spread, with reserve-rate floor.
- Require finance-ministry first-loss protection or formal risk-sharing.

**Rationale:** Stops forced sales and assures depositors that banks can monetize high-quality securities without crystallizing losses.

## Package C — “Stigma and term-market repair”

Best once immediate panic is contained but term funding markets remain impaired.

- Launch **TAF-style term auctions**.
- 28-day and 84-day maturities.
- Use standing-facility collateral.
- Preannounced auction calendar and sizes.
- Broad participation encouraged by pricing and communications.

**Rationale:** Repairs term funding and reduces stigma while giving the central bank balance-sheet control.

## My recommended sequencing

For the present fact pattern—a G-SIB run with signs of contagion—I would recommend:

1. **Announce Package A immediately** as the systemwide liquidity firewall.
2. **Add Package B if unrealized HQLA losses are central to the panic.**
3. **Use Package C over the following weeks** to normalize term funding and reduce stigma.
4. Keep **institution-specific ELA/resolution planning separate** from the broad facility, but coordinate announcements so markets understand that authorities can handle both the G-SIB and the systemwide liquidity shock.