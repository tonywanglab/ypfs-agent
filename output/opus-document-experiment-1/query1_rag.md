# Query 1 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 3, "get_document": 1}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I now have a thorough grounding in the AIG precedent and the relevant lessons learned. Here is my recommendation.

---

# Recommendation Memo: Response to Distressed Systemically Important Insurer

## Bottom line
Do **not** reflexively bail out the company, and do **not** simply write a check. Your first task is to make a **threshold determination of systemic risk**, then—only if warranted—provide **collateralized emergency liquidity on stringent, incentive-compatible terms**, ideally after exhausting private-sector options. The 2008 rescue of AIG is the closest and most instructive precedent, and it offers both a playbook and a set of cautionary lessons.

---

## Step 1: Ask the threshold question — is this liquidity or solvency, and is failure systemic?

Before committing public resources, establish two things:

**(a) Is the firm systemically important?** The US government's strategy in 2008 "was not predicated on saving every institution that might fail, but on addressing those whose failure could jeopardize the stability of the system." For AIG, the factors that tipped the balance were: its size and reach; the concentration of its exposures among the 12 largest international banks; its retail footprint (policyholders, pension plans, municipalities); its role in the commercial paper market; and the risk of contagion in an already-fragile system.

Apply the same lens here. A large natural-catastrophe loss at a globally significant insurer raises analogous questions: Are counterparties, reinsurers, policyholders, and funding markets interconnected enough that a disorderly failure spreads? If not, the case for intervention is much weaker and you should let normal insolvency/resolution processes work.

**(b) Is this truly a liquidity problem or a masked solvency problem?** This distinction is critical but often blurry. With AIG, "even as the Fed was entering into the RCF, there was uncertainty about whether AIG had solvency issues in addition to its liquidity issues," and the two "often coexist." Liquidity support buys time; it cannot repair a hole in the balance sheet. If the catastrophe losses have rendered the firm insolvent, a liquidity loan alone will fail and you will be drawn into "whatever it takes" commitments (see the warning below).

A key structural feature to check, which drove AIG's crisis: **cash is often trapped in regulated insurance subsidiaries.** AIG had a huge balance sheet, but "most of its liquid assets and cash were held in its regulated insurance subsidiaries whose regulators would not permit the cash to flow to the holding company." Determine whether your firm faces the same trapped-liquidity problem before concluding it needs external help.

---

## Step 2: Exhaust the private sector first

In 2008 the authorities' first instinct—modeled on the 1998 LTCM episode—was to use the government's **convening authority** to organize a private consortium (JPMorgan/Goldman were asked to assemble a ~$75 billion bridge loan). Only when that collapsed (in the wake of Lehman) did the government step in. A private solution avoids moral hazard, protects taxpayers, and is generally preferable. Push hard for asset sales, private capital raises, and reinsurance/private financing before public money.

---

## Step 3: If you must intervene, use collateralized lending — not a giveaway

If the firm is systemic and viable-but-illiquid, the recommended instrument is a **secured emergency credit facility** in the classic lender-of-last-resort mold, with these features:

- **Fully collateralized** — AIG's facility was secured on substantially all assets of the parent and its non-regulated subsidiaries, including the stock of regulated insurance subsidiaries. This protects taxpayers and puts the government in a senior secured position.
- **Sized with a cushion** — AIG's line was set at $85bn (vs. the private $75bn) precisely because liquidity needs were uncertain; the extra headroom avoided having to "come back for more."
- **An equity kicker / warrants** — the government took a 79.9% equity interest. This served four purposes: compensate for risk, address moral hazard, give the government control/oversight, and let taxpayers share the upside. Note the deliberate **79.9% cap** — going to 80%+ would force consolidation of the firm's liabilities onto the government balance sheet under GAAP.
- **Governance conditions** — veto over dividends, ability to replace management/board, restrictions on mergers and asset sales.

The AIG rescue ultimately **returned a $22.7 billion profit** to taxpayers—evidence that a well-collateralized, equity-linked structure can protect the public purse.

---

## Step 4: Heed the cautionary lessons

The AIG case is as much a set of warnings as a template:

1. **Don't set terms so punitive they defeat the purpose.** AIG's initial 12% rate (LIBOR + 8.5%) and 8.5% undrawn commitment fee were intended to be "onerous" to incentivize fast repayment and curb moral hazard—but they worsened AIG's leverage ratios and *triggered rating-agency concern about further downgrades*, the very thing you're trying to prevent. The terms had to be softened in later restructurings. **Calibrate the penalty rate carefully.** You have discretion to use a lighter rate.

2. **Rating agencies are a binding constraint.** "A financial institution cannot operate without at least an investment-grade rating." Every design choice must be stress-tested from the rating agencies' perspective, because a downgrade triggers collateral calls and counterparty runs.

3. **A liquidity loan alone often won't be enough.** AIG required capital injections (TARP equity) and asset-purchase vehicles (Maiden Lane II/III) to address the *sources* of the cash drain, not just the symptoms. Have a plan for solvency support and expect to iterate as you learn more about the firm.

4. **Beware the "whatever it takes" trap.** Once the government commits a large initial sum, walking away becomes practically impossible; the initial commitment can bind you to escalating support of unknown ultimate cost. Go in with eyes open.

5. **Legal authority and structure matter.** Ensure any equity stake, special-purpose vehicle, or control mechanism rests on valid legal authority and can withstand later challenge (AIG's structure spawned years of litigation). Coordinate closely with the fiscal authority (Treasury-equivalent) and the firm's insurance regulator(s).

6. **Consider parity and fairness.** Terms seen as more punitive—or more generous—than comparable interventions invite criticism. And be prepared for "backdoor bailout" objections when counterparties/creditors are paid in full.

---

## Step 5: Governance, exit, and communication

- **Coordinate** across the central bank (liquidity), the fiscal authority (capital/guarantees), and the insurance regulator (subsidiary cash, policyholder protection). Cooperation between monetary and fiscal authorities was central to the AIG outcome.
- **Embed monitoring** — the Fed placed a dedicated team inside AIG to understand a firm it had never regulated. Do the same.
- **Define an exit** up front: asset sales, repayment, and eventual disposal of any equity stake.
- **Communicate transparently** — publish terms, state the purpose and systemic-risk rationale, and disclose to oversight bodies. Document your options, constraints, and reasoning contemporaneously; you *will* face intense retrospective scrutiny.

---

## Summary of my recommendation
1. **Assess systemic risk and the liquidity-vs-solvency question first.** If the firm is not systemic or is insolvent, use ordinary resolution/insolvency processes rather than a bailout.
2. **Try a private-sector solution** (asset sales, private capital, convened consortium) before public money.
3. **If intervention is warranted, lend on a fully collateralized basis** with a sizing cushion, an equity kicker (capped below 80%), and strong governance conditions—**not** an unconditional grant.
4. **Calibrate terms carefully** to avoid a self-defeating downgrade, watch the rating-agency constraint, and prepare for the possibility that liquidity support alone won't suffice.
5. **Coordinate, monitor, plan an exit, and be transparent** — and go in aware that the first commitment may bind you to more.

Note the important caveat: since 2008, many jurisdictions (e.g., via Dodd-Frank in the US) have **constrained emergency lending to single firms** and created **resolution regimes for systemic nonbanks**. You should confirm what authorities and resolution tools actually exist in your jurisdiction today before choosing an instrument—the AIG-style single-firm rescue may no longer be legally available, and an orderly-resolution framework may be the intended path.