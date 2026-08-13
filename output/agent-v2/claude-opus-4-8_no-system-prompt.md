I now have a comprehensive grounding in the Yale Program on Financial Stability's survey of 33 broad-based emergency liquidity (BBEL) programs. Below is an options memo synthesizing the key design decisions and historical lessons, tailored to your situation.

---

# Options Memo: Emergency Lending Program (Broad-Based Liquidity Facility)

## Situation as I understand it
- A globally significant bank headquartered in your jurisdiction is experiencing a run.
- There are early signs of contagion to other banks.
- You want a **broad-based** facility (available to all banks), as a **supplement** to existing standing facilities (discount window / Lombard / repo, etc.).

This places you squarely in the "acute phase" of a crisis, where the YPFS survey finds the priority is to **arrest runs and prevent fire sales**, fast, by protecting fragile bank liabilities — not to make solvency judgments. The survey's central trade-off you'll be balancing throughout is **moral hazard vs. stigma**.

---

## Threshold framing (informs every option below)

**1. Acute vs. chronic phase.** You are in the acute phase. The survey is emphatic: emergency liquidity arrests *liquidity* problems; it **cannot fix solvency** (an equity problem requiring fiscal tools). Don't try to impose a strict solvency test in the heat of the run — the survey calls this "doomed to failure" because there's no time, valuations are distorted by fire-sale prices, and it stigmatizes borrowers. (Note the UK Discount Window Facility's on-the-day solvency/viability tests led to *zero usage*.)

**2. Speed via existing infrastructure.** Across 33 cases, the recurring lesson is that **relying on existing authorities, programs, and administrative frameworks is the fastest, most credible path.** 21 of 33 programs were built off existing facilities; this lets you reuse known collateral schedules, haircuts, and counterparty relationships and deploy in days, not weeks.

**3. This is usually "part of a package."** When liquidity constraints persist, central banks typically deploy *multiple* BBEL programs (different maturities, collateral classes, participant groups), often alongside **liability/account guarantees** in the acute phase. Given you already see contagion, plan for a package, not a single facility.

---

## The Options

### Option A — Enhance/expand the existing standing facilities (the "first-movement" option)
The quickest action. Adjust the standing facilities themselves and announce it as a deliberate emergency measure.

Concrete levers (all drawn from real cases):
- **Lower the borrowing rate** and narrow the penalty spread.
- **Lengthen maturities** (e.g., from overnight to 1–3 months) — Hong Kong 2008 (HKMA) extended its discount window maturity from overnight to up to three months and waived its 5% penalty.
- **Broaden eligible collateral** (e.g., add high-quality foreign-currency assets, as HKMA did).
- **Increase frequency and capacity** of operations. The ECB's 2007 same-day fine-tuning operations calmed the euro money market within a week.

**Pros:** Fastest; uses existing authority and plumbing; "first-movement" actions are often very effective at early signs of stress.
**Cons / caution:** Standing facilities (especially the discount window) **carry severe stigma** — the defining failure mode. In August 2007 the Fed lowered the primary credit rate but DW borrowing stayed limited *because of stigma*; banks migrated to FHLB advances instead. This is why a *new, differently-branded* facility (Option B) often works better.

---

### Option B — A new auction-based term facility (the lead recommendation for stigma management)
Model: the **US Term Auction Facility (TAF)** and the ECB's **Term Refinancing Operations** and the BoE's **Extended-Collateral Long-Term Repo / Indexed Long-Term Repo**.

The TAF was explicitly designed to deliver discount-window-type funding *without* the stigma. Key destigmatizing features the survey identifies:
- **Auction format** — sets a market-determined rate, not an obvious "penalty"; banks don't signal distress merely by bidding.
- **Many participants** at once — if identities ever leak, many names emerge together.
- **Individual participation caps** (TAF: no bidder >10% of an auction) — so the facility can't be read as a lifeline for one desperate firm, and protects anonymity.
- **Delayed settlement** (TAF settled ~3 days later) — inconsistent with the needs of a failing institution, deterring adverse selection.
- **Minimum bid rate** below interbank market rate (LIBOR) but above OIS — a low, non-punitive floor that still avoids arbitrage.

**Pros:** Best-in-class stigma mitigation; the survey's restated Bagehot dictum is built around "rates set by auction." Highly used and well-regarded.
**Cons:** Takes somewhat longer to operationalize a *novel* mechanism — but you can run it on your existing collateral/haircut schedule (TAF used the discount window schedule) to compress the timeline.

---

### Option C — A collateral-swap facility (lend government securities/cash against impaired assets)
Model: **BoE Discount Window Facility / ECTR** (gilts for collateral); **Norway Covered Bond Swap**; **Canada Term Loan Facility / Term PRA-PS**.

If the run is being driven (or worsened) by certain **assets becoming illiquid as collateral**, this targets that directly — banks swap illiquid assets for cash or government securities at term.

**Pros:** Directly rehabilitates impaired collateral; can be calibrated to the specific asset class under stress.
**Cons:** Narrower collateral focus can limit usage if mis-targeted. (BoE's DWF, with high penalty pricing and on-the-day solvency tests, was *never drawn* — a cautionary tale.) Watch the monetary-policy transmission point: BoE had to sterilize ELTR's reserve injection by issuing BoE bills.

---

### Option D — Full-allotment, fixed-rate facility (the "break the glass" escalation)
Model: **ECB October 2008** (switched TROs to fixed-rate, full-allotment — "the most significant non-standard measure"); **Fed TAF after Lehman** (moved to effectively full allotment); **BoE CTRF in March 2020** (fixed-rate, full-allotment, unlimited).

Here the central bank sets a rate and gives every bidder whatever they request. The survey notes this shift away from penalty pricing was observed **only in the most critical circumstances**.

**Pros:** Maximum reassurance — "financing will be available against good collateral"; powerful announcement effect; removes the rationing that can intensify a panic.
**Cons:** Strongest moral-hazard signal; can signal the situation is worse than it is. Reserve it for if/when the contagion accelerates despite Options A–C.

---

## Cross-cutting design decisions (apply to whichever option(s) you choose)

| Decision | Survey guidance for the acute phase |
|---|---|
| **Eligible participants** | Start with your existing supervised banks (you have the institutional knowledge). Extending to NBFIs is high-risk due to information asymmetry — survey view: banks get generous access; NBFIs face "constructive ambiguity." Decide early whether to include **foreign-bank branches/subsidiaries** — TAF did (they were ~65% of usage); Greece ELA did not, which caused problems. |
| **Solvency/viability tests** | Avoid strict on-the-day tests in the acute phase (UK DWF → zero usage). Lend against good *collateral* rather than gating on solvency. |
| **Rates** | Prefer **auction-set rates** (penalty achieved with minimum stigma). If fixed-rate, beware overpricing → stigma/non-use (BoE's 2007 penalty-rate term repos got *no takers*; reformatted without the penalty → heavy usage). |
| **Collateral & haircuts** | Reuse your standing facility's schedule for speed and fairness; build in **administrative flexibility to widen collateral** later (8 of cases expanded collateral mid-program). Consider extra haircuts for FX-denominated or own-name collateral. |
| **Program size** | You generally need not pre-announce an aggregate cap. Retain flexibility to **increase auction sizes in response to demand** — a "very powerful tool" in the acute phase (BoE, ECB, Fed all did this). |
| **Individual limits** | Use caps (e.g., 10%) for both moral hazard and anonymity/stigma protection. |
| **Stigma strategy** | Many participants + auctions + caps + delayed settlement. **Minimize borrower-level disclosure during the acute phase**; disclose in aggregate, with borrower-level detail only on a delayed basis after markets calm (revealed RFC borrowers and the 1890 NYCH disclosures triggered runs/failures). |
| **Communication** | Be clear, consistent, confident; announce **close to operational readiness** (do the back-office work first). A credible announcement alone can calm a run (UK 1866; Y2K SFF — no options ever exercised). Inconsistent messaging backfires (Hong Kong 1965). |
| **Exit strategy** | Build in a natural exit: penalty/premium pricing that becomes unattractive as markets normalize, and/or an expiration date, and/or wind-down by shrinking auction size/frequency. Consider whether to **transition a successful facility into your standing framework** later (BoE did this with DWF/ILTR; HKMA kept 2 of 5 measures). |
| **Legal authority** | Confirm now whether you act under regular authority, a pre-positioned emergency authority, or need new legislation. The survey strongly warns that legislative routes are slow and erode confidence — review your "arsenal" of authorities in quiet times. |

---

## My recommendation in brief
Given an active run on a G-SIB plus emerging contagion:

1. **Immediately (Option A):** Adjust standing facilities (rate, maturity, collateral, frequency) as a "first-movement" signal — but recognize stigma limits their reach.
2. **In parallel, lead with Option B:** Stand up a **new auction-based term facility** on your *existing* collateral/haircut schedule, with broad bank eligibility, individual caps, delayed settlement, and minimal individual disclosure — this is the survey's modern best practice for delivering liquidity broadly without stigma.
3. **Add Option C** if a specific impaired collateral class is driving the run.
4. **Hold Option D (fixed-rate, full-allotment) in reserve** to escalate if contagion accelerates.
5. **Coordinate** with the fiscal authority on a likely **liability/account guarantee** (acute-phase complement) and, if solvency concerns surface, recapitalization tools (chronic phase) — emergency lending alone cannot solve solvency. Also consider **cross-border coordination** with peer central banks (e.g., FX swap lines), given the bank's global significance.

**Restated dictum the survey lands on (a useful north star):** *In the acute phase, lend freely and broadly against good collateral, at rates set by auction, taking care to avoid disclosing details about individual borrowers* — notably with **no** solvency gate.

---

*Primary source: Wiggins, Fulmer, Feldberg & Metrick, "Broad-Based Emergency Liquidity Programs," Yale Program on Financial Stability Survey (2022/2023), synthesizing 33 case studies.* I can go deeper on any single model — e.g., pull the full TAF, ECB TRO, BoE ECTR/ILTR, or Norway Covered Bond case studies — to draft detailed term sheets for whichever option(s) you want to advance. Would you like me to do that next?