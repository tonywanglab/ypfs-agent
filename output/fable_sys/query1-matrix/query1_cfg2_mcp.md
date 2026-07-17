# Query 1 — mcp

Model: anthropic/claude-fable-5 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 6}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

Based on the corpus—particularly the Yale Program on Financial Stability's survey of 22 ad hoc emergency liquidity (AHEL) interventions and the AIG rescue case studies, which are the closest analogue to your situation—here is my recommendation.

## 1. First, diagnose correctly: this is probably not "just" a liquidity problem

The most important lesson from the AHEL survey (*Ad Hoc Emergency Liquidity Programs in the 21st Century*, 2025) is that when markets run on a specific institution, **the liquidity crisis is usually the symptom, not the cause**. The market is signaling doubt about the firm's *viability as a going concern*. As Paul Volcker put it: "there are very few liquidity crises that aren't related to a solvency question." In **none of the 22 surveyed cases did liquidity provision alone stop the run**—even when assistance was sized to cover all possible outflows.

A cautionary tale directly on point: in September 2008, New York's insurance regulator arranged for AIG's parent to borrow $20 billion of excess assets from its insurance subsidiaries—a plan "based on the false belief that AIG was experiencing a brief cash flow problem." It collapsed within days once the true scale of the problem emerged.

**So before committing anything, your authorities must rapidly assess:**
- Are the disaster losses a genuine one-off against an otherwise sound business model, or do they expose chronic under-reserving, underpricing, or balance-sheet weakness?
- Is the company **viable**—either now, or with the interventions you're prepared to make? Note that modern crisis-fighters assess *viability*, not point-in-time accounting solvency, which is nearly impossible to measure mid-crisis anyway.
- Is it truly **systemically important**? Size is not the only test—interconnectedness (reinsurance chains, derivatives, securities lending, guarantees to pension products) and contagion risk matter. This was always a necessary condition for AHEL support in the cases surveyed.
- Do not take the company's own numbers at face value. Don Kohn's lesson from AIG: management "didn't have a very good sense of their own liquidity needs." Embed supervisors immediately and build your own picture, including insurance-specific channels (policyholder surrenders, collateral calls triggered by the downgrade, securities lending programs run out of the subsidiaries—the AIG sec-lending program was a major hidden drain).

## 2. If systemic and viable (or you can make it viable): provide liquidity **as a bridge, announced as part of a package**

Emergency liquidity should be extended only if you have deemed the firm viable **or you are committed to making it viable** through follow-on measures—most commonly a government capital injection, or a merger with a stronger institution. The Ad Hoc Capital Injections survey confirms the pattern in reverse: essentially every ad hoc capital injection studied was accompanied by liquidity support; liquidity buys time, capital or a merger cures.

Design lessons for the liquidity facility itself:

- **Lend freely; don't try to manage moral hazard through the facility's terms.** Punitive rates and steep haircuts accelerate the firm's deterioration, worry rating agencies, and often have to be loosened later (as happened with AIG's Revolving Credit Facility, which was restructured within weeks). Save the tough terms for the structural phase.
- **Be flexible on collateral**, and count forthcoming measures as protection—e.g., the Bank of England lent to HBOS/RBS against the impending Lloyds merger and recapitalization; the SNB's Credit Suisse loans were de-risked by the UBS takeover.
- **Tie duration to outcomes, not arbitrary dates.** The AIG facility's initial two-year term had to be extended to five years to allow orderly asset sales. Communicate that support will remain until the firm is stabilized—premature expiry reignites the run. (But note the Cyprus/Laiki caution: don't lend against a rescue package that isn't actually agreed.)
- **Confirm legal authority early.** In AIG's case, only the Fed's emergency authority could reach a nonbank; your central bank's standing facilities likely exclude insurers, so identify now which entity (central bank, treasury, or both) can lend, inject capital, or guarantee.

## 3. Move quickly to the structural fix—and put the moral-hazard terms there

This is where taxpayers are protected and shareholders bear the cost:

- **Take substantial equity and impose dilution.** The government took a 79.9% stake in AIG; as trustee Chester Feldberg noted, shareholders "may have lost 80 percent of the value, but if the government hadn't stepped in, they would have lost 100 percent," and the stake gave government the leverage to protect the taxpayer investment and discourage future firms from seeking help except in dire circumstances.
- **Replace management** if warranted (AIG's CEO was required to step down) and require a credible restructuring plan—asset sales, exit from the problem business lines, de-risking.
- **Explore a private solution or merger first and in parallel**—but move fast if it fails, as the private consortium for AIG did within 24 hours.

## 4. Insurance-specific safeguards

- **Ring-fence the regulated insurance subsidiaries and protect policyholders.** Structure support at the holding-company level where possible, and coordinate closely with the insurance regulator(s)—in AIG's case, fragmented oversight (state regulators plus a holding-company regulator that admitted it was "wholly unprepared") let risks build unseen. Millions of retail policyholders were a key reason bankruptcy was deemed more systemic than Lehman.
- **Resist the temptation to strip subsidiary assets to fund the parent** (the failed NY plan) unless you are certain the problem is small and temporary.

## 5. If the firm is *not* viable or not systemic: don't lend

Lending to a nonviable firm risks losses, stigma, drift into fiscal policy, and lost credibility. In that case, use (or improvise) an orderly resolution: protect policyholders through guarantee schemes and portfolio transfers, impose losses on shareholders and subordinated creditors, and consider a good-firm/bad-firm split. The post-GFC resolution survey emphasizes that resolution must *eliminate* uncertainty—by closing, recapitalizing, or merging the institution.

## 6. Communicate deliberately

Sarah Dahlgren's lesson from AIG: the authorities "completely underestimated" the public backlash. Announce the liquidity support and the path to the structural solution together, explain why the firm is systemic, be transparent about terms and taxpayer protections, and never assume the public understands your motives. Also guard against leaks—in the Swiss Volksbank case, a leak the day before the announcement triggered a deposit run.

**Bottom line:** Agree to help only if the company is systemically important and viable (or can be made so). Provide generous, flexible liquidity immediately—but only as an explicit bridge to a capital injection, restructuring, or merger announced as quickly as possible, with shareholders diluted, management accountable, policyholders ring-fenced, and the taxpayer holding equity upside. Liquidity alone will not stop this run.