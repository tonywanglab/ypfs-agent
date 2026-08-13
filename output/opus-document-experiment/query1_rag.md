# Query 1 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 6, "get_document": 1}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I now have comprehensive grounding. Here is my recommendation.

---

# Recommendation: Responding to a Distressed Systemically Important Insurer

## Framing note

The scenario you describe — a globally significant insurer hit by a large loss, downgraded by rating agencies, facing investor flight and a short-term liquidity crisis, and asking government for help — maps almost exactly onto the most instructive case in the corpus: the 2008 rescue of **American International Group (AIG)**. I draw my recommendation from that case (YPFS Module Z Overview and the related modules) and from the survey on emergency liquidity design. Below I set out the analysis and a concrete sequence of steps.

## Step 1 — Do not commit to anything before answering the threshold question: is failure a *systemic* threat?

The government's strategy should **not** be to save every institution that might fail, but only those "whose failure could jeopardize the stability of the system" (Module Z, Key Design Decision 1). Before offering anything, assess:

- **Size, reach, and interconnectedness** — Is the insurer's failure likely to spread contagion? In AIG's case the decisive factors were its ~$1 trillion balance sheet, a $2.7 trillion derivatives book, concentrated exposures among the 12 largest international banks, and retail reach into pension plans and policyholders.
- **Counterparty and funding-market linkages** — Would failure force write-downs at major banks, raise their capital requirements, or disrupt the commercial paper / money-market funds?
- **State of the wider system** — The same failure is far more dangerous in a fragile market. AIG's risk was judged "a function of the state of the world at that moment."

If failure is **not** systemic, the appropriate answer is generally to let existing insolvency/resolution processes handle it — not a bailout.

## Step 2 — Diagnose liquidity vs. solvency, and expect the line to blur

A critical AIG lesson: officials initially treated it as a *liquidity* problem, then discovered the problems were deeper — asset devaluations and possible *insolvency*. "The line between the two is often vague" (KDD 9). Your natural-disaster loss is a real capital hit, so you should assume from the outset that pure liquidity lending may not be enough and that a **capital** solution may also be required. Do not design a facility that only addresses today's cash calls if the underlying capital hole will trigger the next downgrade.

## Step 3 — Push hard for a private-sector solution first

In AIG, the authorities' *first* option was always a private solution — convening major banks to assemble a syndicated bridge loan (modeled on the 1998 LTCM rescue). Only when Lehman's bankruptcy caused the private consortium to collapse did the government become "the company's last hope." **Use your convening authority** to attempt a private lifeline (asset sales, a private syndicate, a strategic buyer) before deploying public funds. This both tests whether public money is truly necessary and creates a defensible record.

## Step 4 — Confirm legal authority and required approvals

AIG was rescued under emergency lender-of-last-resort authority (Fed Section 13(3)) because there was no resolution framework for a nonbank insurer other than bankruptcy. Note two things:

- **Insurers are typically regulated separately** (in the US, at the state level; insurance is often carved out of bankruptcy). Coordinate immediately with the insurance regulator(s).
- **Post-crisis law changed the tools.** Dodd-Frank now requires that Fed emergency lending go through a "program or facility with broad-based eligibility" and be approved by the Treasury Secretary — a bespoke, single-firm AIG-style facility would **not** be permitted today. Confirm what your own jurisdiction's current law actually authorizes before promising anything. If there is an orderly-resolution regime (e.g., an OLA-type receivership), consider whether that, not an open-ended rescue, is the right vehicle.

## Step 5 — If you must intervene, lend on a secured basis to a viable firm

If failure is systemic and no private solution exists, the classic lender-of-last-resort structure applies:

- **Secured lending.** AIG's facility was collateralized by substantially all assets, including the equity of its regulated insurance subsidiaries, placing the government in a senior secured position. The core judgment was that the insurance subsidiaries "had value" sufficient to secure the loan.
- **Collateral discipline.** Per the emergency-liquidity survey: lend against adequately valued collateral with appropriate haircuts, using an existing published schedule where possible for fairness and speed. Be aware that stress can rapidly erode collateral values, so adjust haircuts/valuation accordingly.
- **State the purpose narrowly:** to let the firm "meet its obligations as they come due" and "sell certain of its businesses in an orderly manner, with the least possible disruption."

## Step 6 — Set terms carefully — the AIG "penalty rate" is a *caution*, not a model

AIG's original terms (LIBOR + 8.5%, ~12%, plus an 8.5% undrawn commitment fee, 2-year term) were deliberately "onerous" to combat moral hazard and force quick repayment. **But this backfired**: the punitive terms raised leverage, alarmed the rating agencies, and threatened the very downgrade the rescue was meant to prevent. Within weeks the terms had to be softened (rate cut to LIBOR + 3%, term extended to 5 years). The lesson (Module Z, footnotes 19 & 75):

- Calibrate rates to be a genuine incentive to repay **without** being self-defeating for a firm whose survival depends on keeping an investment-grade rating.
- **Watch the rating agencies as a binding constraint** — "a financial institution cannot operate without at least an investment-grade rating."
- Consider **parity** with terms offered to other firms, to avoid criticism of unfairness.

## Step 7 — Protect taxpayers and address moral hazard — with an equity component, cautiously

The government protected taxpayers through (a) senior secured lending at market-value asset purchases, (b) dividend restrictions and governance rights, (c) **management change** (the CEO was required to resign), and (d) an **equity "kicker"** — a 79.9% stake giving upside to taxpayers. This ultimately produced a **$22.7 billion net gain**. Two cautions:

- Keep any ownership stake **below 80%** to avoid consolidating the firm onto the government balance sheet.
- The equity/control mechanism drew charges of "nationalization" and a decade of litigation (*Starr*). If you take equity, ensure the legal basis is solid and any holding structure (e.g., an independent trust) is genuinely independent in form and substance.

## Step 8 — Expect to iterate, coordinate, and staff up

The AIG rescue was not one action but a **sequence** — a credit facility, a securities-borrowing facility, two special-purpose vehicles to buy troubled assets at market value, capital injections, and a final recapitalization, totaling $182.3 billion. Practical lessons:

- **Be prepared to "recalibrate"** as you learn more; the initial facility was based on incomplete information. Embark on continuous monitoring and place your own team inside the firm.
- **Coordinate** across the central bank, the treasury/fiscal authority, and insurance regulators — liquidity tools and capital tools come from different places, and "cooperation between monetary and fiscal authorities is key."
- **Document** facts known, options considered and rejected, and time constraints — you will face intense scrutiny.
- **Communicate transparently** and manage disclosure carefully (e.g., counterparty identities), balancing accountability against market-stability risks.

## Step 9 — Have an exit strategy from the outset

Aim for full repayment, orderly asset sales, and eventual disposal of any equity stake — as in the AIG recapitalization, which returned all funds plus a profit.

---

## Bottom line

1. **Verify systemic risk first.** If the insurer's disorderly failure would not threaten the financial system, do not bail it out — use resolution/bankruptcy tools.
2. **Exhaust a private-sector solution** using your convening authority.
3. **Confirm you actually have legal authority** — modern rules may bar an AIG-style single-firm rescue.
4. **If you intervene:** lend secured against genuinely valuable collateral to a firm you judge viable; diagnose the capital hole, not just the cash gap; set terms that incentivize repayment **without** triggering the downgrade you're trying to prevent; require management/governance changes and consider a sub-80% equity stake to protect taxpayers and address moral hazard; coordinate with insurance regulators and the treasury; monitor continuously and be ready to restructure; and plan the exit.

The AIG experience shows this can work — the firm survived, systemic collapse was averted, and taxpayers ultimately profited — but also that it is legally fraught, politically charged, far larger and longer than first anticipated, and easy to get wrong on the terms.

**Caveat:** These recommendations are grounded in the AIG case and the emergency-liquidity survey in the corpus. The specific legal authorities, resolution regimes, and insurance-regulatory arrangements in *your* jurisdiction will materially shape what is permissible and advisable, and should be confirmed before acting.