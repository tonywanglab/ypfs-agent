# Summary of core design dimensions

For an emergency, broadly available lending program supplementing standing facilities, the main design choices are:

1. **Objective**
   - Stop contagious liquidity runs and fire sales.
   - Reassure markets that solvent banks can convert eligible collateral into central-bank money.
   - Avoid making the program look like a rescue of one globally significant bank.

2. **Eligible borrowers**
   - Broadly available to all regulated banks, and possibly bank holding companies’ depository subsidiaries, branches of foreign banks, and building societies/credit unions if systemically relevant.
   - Limit to institutions judged **solvent or viable** under supervisory criteria.
   - Pre-clear participants operationally; do not make first-time onboarding the bottleneck.

3. **Collateral**
   - Options range from:
     - Existing standing-facility collateral.
     - Expanded collateral, including high-quality securities, covered bonds, securitizations, and performing loan pools.
     - A narrow, high-quality collateral set valued unusually favorably, if the acute stress is mark-to-market losses on government/agency securities.
   - Haircuts and margin calls are the main central-bank risk mitigants.

4. **Pricing**
   - A classic penalty rate can protect incentives but may worsen stigma and reduce uptake.
   - A modest spread over policy/OIS can encourage broad use while still avoiding a subsidy.
   - Auction pricing can reveal demand but may be too slow or uncertain during a fast run.
   - Fixed-rate full-allotment maximizes reassurance but increases balance-sheet and moral-hazard risks.

5. **Tenor**
   - Overnight liquidity may not stop a run if depositors and wholesale funders fear rollover risk.
   - Crisis precedents commonly used **28 days, 84 days, 3 months, 6 months, or 1 year**.
   - Longer tenors reduce rollover anxiety but increase credit, interest-rate, and political risk.

6. **Size and allotment**
   - A credible systemic backstop should be either very large, scalable, or full-allotment against eligible collateral.
   - A small capped auction may fail if the market interprets excess demand as evidence of systemic stress.

7. **Stigma and disclosure**
   - Stigma is central. Programs should produce many simultaneous users, publish only aggregate data in real time, and make participation normal rather than exceptional.
   - Ex post disclosure requirements should be anticipated in communications.

8. **Exit**
   - Temporary facility with clear review dates, sunset authority, and phase-down triggers.
   - Exit can occur through reduced frequency, shorter maturities, higher spreads, narrower collateral, or declining allotment.

---

# Program Archetypes

## Option 1: Term Auction Facility model — broad term funding by auction

**Core design:**  
A temporary auction facility for solvent banks, using existing standing-facility collateral and infrastructure, but offering term loans at auction-determined rates. Auctions could be daily or twice weekly initially, then weekly or biweekly.

**Illustrative terms**
- Eligible borrowers: all banks eligible for ordinary central-bank credit and judged sound.
- Collateral: same as standing facility, with existing or slightly tighter haircuts.
- Tenor: 28-day and 84-day funds; possibly add 6-month tenor if stress persists.
- Rate: single-price auction with a minimum bid rate, e.g., policy rate/OIS plus a modest spread.
- Size: preannounced auction amounts, with authority to scale rapidly.
- Participation limits: cap individual awards, e.g., 10–20% of auction size, to prevent a few large banks absorbing the facility.
- Disclosure: aggregate auction results only; no same-day borrower-level disclosure.

**Why choose it**
- Good if the main obstacle is **discount-window stigma**.
- Uses existing central-bank lending infrastructure.
- Auction participation by many banks can make use less stigmatizing.
- Central bank retains control over aggregate reserve injection.

**Tradeoffs**
- If the run is accelerating, auctions may be too slow or uncertain.
- If capped auctions are oversubscribed, losing bidders may be interpreted as vulnerable.
- If auction rates rise sharply, the facility can signal stress rather than calm it.
- Requires careful communications so markets see participation as prudent liquidity management, not weakness.

**Relevant precedent**
- The Federal Reserve’s **Term Auction Facility** was created after discount-window rate cuts and term extensions failed to generate sufficient borrowing because of stigma. It offered 28-day and later 84-day credit to banks eligible for primary credit, used discount-window collateral, peaked at USD 493 billion outstanding, and all loans were repaid. It was explicitly designed to provide term funding while avoiding discount-window stigma (“United States: Term Auction Facility,” YPFS case study).

**Best use case:**  
A serious but not yet explosive systemic liquidity squeeze where standing facilities exist but are stigmatized.

---

## Option 2: Fixed-rate, full-allotment term lending facility — maximum systemic reassurance

**Core design:**  
A temporary facility under which all eligible banks can borrow as much as they can collateralize at a fixed rate for a defined term. This is the most forceful “liquidity is available” design.

**Illustrative terms**
- Eligible borrowers: all solvent regulated banks meeting prudential criteria.
- Collateral: existing standing-facility collateral, possibly expanded temporarily.
- Tenor: 3 months initially; 6 months or 1 year if funding markets remain impaired.
- Rate: policy rate/OIS plus a modest spread; potentially above normal standing-facility rate but below stressed market funding costs.
- Allotment: full allotment against eligible collateral and haircuts.
- Size: no ex ante cap, or a very high announced cap with ability to expand.
- Risk controls: haircuts, daily valuation, margin calls, supervisory solvency screen, concentration limits for lower-quality collateral.
- Disclosure: aggregate usage only during the crisis.

**Why choose it**
- Most powerful option for stopping a generalized bank run.
- Removes quantity uncertainty.
- Reduces rollover risk and fire-sale pressure.
- Encourages banks to preemptively borrow rather than wait until desperate.

**Tradeoffs**
- Potentially very large central-bank balance-sheet expansion.
- Can blur monetary policy and financial-stability operations.
- Higher moral hazard than a capped auction.
- Requires strong collateral and legal authority.
- If pricing is too cheap, banks may use it as routine funding rather than crisis insurance.

**Relevant precedent**
- During the global financial crisis, the ECB shifted its term refinancing operations to **fixed-rate, full-allotment**, expanded eligible collateral, and offered maturities up to one year. The program reached more than EUR 729 billion outstanding and all loans were repaid (“European Central Bank: Term Refinancing Operations,” YPFS case study).

**Best use case:**  
A fast-moving systemic run where confidence requires a decisive announcement that liquidity is not constrained.

---

## Option 3: Expanded-collateral term repo facility — targeted at fire-sale pressure

**Core design:**  
A temporary term repo operation that lends against a wider collateral set than the standing facilities, with conservative haircuts and differentiated pricing by collateral type.

**Illustrative terms**
- Eligible borrowers: banks and other prudentially supervised deposit-takers.
- Collateral:
  - Level A: government and central-bank securities.
  - Level B: agency, supranational, covered bonds, high-quality corporate bonds.
  - Level C: senior securitizations, high-quality loan pools, performing mortgages, with steeper haircuts.
- Tenor: 3 months initially; 6 months if stress is persistent.
- Rate:
  - Level A: policy/OIS + small spread.
  - Level B: higher spread.
  - Level C: materially higher spread.
- Allotment: auction-based, fixed-size, or variable-size depending on stress indicators.
- Operational requirement: pre-position collateral and legal documentation.

**Why choose it**
- Addresses the precise problem of banks holding assets that are sound but temporarily illiquid.
- Reduces forced sales into impaired markets.
- Differentiated pricing and haircuts reduce subsidy concerns.
- Can preserve incentives better than full-allotment lending against all assets at one price.

**Tradeoffs**
- More operationally complex than using existing standing-facility collateral.
- Valuation disputes and haircut calibration become critical.
- Accepting loan pools or securitizations increases due-diligence burden.
- If collateral expansion is too broad, it may be interpreted as evidence that banks are asset-impaired rather than liquidity-impaired.

**Relevant precedent**
- The Bank of England’s **Extended-Collateral Long-Term Repo** offered three-month term repo against a broader set of collateral during the GFC. Earlier penalty-rate auctions had no participation, but usage improved after the penalty-rate design was changed and collateral eligibility widened. The facility later reached GBP 180 billion outstanding (“United Kingdom: Extended-Collateral Long-Term Repo,” YPFS case study).

**Best use case:**  
A run driven by funding-market dysfunction and collateral illiquidity, rather than doubts about all bank asset values.

---

## Option 4: Indexed multi-collateral auction — more market-sensitive but harder to launch quickly

**Core design:**  
A more sophisticated version of the expanded-collateral facility. Banks bid for liquidity against different collateral pools, and the auction allocates more liquidity against less-liquid collateral when market stress rises.

**Illustrative terms**
- Eligible borrowers: all banks eligible for central-bank open-market operations.
- Collateral pools:
  - Level A: safest sovereign and central-bank collateral.
  - Level B: high-quality liquid private collateral.
  - Level C: less-liquid but acceptable collateral, including securitizations or loan pools.
- Tenor: 3 or 6 months.
- Pricing: uniform-price auction by collateral pool; spreads indexed to policy rate.
- Supply: variable supply, rising as bid patterns indicate systemic stress.
- Frequency: monthly in normal times, weekly or more frequent in stress.

**Why choose it**
- Good at distinguishing system-wide liquidity stress from a single institution’s distress.
- Provides an embedded price signal: demand for wider collateral reveals stress.
- Can allocate liquidity to where market dysfunction is greatest.
- More incentive-compatible than simple full-allotment.

**Tradeoffs**
- Probably too complex to design from scratch during a weekend crisis.
- Requires prior counterparty education and tested systems.
- If counterparties do not understand the auction, bids may misfire.
- Less suitable as the immediate first announcement in a bank run.

**Relevant precedent**
- The Bank of England’s **Indexed Long-Term Repo** used a multi-good auction with separate collateral sets and uniform pricing. It was designed to provide liquidity insurance while preserving incentives and limiting central-bank risk (“United Kingdom: Indexed Long-Term Repo Operations,” YPFS case study).

**Best use case:**  
A follow-on or standing enhancement after the immediate panic has been contained, not the first line of defense if a G-SIB run is already spreading.

---

## Option 5: High-quality securities term funding at favorable valuation — “BTFP-like” anti-fire-sale backstop

**Core design:**  
A temporary facility for banks to borrow against high-quality securities, potentially valued at par or amortized cost rather than depressed market value, to prevent forced sales of safe assets whose market prices have fallen because of interest-rate movements.

**Illustrative terms**
- Eligible borrowers: all banks and depository institutions.
- Collateral: government bonds, agency securities, central-bank-eligible high-quality securities.
- Valuation: par or amortized cost, or market value with reduced haircuts.
- Tenor: up to 1 year.
- Rate: 1-year OIS plus a spread, or policy rate plus spread.
- Backstop: fiscal indemnity or guarantee if valuation is materially more generous than normal central-bank collateral policy.
- Sunset: strict origination window, e.g., 6–12 months.

**Why choose it**
- Very powerful if the run is caused by unrealized losses on high-quality securities.
- Stops banks from selling safe securities into a falling market.
- Easier to value than loan pools or complex securitizations.
- Can be framed as liquidity support against safe assets, not a credit bailout.

**Tradeoffs**
- Par valuation or no-haircut lending is a subsidy if market values are materially below par.
- Creates interest-rate risk and political risk for the central bank.
- Does not help banks whose liquidity need is backed mainly by loans or lower-quality assets.
- Should probably require fiscal loss protection if collateral valuation departs from conservative central-bank norms.

**Relevant precedent**
- In 2023, the Federal Reserve’s **Bank Term Funding Program** was made available to all depository institutions as an additional program on top of the discount window. It accepted Treasuries, agency debt, and agency MBS, valued collateral at par, applied no haircut, offered advances up to one year, and used Treasury credit protection (“The 2023 Banking Turmoil: Lessons for EU Resolution Authorities,” YPFS article).

**Best use case:**  
A run centered on high-quality securities portfolios with large unrealized interest-rate losses.

---

# Complementary Considerations

1. **Do not let a broad liquidity program substitute for G-SIB resolution planning**
   - If the headquartered globally significant bank is insolvent or nonviable, central-bank lending alone will not restore confidence.
   - The lending facility should be paired with supervisory, resolution, and possibly fiscal options for the troubled bank.

2. **Pair with deposit and liability measures if the run is depositor-led**
   - Broad liquidity may not stop retail or uninsured deposit flight if depositors fear losses.
   - Depending on legal framework, authorities may need to consider temporary deposit guarantee expansion, systemic-risk exceptions, public guarantees, or resolution actions.

3. **Communications should normalize use**
   - Announce that the facility is for the entire banking system.
   - Encourage strong banks to participate.
   - Publish aggregate usage only.
   - Emphasize that lending is secured, temporary, and available to solvent institutions.

4. **Pre-positioning and operational readiness are crucial**
   - A weekend announcement is not enough if banks cannot pledge collateral Monday morning.
   - Require immediate collateral mobilization, legal opinions, payment-system readiness, and supervisory eligibility decisions.

5. **Pricing should be high enough to avoid routine use, low enough to overcome stigma**
   - A severe penalty rate can fail in practice.
   - A modest spread over policy/OIS is often more effective during systemic stress.
   - Different collateral pools can carry different spreads.

6. **Central-bank risk should be explicitly allocated**
   - Normal collateralized lending with haircuts can remain on the central bank’s balance sheet.
   - Unusual valuation concessions, par lending, or weak collateral should receive fiscal indemnity or Treasury loss-sharing.

7. **Monetary policy sterilization may be needed**
   - If the facility causes a large reserve expansion, use central-bank bills, term deposits, reverse repos, or reserve remuneration to preserve rate control.

8. **International coordination matters**
   - A globally significant domestic bank may have foreign branches, foreign-currency funding needs, and cross-border counterparties.
   - Consider central-bank swap lines, coordinated announcements, and supervisory coordination with host authorities.

---

# Suggested Framing

For an immediate recommendation to your supervisor, I would frame the options as follows:

**Preferred emergency option if contagion is already spreading:**  
Launch a **temporary fixed-rate, full-allotment term funding facility** for all solvent banks, using existing standing-facility infrastructure, with 3-month funding, authority to extend to 6 or 12 months, broad but risk-controlled collateral, aggregate-only disclosure, and a modest spread over the policy/OIS rate.

**Backup or complementary option if stigma is the main problem but the run is not yet disorderly:**  
Use a **Term Auction Facility-style program** with frequent single-price auctions, large allotments, 28-day and 84-day maturities, and strict aggregate-only disclosure.

**Targeted option if the stress is driven by unrealized losses on high-quality securities:**  
Add a **BTFP-like high-quality securities facility**, potentially with favorable valuation, but only with fiscal indemnity if valuation is materially more generous than normal collateral policy.

**Medium-term enhancement:**  
Develop a **multi-collateral indexed repo facility** as a permanent or semi-permanent liquidity-insurance tool, but do not rely on it as the first crisis announcement unless it already exists and counterparties know how to use it.

A concise policy line could be:

> “The central bank should announce a temporary, system-wide, collateralized term funding facility available to all solvent banks, designed to remove uncertainty about access to liquidity, reduce stigma relative to standing facilities, and prevent fire sales, while preserving safeguards through supervisory eligibility, haircuts, margining, aggregate disclosure, and a clear exit path.”