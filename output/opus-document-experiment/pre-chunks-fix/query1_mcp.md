# Query 1 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 3, "get_document": 1}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I now have a thorough, well-grounded basis for recommendations. Let me synthesize these into practical advice.

---

# Recommendation Memo: Responding to a Distressed Systemically Important Insurer

Your scenario closely tracks the 2008 rescue of **American International Group (AIG)**—a ~$1 trillion global insurer that, following losses and a two-to-three-notch ratings downgrade by all three agencies on a single day (September 15, 2008), faced collateral calls and a run on its liquidity, and asked the government for help. The lessons from that episode, and from the broader YPFS survey work on emergency liquidity, drive the following recommendations.

## 1. First, diagnose whether this is truly *just* liquidity—or solvency/viability

Do not take the company's framing ("short-term liquidity crisis") at face value. The survey literature is emphatic on this point:

> "Policymakers should thus take care to not misdiagnose the run on an institution's liquidity as the cause rather than the effect of its problems." (*Ad Hoc Emergency Liquidity Programs in the 21st Century*)

In the AIG case, within two weeks the fast draw-down of the credit line (over $61 billion by October 1) revealed the problem was "more than just a liquidity problem: possibly an insolvency problem. The line between the two is often vague." The right test is not accounting solvency but **viability as a going concern**, inclusive of the support you intend to provide.

**Action:** Rapidly assemble a team to get inside the company (as the FRBNY did with a 25-person team plus outside experts). Because your natural-disaster insurer may not be your primary regulatory charge, you will likely be "learning the company as you execute the rescue"—so start immediately.

## 2. Confirm the systemic-risk case before committing public funds

The government's rationale for saving AIG was not "save every failing firm" but avoiding contagion from a firm whose failure would jeopardize the system. Weigh:
- Size, interconnectedness, and reach (counterparties, reinsurers, policyholders, pension plans, municipalities);
- Retail/policyholder dimension (an insurer's failure can trigger seizures of subsidiaries by insurance regulators, cascading disruption);
- Whether the failure would be a destabilizing "surprise" to already-fragile markets.

If the firm is *not* systemic, the calculus changes and orderly resolution/bankruptcy may be preferable.

## 3. Pursue a private-sector solution first

The Fed's first move was to convene major banks to assemble a private bridge loan (modeled on the 1998 LTCM rescue). It failed for AIG only because Lehman collapsed simultaneously. A private solution—syndicated loan, capital raise, or acquisition by a healthier insurer—avoids taxpayer exposure and moral hazard. **Exhaust this before public assistance.**

## 4. If you must lend, structure liquidity as a *bridge*, not a cure

Emergency liquidity buys time; it does not fix viability. As the survey notes, AHEL interventions "work only as bridges to more structural policy responses"—capital injections, asset purchases, guarantees, restructuring, or merger. Liquidity alone did not stop the AIG run; the collateral drains and rating pressure continued until the November 2008 restructuring (capital injection + asset-purchase vehicles) addressed the *sources* of the cash drain.

## 5. Be very careful with a "penalty rate" and onerous terms

This is perhaps the single most important, counterintuitive lesson. AIG's initial Revolving Credit Facility charged LIBOR + 850 bps (~12%) plus an 8.5% undrawn commitment fee—deliberately "onerous" to limit moral hazard and force quick repayment. **This backfired.** The heavy terms pushed up AIG's leverage, alarmed the rating agencies, and *increased* the risk of the very downgrade the rescue was meant to prevent. The Fed had to cut the rate by 550 bps in November.

> A penalty rate "is liable to instead accelerate the drain on the affected institution's financial resources (and be disfavored by the market and the rating agencies)." (*AHEL* survey)

Because a targeted rescue is already stigmatized and under scrutiny, you don't need a punitive rate to discourage use. **Recommendation: price the assistance to be sufficient and stabilizing—not so expensive it undermines survival. Save moral-hazard/loss-allocation measures for the later structural stage** (equity terms, governance controls), once the firm is stabilized.

## 6. Manage the rating agencies as a central constraint

The downgrade is the trigger of the crisis, so the agencies are effectively a party to your intervention. In AIG, "each of the major ratings agencies called... wanting all types of information," and the entire rescue was ultimately shaped around avoiding further downgrades. As Treasury's restructuring officer put it: "a financial institution cannot operate without at least an investment-grade rating." Evaluate every proposed term from the rating agencies' perspective, and engage them directly and early.

## 7. Do *not* casually impose haircuts on creditors/counterparties

There is a strong temptation to force counterparties to take discounts. The AIG lessons (Millstein) warn this can backfire:
- A distressed-exchange haircut can itself trigger a "D" (default) rating, causing massive collateral calls and deeper illiquidity;
- Counterparties taking losses may themselves need rescue—spreading contagion and *increasing* total government cost;
- Any hint of insolvency accelerates the run.

Haircuts (the ML III counterparties paid at par) drew heavy criticism as a "backdoor bailout," but officials judged that forcing concessions risked triggering the collapse they were trying to prevent—and the government lacked authority to compel them mid-crisis. Weigh the political fairness concerns against these real financial risks.

## 8. Protect taxpayers—and capture the upside

Balance-sheet protection is essential and is compatible with a stabilizing (non-punitive) rate:
- **Collateralize** the loan with substantially all assets, placing the government in a senior secured position (note: senior secured status itself worried AIG's rating agencies, so calibrate);
- **Take an equity interest / warrants** (AIG's "equity kicker" gave the government ~79.9% of equity)—this compensates taxpayers for risk and lets them share the upside. Structure it carefully for legal validity (the AIG Trust device drew litigation). Note the **79.9% ceiling** avoids consolidating the firm onto the government balance sheet under accounting rules;
- **Restrict dividends** and impose governance controls until repayment;
- Consider transactions at **market value** with the firm absorbing first losses (as in the Maiden Lane vehicles).

## 9. Verify legal authority and coordinate

Confirm your institution's legal authority to lend, inject capital, take equity, or guarantee (these were split across the Fed and Treasury/TARP in the US, requiring coordination). Where a natural disaster is the trigger, check whether you have—or need emergency legislative authority for—capital and guarantee tools, not just central-bank lending. **Document decisions, options considered and rejected, and time constraints contemporaneously**—you will face intense oversight.

## 10. Adapt over time, communicate transparently, and plan an exit

The AIG strategy evolved across multiple restructurings as information improved. Build in the flexibility to recalibrate. Communicate terms transparently to markets, policyholders, and legislators, and design an exit (asset sales, equity sell-down) from the outset.

---

### Bottom line

If the firm is genuinely systemic and no private solution is available, provide emergency **liquidity as a bridge**, priced to stabilize rather than punish, backed by collateral and an equity stake to protect taxpayers—**but simultaneously plan the structural fix** (capital injection, removal of loss-making assets, and/or merger) that actually restores viability and calms the rating agencies. Resist punitive terms and reflexive creditor haircuts in the acute phase; they tend to accelerate the run and raise total costs. The AIG rescue, despite heavy criticism, ultimately met its objectives—the firm survived, contagion was averted, and the government recovered its funds plus a $22.7 billion gain—largely because officials adapted away from their initial overly-onerous terms toward a coherent structural stabilization.

Would you like me to draft specific term-sheet parameters, or explore any of the alternative options the Congressional Oversight Panel raised (e.g., a short-term bridge to a pre-packaged restructuring, or a guarantee of a private loan)?