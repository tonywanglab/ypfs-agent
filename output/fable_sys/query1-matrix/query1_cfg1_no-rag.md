# Query 1 — no-rag

Model: anthropic/claude-fable-5 | Retrieval: no-rag | System prompt: none
Tool calls: none (plain model)

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

## Recommended Approach

### Step 1: Diagnose the actual problem first

The single most important question: **is this a liquidity problem or a solvency problem?** Your response should differ dramatically depending on the answer.

- **Liquidity crisis, fundamentally solvent:** The company has assets exceeding liabilities, but can't monetize them fast enough to pay claims and meet collateral calls. Government support is defensible here.
- **Solvency crisis:** Losses exceed capital. "Liquidity support" would just delay recognition and transfer losses to taxpayers. Here you need resolution, not rescue.

Commission an immediate independent assessment (regulator + external actuaries) of claims reserves, reinsurance recoverables, and asset quality. Insurers' loss estimates after major catastrophes are notoriously uncertain in the first weeks.

### Step 2: Assess systemic importance honestly

Insurance failures are usually *less* systemic than bank failures—insurers don't face classic runs, and liabilities pay out slowly. But intervention may be justified if:

- The company is a major counterparty in derivatives or securities lending markets (the AIG problem in 2008)
- Its failure would leave millions of disaster victims with unpaid claims, amplifying the economic shock
- Its collapse would trigger contagion to other insurers or a collapse of insurance availability in the affected region
- Fire-sale liquidation of its asset portfolio would destabilize bond/equity markets

If none of these apply, an orderly resolution or run-off with policyholder protection may be preferable to a bailout.

### Step 3: Exhaust private solutions first

Before public money:
- **Emergency capital raise or strategic investor** (another insurer, private equity)
- **Reinsurance recoveries** — accelerate collection; verify reinsurers will pay
- **Asset sales or repo of high-quality assets**
- **Sale of healthy business units**
- **Regulatory forbearance tools**: temporary stays on policy surrenders, dividend suspension, temporary capital requirement flexibility

### Step 4: If public support is warranted, follow Bagehot principles

Lend **freely, against good collateral, at a penalty rate**, with strict conditions:

1. **Liquidity facility, not a gift** — secured lending or guarantees, priced to be unattractive except in emergency, senior in the capital structure
2. **Shareholders take losses first** — the state should receive equity, warrants, or preferred shares so taxpayers share upside; existing shareholders should be heavily diluted
3. **Conditionality**: suspend dividends and buybacks, replace management if failures contributed, cap executive compensation, require a credible restructuring plan
4. **Time limits and exit strategy** defined upfront
5. **Protect policyholders, not investors** — the public interest is in claims being paid, not in bondholders and shareholders being made whole

### Step 5: If insolvent, use resolution instead

Transfer the policy book to a solvent carrier or a bridge institution, activate the policyholder guarantee scheme (if one exists), and wind down the shell. Policyholders—especially disaster victims—get priority; shareholders are wiped out; creditors take haircuts per the legal hierarchy.

### Step 6: Manage communication and moral hazard

- Coordinate messaging between the government, central bank, and regulator to prevent a panic-driven surrender wave—but do not misrepresent the company's condition
- Coordinate with foreign regulators, since the company is globally significant
- Be explicit that support is exceptional and conditional, to limit moral hazard across the industry

### Longer-term follow-up

- Review whether catastrophe risk was adequately capitalized and reinsured industry-wide
- Consider a public-private catastrophe risk pool (like Florida's or France's CCR) if the underlying exposure is uninsurable at market prices
- Strengthen the insurance resolution regime so the next crisis has a clear playbook

**Bottom line:** Verify solvency, force private solutions first, and if you intervene, do it as a secured lender with tough conditions that protect policyholders and taxpayers—never as a rescuer of shareholders.