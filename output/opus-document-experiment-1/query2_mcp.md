# Query 2 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 7}

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

I now have a comprehensive evidence base. Let me synthesize a policy recommendation grounded in these historical cases.

---

# Should the government intervene? Yes — but the tool must match the problem, sequenced carefully

## 1. Diagnose the problem: this is a classic "confidence contagion" driven by unknown exposures

Your scenario has a specific and dangerous signature. The precipitating shock (the private-debt fund loss) has real, fundamental linkages to *two* banks — but the sector-wide run is being driven by something else: **uncertainty about who else is exposed.** The crisis literature draws exactly this distinction. Contagion has two channels (Dornbusch, via the *Lehman Brothers Bankruptcy H* case study):

- **Spillovers** — losses transmitted through genuine exposures (your two regional banks).
- **Investor-directed / confidence contagion** — runs that "cannot be linked to any real or fundamental interconnections" but arise because, "when in doubt about a firm's stability, it is easier for investors to abandon that firm rather than figure out its true situation."

Hal Scott's formulation, quoted in the same case, describes your situation almost exactly: *"there could be a run on … banks because funders fear that all such banks could be in trouble."* This is precisely what happened when the Reserve Primary Fund "broke the buck" in 2008 — a *$38 million* loss on a small fund triggered a ~$230–439 billion run across money-market funds because investors couldn't tell which funds held bad paper. Michael Silva's *Lessons Learned* is blunt: economists dismissed it as "one small little fund," but "that small, little fund … turned out to be when the dyke almost broke."

**Implication:** Because much of the run is confidence-driven rather than fundamentals-driven, it is both *dangerous* (it will hit sound banks) and *addressable* (removing the incentive to run can stop it without validating the panic).

## 2. The strategic frame: separate the acute phase from the chronic phase

The *Blanket Guarantees Survey* offers the organizing principle. Think of the response in two phases:

- **Acute phase:** "runs on banks are easy to spot" but "the underlying solvency of the financial system is difficult to judge." Here, responses must be *fast* and emphasize **liquidity and guarantees**. The overriding priority is to stop the run; moral-hazard concerns are secondary and should not be allowed to block participation.
- **Chronic phase:** liquidity pressures ease but solvency problems remain. Now policy should shift to the *banks themselves* — recapitalization, resolution of the nonviable, and heightened supervision. Contagion fears have receded, so weak banks can be allowed to fail or be merged.

## 3. What to do in the acute phase — a graduated escalation

Geithner's *Reflections on the Lender of Last Resort* provides the escalation ladder, and it deliberately runs from cheapest/least-committal to most powerful:

**(a) Lender of last resort first (liquidity).** Open central-bank liquidity to solvent-but-illiquid banks against good collateral (Bagehot: "lend freely against good securities at a penalty rate"). The purpose is to prevent sound banks from being forced into fire sales that would validate the panic. But note the sharp *limit*: LOLR lending "can help reduce the risk that the strong become illiquid, but it cannot make viable the fundamentally nonviable." Liquidity alone will **not** fix a solvency hole — and your two exposed banks may have a genuine solvency hole.

A caution from the *FHLB* note: don't let banks route around the true lender of last resort. In March 2023, troubled banks used the Federal Home Loan Banks as "lender of next-to-last-resort," which lack the capacity for large, fast, late-day liquidity. The central bank's discount window (or equivalent) must be the backstop, and discount-window stigma must be actively managed.

**(b) Address the run's root cause — a guarantee.** Because the run is driven by *uncertainty about exposures*, the single most powerful move is to remove the incentive to run by guaranteeing the liabilities creditors are fleeing. The corpus shows guarantees scaled to the problem:

- **Targeted guarantee of the fleeing instrument** — as in the 2008 U.S. response to the MMF run: Treasury's *Temporary Guarantee Program for Money Market Funds* insured shares as of the announcement date, and it worked — it covered 93% of the $3+ trillion market, **stopped the run, and cost nothing** (in fact earned $1.2 billion in fees). Pair it with a facility to relieve liquidity pressure (the Fed's AMLF/MMIFF lent against the funds' assets so they didn't have to dump them).
- **A broader blanket guarantee of bank liabilities** — if the run spreads to a wide range of bank funding, not just deposits. Sweden (1992) guaranteed *all* bank liabilities sector-wide; it is "widely agreed" this stopped runs, maintained foreign funding, and gave the central bank room to provide liquidity. Ireland (2008) did the same.

**The design lessons on guarantees are as important as the decision to use one:**

- **Credibility relative to fiscal capacity is everything.** Thailand's 1997 blanket guarantee *failed initially* — runs continued for months — because of "the size of liabilities the program covered and inconsistencies in government messaging," plus skepticism about whether the government could actually make good. Contrast Sweden, where a **joint announcement with the political opposition** gave the guarantee strong credibility.
- **Communication must be consistent.** Thailand reversed a promise to guarantee certain notes days after making it; Indonesia's initial *partial* guarantee (only IDR 20m/account) actually *triggered* runs by large depositors. Ireland's guarantee was criticized because authorities underestimated the problem — and it ultimately cost EUR 41.7bn and an IMF program.
- **A guarantee does not cure underlying insolvency.** It buys time; it must be paired with liquidity and, later, restructuring.
- **Manage moral hazard with light-touch acute-phase tools** — cap deposit rates, ban aggressive marketing of the guarantee — rather than punitive measures that would deter participation.

**(c) A bank holiday / ring-fencing — only as a measure of last resort.** The *Survey of Bank Holidays and Fund Suspensions* is explicit: a holiday is a "high-risk tool" best reserved for when distress is *widespread* and a *coordinated* solution is needed. Crucially for your scenario, a holiday can be used to **ring-fence** the affected institutions and differentiate them from healthy ones — exactly the *US–Rhode Island 1991* case, where the collapse of two institutions bankrupted the private insurer, and a holiday closed the affected banks while sparing the sound ones. But note the counter-lesson: *Ecuador 1999* imposed a broad holiday instead of resolving a few nonviable banks and made the crisis far worse. **If only a limited number of banks are truly in distress, prefer the tailored approach** — recapitalize or resolve them (as India did with Yes Bank 2020, expanding deposit insurance *before* imposing the moratorium). The SEC's experience also warns that a *discretionary* redemption gate at a liquidity threshold caused investors to run *in anticipation* of it — poorly designed circuit-breakers backfire.

## 4. The decisive move for the *unknown-exposure* problem: a stress test with a capital backstop

This is the part of the toolkit built precisely for "no one knows the pattern of exposures." In 2009 the U.S. faced the same confidence deficit — Tim Clark recalls loss estimates ranging "from not really being much of a problem to possibly wiping out the entire capital base of the banking system." The response was the **Supervisory Capital Assessment Program (SCAP / "stress test")** paired with the **Capital Assistance Program (CAP)**:

- **Publicly test the banks and disclose the results and methodology.** This directly attacks the information vacuum that is fueling the run — it *reveals* the exposures rather than leaving the market to fear the worst. It "restore[d] confidence … that the nation's largest banking institutions have a sufficient capital cushion."
- **Make it credible.** Clark stresses it "had to be a real stress test" with an uncertain outcome; predetermining a happy ending "would obviously have massively undermined the credibility."
- **Back it with a guaranteed capital source.** The test worked *only because* Treasury committed under CAP to inject capital into any bank the test found short. That way the "worst thing that was going to happen" was known and bounded. Banks were given time (six months) to raise private capital first — and, as Clark notes, showing that private investors "have enough confidence that they're willing to put billions of dollars at risk" is itself a powerful confidence signal.

This maps directly onto your problem: the sector faces runs *because the pattern of exposures is unknown*. A transparent, credible supervisory assessment — backed by a public capital backstop — resolves the uncertainty and lets you **differentiate viable from nonviable banks**, which the bank-holiday survey identifies as the single most important step for restoring trust.

## 5. Deal with the actually-insolvent banks — differentiation is critical

Your two exposed regional banks may be genuinely insolvent (a solvency problem, not a liquidity one). The corpus is emphatic that you must not paper over this:

- **Reopen/support only viable banks; resolve the rest.** From the bank-holiday survey: reopening nonviable banks "risks a restart of runs." Roosevelt's 1933 success rested on reopening only "sound" banks (~12,000 of 17,000) after recapitalizing where needed.
- **Solvency is the constraint on central-bank support.** Both Geithner's essay and the *Solvency as a Fundamental Constraint on LOLR* article (citing the ECB's ELA framework) hold that liquidity support is for the solvent, or those with a *credible* recapitalization prospect; keeping fundamentally insolvent firms alive with central-bank loans is really fiscal policy and belongs with elected authorities. Resolving your two banks — through recapitalization, a supervised sale/merger, or a systemic-risk-exception assisted deal (as with Wachovia/Citigroup in 2008) — is appropriate.
- **Avoid forbearance.** The *Containing Runs on Solvent Banks* article warns that supervisory hesitation to act on undercapitalized banks — driven by fear of triggering panic — "buys time but ultimately extends value deterioration and increases losses." Act early on capital, and note the accelerant of modern runs via social media.

## 6. A recommended package (matching scope of response to scope of problem)

Drawing the threads together — and heeding the COVID-19 policy-package finding that a coordinated, "all-out" combination of measures works best under deep uncertainty:

1. **Immediately:** Open ample central-bank liquidity to solvent banks against good collateral; ensure the discount window (not next-to-last-resort substitutes) is the backstop and manage stigma.
2. **Fast, to stop the confidence run:** Announce a credible, well-communicated **guarantee** targeted at the liabilities creditors are actually fleeing (expand deposit insurance and/or guarantee broader funding), sized to the run and clearly backed by fiscal capacity — ideally with visible political unity. Pair with a facility so banks/funds need not fire-sell assets. Add light-touch moral-hazard controls (rate caps, no aggressive marketing of the guarantee).
3. **Within weeks, to resolve the unknown-exposure problem:** Run a **credible, transparent supervisory stress test** across the regional-bank sector, disclose results, and **pre-commit a public capital backstop** for any bank found short after a private-raising window. This converts unknown exposures into known, bounded ones and lets the market differentiate.
4. **For the two genuinely troubled banks:** Recapitalize if viable; otherwise resolve them promptly (assisted sale/merger or resolution) — differentiate the sound from the unsound, and reopen/support only the viable.
5. **Reserve the bank holiday / ring-fencing** only if the run becomes truly systemic and uncontrollable; if distress remains confined to a few banks, prefer the tailored resolution route.
6. **Wind down as you move to the chronic phase:** As confidence returns, let the guarantees expire on schedule, allow weak banks to fail or merge, and raise supervisory intensity on the guaranteed institutions.

## Bottom line

**Yes, the government should act — decisively and with a coordinated package, not a single tool.** The run is largely confidence contagion driven by unknown exposures, so the highest-value moves are (i) a credible, well-communicated **guarantee** to remove the incentive to run, combined with **liquidity** to prevent fire sales, and (ii) a **transparent stress test with a public capital backstop** to resolve the very uncertainty that is fueling the panic. Simultaneously, **differentiate and resolve** the genuinely insolvent banks — guarantees and liquidity buy time but cannot cure insolvency, and reopening or propping up nonviable banks simply restarts the runs. Sequence liquidity → guarantees → capital/resolution, size each measure to the actual scope of the problem, and preserve credibility above all — that is the consistent through-line from Sweden and the 2008–09 U.S. response (success) to Thailand, Indonesia, and Ecuador (where under-scaled or inconsistent action prolonged the crisis).