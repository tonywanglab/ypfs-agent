# Query 1 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 5, "get_document": 1}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I now have a comprehensive, directly-on-point precedent (the AIG rescue) plus the general survey guidance on ad hoc emergency liquidity. Here is my recommendation.

---

# Recommendation: Response to a Distressed Systemic Insurer in a Liquidity Crisis

## Executive summary

Do **not** simply hand the company a government check. The corpus's most directly analogous precedent — the 2008 rescue of **American International Group (AIG)**, a ~$1 trillion global insurer downgraded by all three rating agencies in a single day, facing collateral calls and investor flight — shows a structured path that both averted systemic collapse **and ultimately returned a $22.7 billion profit to taxpayers**. The lessons literature (YPFS "Ad Hoc Emergency Liquidity Programs" and "Broad-Based Emergency Liquidity Programs" surveys) reinforces the design principles below.

My recommendation proceeds in five steps.

---

## Step 1 — First, establish whether this failure is genuinely *systemic*

The government's job is **not to save every institution that might fail**, only those whose failure would jeopardize the financial system (Geithner). In the AIG case, the authorities documented specific systemic-risk factors before acting. You should make the analogous determination here:

- **Size, reach and interconnectedness** — how concentrated are the exposures among other large banks/insurers, domestically and cross-border?
- **Contagion channels** — CDS/derivatives counterparties, securities-lending counterparties, commercial paper and repo funding markets, money-market funds.
- **Retail/real-economy dimension** — policyholders, pension funds, municipalities. AIG's retail footprint was judged to make its failure potentially *more* systemic than Lehman's.
- **Timing/market fragility** — a surprise failure in an already-stressed market is far more damaging.

If the failure is **not** systemic, the right answer is to let normal resolution/bankruptcy or insurance-guaranty mechanisms handle it. Government liquidity support should be reserved for genuine systemic risk.

---

## Step 2 — Push hard for a private-sector solution first

Before committing public funds, use the government's **convening authority** to try to assemble a private consortium (banks, potential acquirers) to provide a bridge loan or capital. In the AIG case the Fed pursued this first (modeled on the 1998 LTCM rescue), and only stepped in when it collapsed after Lehman's bankruptcy. A private solution avoids public risk and moral hazard. Document the effort — it strengthens the legitimacy of any subsequent public intervention.

---

## Step 3 — If public support is needed, lead with *secured, penalty-priced emergency liquidity* — not a giveaway

The classic lender-of-last-resort framework (Bagehot, echoed throughout the surveys): lend **to firms that are illiquid but viable, against collateral, at a penalty rate.** Concretely, following the AIG Revolving Credit Facility model:

- **A secured revolving credit line**, sized with a cushion to avoid having to return for more (AIG's line was topped up $10bn above the private estimate to reduce refunding risk).
- **Collateralized** by substantially all of the company's assets, including the equity of its regulated subsidiaries, placing the government in a **senior secured position**.
- **Penalty pricing** to (a) protect taxpayers, (b) mitigate moral hazard, and (c) incentivize rapid repayment/replacement with private financing.

### Two important cautions the corpus emphasizes:

1. **Do not make the terms *so* onerous that you defeat the purpose.** AIG's original 12% rate and short 2-year term were later judged counterproductive: they worsened AIG's leverage ratios and *triggered more rating-agency concern*, forcing a restructuring to lighter terms months later. **Calibrate the penalty rate carefully** — the Fed has discretion to do so, and other facilities used far lighter rates. Rating-agency reaction must be a design input from day one, because a company "cannot operate without at least an investment-grade rating."

2. **Liquidity buys time; it rarely stops the run by itself.** The AHEL survey is explicit: even covering all short-term outflows often did not halt runs. Emergency liquidity is a **bridge** to more structural measures (capital, guarantees, asset removal). Plan those in parallel.

---

## Step 4 — Protect the taxpayer and address moral hazard

- **Take an equity interest ("equity kicker").** In exchange for the extraordinary risk, the government took a **79.9% equity stake** in AIG (capped just under 80% to avoid consolidating the company's liabilities onto the government balance sheet under accounting rules). This penalized existing shareholders (moral hazard) and let taxpayers **share the upside** — which is precisely how the rescue ultimately generated a profit. If direct government share ownership is legally awkward, the AIG solution was an **independent trust** holding the shares for the benefit of taxpayers (design it to be genuinely independent to withstand legal challenge).
- **Governance conditions:** veto over dividends, restrictions on mergers/asset sales, and management change (AIG's CEO was replaced).
- **Address the *source* of the drain, not just the symptom.** AIG's liquidity was hemorrhaging through securities-lending cash-collateral demands and CDS collateral calls. The RCF alone didn't fix this; the authorities later created dedicated facilities (a Securities Borrowing Facility, and the Maiden Lane II/III SPVs) to **purchase the distressed assets at market value** and terminate the contracts, permanently stopping the drains. Identify your company's equivalent pressure points early.

---

## Step 5 — Get the legal authority, coordination, exit and transparency right

- **Legal authority:** Confirm the specific statutory basis for lending to a *nonbank*. Post-crisis reforms (Dodd-Frank) narrowed the Fed's individual-institution 13(3) authority and now require Treasury sign-off and broad-based eligibility — so verify what your jurisdiction actually permits before promising anything. Use the **minimum innovation necessary**; novel structures (like Maiden Lane III) drew the most criticism.
- **Coordination:** The rescue worked because the central bank (liquidity) and fiscal authority (capital, via TARP) coordinated, with the insurance supervisor engaged. Match the tool to the problem: **liquidity ≠ solvency capital**. If the company is undercapitalized (not merely illiquid), you will need a fiscal capital-injection tool, which the central bank generally cannot provide.
- **Exit strategy:** Define upfront how the government unwinds — asset sales, repayment, and disposal of the equity stake over time (AIG's was fully exited by 2012–13).
- **Transparency:** Announce purpose and terms; be prepared for intense scrutiny (bonuses, "backdoor bailout" of counterparties paid at par, "nationalization" charges all dogged AIG). Consider whether **shared sacrifice / haircuts** on creditors and counterparties are feasible — though note the genuine tension: haircuts can themselves trigger the run you're trying to stop, and mid-crisis is a poor time to litigate creditor priority.

---

## Bottom line

**Recommend conditional, secured, penalty-priced emergency liquidity — as a bridge, not a gift — coupled with an equity stake and governance controls to protect taxpayers, and paired with structural measures (asset purchases and, if needed, capital) that address the actual sources of the run.** Only do this if the failure is truly systemic, only after a private solution has genuinely been attempted, and only within clear legal authority with a defined exit. The AIG precedent shows this approach can both prevent systemic collapse and protect — even reward — the taxpayer.

*Caveats:* The AIG case is the closest analogue in the corpus, but every situation differs. Key unknowns you must resolve before deciding: (1) is this a pure liquidity problem or also a solvency/capital problem; (2) what does your jurisdiction's law actually authorize for nonbank support today; and (3) what is the realistic size and interconnectedness of the systemic threat.