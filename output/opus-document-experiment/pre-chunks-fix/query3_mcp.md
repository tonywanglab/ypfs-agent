# Query 3 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 4}

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

I now have a strong grounding in the corpus. Let me synthesize a response.

## First, diagnose before you act

The corpus lessons are unanimous on one point: **do not misdiagnose the problem.** As the surveys of both broad-based and ad hoc emergency liquidity programs stress, "policymakers should take care to not misdiagnose the run on an institution's liquidity as the cause rather than the effect of its problems." Paul Volcker and Mervyn King are both quoted to the same effect: "Almost every financial crisis starts with the belief that the provision of more liquidity is the answer, only for time to reveal that beneath the surface are genuine problems of solvency" (King 2016).

Your scenario has a distinctive feature that matters enormously for the diagnosis. The originating shock is **a real, permanent repricing of assets** — a Chinese competitor has plausibly destroyed a chunk of the fundamental value underpinning U.S. AI-company equities. This is not a rumor-driven panic on assets that are fundamentally sound; it is (potentially) a genuine solvency event. That distinction dictates almost everything about the right response, because the corpus is clear that **"Solvency is ultimately an equity problem and cannot be solved simply by lending"** (Broad-Based Emergency Liquidity survey).

So the first task is triage: figure out which of two very different situations you are in.

## The two-phase framework the corpus recommends

Nearly every survey frames crisis response as **acute vs. chronic phases**:

- **Acute phase:** The system has an *obvious liquidity problem* (runs, funding withdrawals, margin calls) but underlying solvency is *hard to judge in the heat of the moment*. Here, act fast and prioritize protecting fragile short-term liabilities. Do not let moral-hazard concerns stop you from arresting runs and preventing fire sales.
- **Chronic phase:** Liquidity pressure has eased but solvency problems remain. Here, you shift to influencing the banks themselves — recapitalization, restructuring, resolution — using fiscal tools, and moral-hazard concerns get more weight.

## What the government should do — sequenced

### 1. In the acute phase: break the fire-sale doom loop with liquidity

The exact "vicious dynamic" you describe is documented in the Fed's crisis-response case study: *"Asset price declines lead to margin calls. Some highly leveraged firms are unable to meet these calls. Dealers respond by liquidating collateral. This puts downward pressure on asset prices... A vicious circle ensues of higher haircuts, fire sales, lower prices, higher volatility, and still lower prices, and financial intermediaries start to break as a liquidity crisis potentially leads to insolvency when assets are sold at fire sale prices."*

To halt this, the central bank should act as **lender of last resort** following the modernized Bagehot dictum: *"In the acute (panic) phase of a crisis, a lender of last resort should lend freely and broadly against good collateral, at rates set by auction, taking care to avoid disclosing details about individual borrowers."* Key points from the Broad-Based Emergency Liquidity survey:

- **Do not impose a strict solvency test during the acute phase.** "Defining what solvency means in the midst of the panic would be difficult and even counterproductive." You cannot value AI-company collateral in real time while prices are collapsing.
- Consider **broadening collateral eligibility** and the class of eligible participants, since the affected exposures may sit in nonbanks. A market-liquidity program (à la the TSLF, which let dealers swap illiquid collateral for Treasuries) can be used to prevent cascading fire sales in the specific stressed markets.

### 2. Consider guarantees to stop runs on funding

If short-term creditors of the affected intermediaries are running (not just depositors — modern institutions rely heavily on wholesale funding), account or debt guarantees may be needed. The Blanket Guarantees survey warns, though, that **guarantees "cannot address underlying problems without complementary liquidity support and restructuring measures,"** and that credibility depends on the guaranteed amount relative to fiscal resources. In the acute phase, don't let moral-hazard measures (e.g., executive-pay restrictions) discourage participation, but *do* use light-touch guardrails like interest-rate caps and marketing bans.

### 3. Crucially — recognize this may be a solvency problem, not a liquidity one

Here your scenario diverges from a classic panic. If the collateral has *permanently* lost value because the technology thesis has genuinely changed, then liquidity buys time but **cannot cure the wound**. As the Ad Hoc Emergency Liquidity survey concludes, in *no* case did liquidity provision alone cure a run; its value was in "buying time to implement the more structural responses necessary to address an institution's viability concerns." So liquidity must be explicitly understood as a **bridge to a solvency fix**, not the fix itself.

### 4. In the chronic phase: triage viability, then recapitalize the viable

Once the acute panic is contained, move to the solvency question using the Broad-Based Capital Injection playbook:

- **Triage for viability, not just accounting solvency.** Assess whether each intermediary can be a going concern *after* the AI repricing. During the acute phase, broad availability is acceptable (cf. US CPP); during the chronic phase, use rigorous, credible **stress testing** (cf. the 2009 US CAP/SCAP) to size capital needs against a scenario that assumes the AI-driven asset losses are real.
- **Size it correctly.** The surveys repeatedly warn that too-small injections fail and can create "zombie" lending; but they must be credibly sized or they won't calm counterparties.
- **Require private capital first where possible** (cf. Piraeus, Bank of America), and use terms that encourage repayment and private recapitalization.
- **Resolve the nonviable.** For intermediaries that are genuinely insolvent because their AI collateral is permanently impaired, the chronic phase makes it "more feasible to allow weak banks to fail or to resolve them through a sale or merger," since contagion fears have receded.

### 5. A caution on what *not* to backstop

The "Black Swans" resilience article draws a sharp and relevant line: *"Bailouts occur in crises, which are the realization of systematic risk, whereas events stemming from non-systematic risks are not bailed out."* Systemic policies "do not prevent the harms that can arise from routine events such as firm bankruptcies... as part of traditional Schumpeterian creative-destruction dynamics."

This is a critical judgment for your scenario. A crashing equity price for AI companies is, by itself, **market repricing in response to a genuine competitive/technological shock — arguably exactly the kind of creative destruction the government should *not* insulate.** The government's proper concern is not the AI companies' stock prices or their creditors' losses per se; it is **whether the transmission into financial intermediaries threatens the system's critical functions.** The goal, in the article's terms, is to keep the financial system "away from the cliff" and preserve its critical functions — not to reverse the AI companies' losses or protect their lenders from a bad credit judgment.

## Summary

1. **Diagnose first.** Determine whether you face a liquidity panic on sound assets or a genuine solvency shock from permanently repriced AI collateral. This scenario likely contains real solvency loss.
2. **Acute phase:** Lend freely against good collateral, broadly, without a strict solvency test, to break the fire-sale/margin-call doom loop; add targeted market-liquidity support and, if funding runs, guarantees — while treating all of this as a *bridge*, not a cure.
3. **Chronic phase:** Use credible stress tests to triage viability, recapitalize the viable (private capital first), and resolve or merge the nonviable.
4. **Don't over-insure the shock itself.** Protect the *system's functions*, not the AI companies' equity value or their lenders' bad bets. Absorb the losses where they belong once systemic transmission is contained.

One caveat: the corpus is drawn from historical banking-centric crises. Your scenario's transmission runs through *equity collateral* and possibly *nonbank lenders*, so you'd want to confirm the affected intermediaries are within (or can be brought within) your liquidity, guarantee, and resolution toolkits — the "regulatory perimeter" problem the Black Swans article flags. If they aren't, that gap itself becomes a first-order policy problem.