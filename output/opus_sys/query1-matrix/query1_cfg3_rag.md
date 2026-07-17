# Query 1 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 6}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I now have comprehensive material—the AIG precedent (nearly identical fact pattern), the AHEL survey's key design decisions, and the important solvency/viability governance debate. Here is my recommendation.

---

## Recommendation: How to Respond to a Distressed Globally Significant Insurer

Your situation closely mirrors the September 2008 rescue of **American International Group (AIG)**—a globally significant insurer that, after a shock (multi-notch downgrades by all three major agencies), faced mass collateral calls and creditor/counterparty runs, an inability to fund short-term obligations, and imminent bankruptcy. The corpus offers a well-developed playbook, and equally important, a set of cautionary lessons. Below is what I recommend, and why.

### 1. First diagnose: is this genuinely a liquidity problem, or a solvency/viability problem in disguise?

This is the single most important threshold decision. The *Ad Hoc Emergency Liquidity Programs* survey warns crisis-fighters "to not misdiagnose the run on an institution's liquidity as the cause rather than the effect of its problems." When a specific systemically important firm is being run on, the source is "almost never some contagion of illiquidity only, but rather the market's fears about the firm's viability as a going concern."

- Do **not** ask only whether the firm is accounting-solvent at a point in time; that is impractical to judge in a fast-moving crisis and can be misleading. Instead assess **viability as a going concern**, inclusive of the effect of the support you intend to provide (BIS CGFS 2017; Dobler et al. 2016).
- The corpus offers a stark cautionary tale: **Ireland (2008)** issued a blanket guarantee based on the belief that its banks faced only a liquidity issue, when in fact they were insolvent. The response ended up costing ~40% of GDP. Get the diagnosis right before committing public resources.
- Paul Tucker's "Fundamental Constraint" argues that an independent **central bank should not lend to a firm it knows to be fundamentally bust**—because doing so simply lets short-term creditors escape while leaving long-term creditors and taxpayers worse off. If the firm is doomed, this becomes a *fiscal/resolution* decision for the elected government, not a central-bank liquidity operation.

**Practical point for an insurer:** Note the AIG lesson from Eric Dinallo—insurers must be assessed by people who understand insurance. The core question is solvency *and* long-term policyholder obligations ("money keeps coming in so you can pay out 30 years from now"). Involve the insurance supervisor, not just banking authorities.

### 2. If viable: provide liquidity as a *bridge*, not as the whole solution

The recurring lesson is that ad hoc emergency liquidity (AHEL) works **only as a bridge that buys time** for the structural measures that actually fix the problem—capital injections, guarantees, balance-sheet restructuring, a merger, or an orderly resolution. Even fully covering all maturing obligations did **not** stop runs in the surveyed cases; runs continued until viability was addressed.

- Confirm systemic importance. This is a necessary condition for support. For an interconnected global insurer, "too interconnected to fail" (as with Bear Stearns) may matter more than sheer size—consider the CDS/counterparty web, securities-lending exposures, and contagion channels.
- **Size the facility to the actual outflows.** With AIG, the collateral-call and securities-lending drains ballooned from ~$20bn to ~$80bn within a week; the Fed's initial $85bn Revolving Credit Facility (RCF) plus a separate ~$37.8bn Securities Borrowing Facility were needed to cover both channels. Diagnose *all* the run channels (collateral calls on derivatives, securities-lending cash-collateral redemptions, commercial paper, etc.).

### 3. Design terms that help the firm survive—resist over-punitive pricing

This is the corpus's most counterintuitive and important design lesson, and it comes directly from the AIG mistake.

- **Rethink the "penalty rate."** Of Bagehot's dictum ("lend freely, against good collateral, at a penalty rate"), the survey concludes that for a single targeted institution "only 'lend freely' survives in practice." A penalty rate on a firm already being run on will *accelerate* the drain, be disfavored by markets and rating agencies, and can "make survival of the institution (and repayment) less likely."
- **The AIG cautionary example:** The Fed initially priced the RCF at LIBOR + 850 bps—a premium even over the private consortium's proposed rate—to limit moral hazard. AIG's position kept deteriorating and the punitive terms *portended further downgrades*. The Fed had to cut the rate (first by 550 bps) alongside a capital injection. Latvia–Parex repeated the same error and also had to lower rates. **Don't try to solve all the moral-hazard problem inside the liquidity facility**—save punitive/costly terms for the later structural stage once the firm is stabilized.
- **Collateral flexibility.** In AHEL, collateral sufficiency is interpreted "as flexibly as necessary" to get liquidity to the firm. Where a forthcoming measure (capital injection, merger with a healthy acquirer) provides added security, you can rely less on hard collateral—as the BoE did for RBS/HBOS and the SNB did for Credit Suisse (once UBS became liable). **But** heed the Cyprus–Laiki caution: relying on a rescue package (an MoU) that has *not yet been finalized* is dangerous—Laiki went into resolution before its recapitalization MoU was executed.

### 4. Tap the insurer's own resources and private-sector options first

- **Pursue a private solution before committing the public balance sheet.** With AIG, authorities first tried to organize a private syndicated loan (JPMorgan/Goldman); it collapsed only because of the concurrent Lehman failure. Even a failed private effort is useful—the Fed used the consortium's term sheet as the skeleton for the RCF. (But modify commercial terms to serve *public* policy goals.)
- **Consider ring-fenced subsidiary liquidity, but understand the limits.** New York regulators explored letting AIG borrow ~$20bn of excess liquid assets from its insurance subsidiaries. This was dropped once it became clear the problem was far larger than a brief cash-flow gap—and because tapping insurance-subsidiary assets threatens policyholder protection. Protect the regulated insurance entities and their policyholders; the problems typically originate at the holding company / non-insurance units (as with AIG Financial Products' CDS book and the securities-lending program).

### 5. Sequence the structural measures and plan the exit

- Solvency "is ultimately an equity problem and *cannot be solved* simply by lending." If the firm is viable but undercapitalized, the liquidity bridge must be paired with a **capital injection, guarantee, restructuring, sale/merger, or orderly resolution**—decisions that require *fiscal* authority (i.e., government/legislature), not the central bank alone.
- Attach conditions and consequences appropriate to a rescue (as governments did with equity stakes/warrants and management/business-model changes in the GFC), but place them at the structural stage rather than loading them onto the emergency liquidity line.
- Observe the "no creditor worse off" norm and the separation-of-powers principle: an independent central bank can be lender of last resort, but capital-provision-of-last-resort is a fiscal choice requiring democratic accountability.

### 6. Governance, roles and communication

- **Clarify agency roles up front.** The Northern Rock episode showed that split authority (BoE as LOLR, FSA as supervisor, Treasury for fiscal) caused delay and missteps. Coordinate the central bank, the insurance supervisor, the resolution authority, and the treasury with clear decision rights.
- Manage disclosure deliberately. Authorities have used structures (e.g., the BoE's off-balance-sheet trusts for HBOS/RBS) to manage confidentiality, and considered stigma effects. Weigh the trade-off between transparency and adding to the run.

---

### Bottom line

1. **Diagnose viability, not just point-in-time solvency**—involve the insurance supervisor. If the firm is fundamentally bust, this is a resolution/fiscal decision, not a liquidity operation.
2. **If viable and systemic, provide a liquidity bridge sized to *all* run channels**, but treat it explicitly as a bridge—not a fix.
3. **Do not over-penalize the terms**; the AIG and Parex experiences show punitive rates trigger further downgrades and undermine survival and repayment. Manage moral hazard at the later structural stage.
4. **Exhaust private-sector and (limited) internal options first**, and protect policyholders/regulated subsidiaries.
5. **Pair the bridge with a concrete, near-certain structural plan** (recapitalization, guarantee, merger, or orderly wind-down) authorized by the fiscal authority, with a defined exit.

The single biggest risk, per the corpus, is misdiagnosing a solvency problem as mere illiquidity (Ireland) or over-punishing a viable firm into failure (AIG's initial terms). Avoid both, and use the liquidity line to buy the time needed to implement the real, structural solution.

*Primary sources: "Ad Hoc Emergency Liquidity Programs in the 21st Century" (survey); "Broad-Based Emergency Liquidity Programs" (survey); AIG Modules A & B case studies; Lessons Learned: Eric Dinallo; Tucker, "Solvency as a Fundamental Constraint on LOLR Policy"; Ireland CIFS case studies.*