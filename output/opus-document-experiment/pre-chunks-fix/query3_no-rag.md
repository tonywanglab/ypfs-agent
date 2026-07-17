# Query 3 — no-rag

Model: anthropic/claude-opus-4.8 | Retrieval: no-rag | System prompt: none
Tool calls: none (plain model)

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

# Assessing the Scenario First

Before prescribing action, I'd want to separate distinct problems that are getting bundled together here, because they call for very different responses—and some call for no government response at all.

## Three separate things are happening

**1. AI equity prices crash.** This is not, by itself, a problem for the government to solve. Asset prices falling because a competitor may have leapfrogged is the market working correctly. Bailing out equity holders would be indefensible—they took a risk and it went against them. If the Chinese claim is real, US AI valuations *should* fall.

**2. Loan collateral falls, raising solvency concerns.** This matters more, but it's still fundamentally a story about lenders who made loans against volatile collateral. Solvency losses should generally fall on the shareholders and creditors of the affected firms, not taxpayers.

**3. A liquidity crisis is feared.** This is the one legitimate area for aggressive government (specifically central bank) action.

## The critical distinction: solvency vs. liquidity

This is the heart of it. The classic **Bagehot rule** applies:

- **Illiquid but solvent institutions** should be lent to freely, against good collateral, at a penalty rate. This stops fire-sale contagion where a temporary funding freeze turns healthy firms into failed ones.
- **Insolvent institutions** should *not* be propped up. They should be resolved—wound down, with losses imposed on shareholders and then creditors, depositors protected up to insurance limits.

The danger is that in a panic these are hard to tell apart, and there's enormous political pressure to treat everything as "just liquidity" to avoid imposing losses.

## What I'd actually recommend

**Central bank (the Fed, not "the government"):**
- Stand ready to provide liquidity through the discount window and, if contagion is systemic, emergency facilities—against sound collateral, at a penalty rate.
- Emphasize this is liquidity support, not a solvency backstop.

**Regulators/Treasury:**
- Rapidly assess actual exposures. How concentrated is AI-collateralized lending? Is this a few overexposed intermediaries or a systemic web?
- Prepare resolution mechanisms for genuinely insolvent firms. Impose losses on equity and creditors first.
- Communicate clearly to reduce the *fear* itself, since much of a liquidity crisis is a coordination failure driven by uncertainty.

**What the government should NOT do:**
- Bail out AI companies or their shareholders.
- Prop up insolvent lenders to avoid embarrassment.
- Attempt to prop up asset prices.

## A note on the harder questions this raises

A few things worth flagging that go beyond crisis mechanics:

- **The moral hazard problem is real.** Every intervention teaches lenders that AI-collateral risk is partly socialized. If the response is generous, expect more of this next time.
- **The Chinese announcement should be verified, not assumed.** Claims of "recursive self-improvement" are extraordinary and often overstated. Policy shouldn't be anchored to an unverified press release; markets may partly correct on their own.
- **The deeper issue is that highly volatile, correlated assets became widely used as loan collateral.** That's a supervisory/regulatory failure worth examining *after* the fire is out.

The short version: **provide liquidity to the solvent, resolve the insolvent, protect no one from the consequences of their own bets, and don't confuse a falling stock market with a financial crisis.**