# Query 1 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 3, "get_document": 1}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I now have a rich evidentiary base. The AIG case (a globally significant insurer with a ratings downgrade, investor flight, collateral-call-driven liquidity crisis, and a request for government help) is a near-exact analogue to your scenario, and the survey literature on ad hoc emergency liquidity (AHEL), resolution frameworks, and moral hazard provides the general principles. Here is my recommendation.

---

## Recommendation: How to Respond to the Distressed Systemic Insurer

### 1. First, diagnose the real problem: liquidity vs. viability — do not treat the run as the disease

The single most important lesson from the corpus is that **you must not mistake the liquidity run for the cause rather than the symptom of the company's problems.** The *Ad Hoc Emergency Liquidity Programs in the 21st Century* survey is explicit:

> "the liquidity crisis should instead be viewed as the manifestation of the market's assessing the firm as nonviable as a going concern… authorities should provide AHEL assistance only to institutions that they have deemed viable or that they have committed to make viable through additional interventions."

Across all 22 AHEL cases surveyed, **liquidity provision alone never "cured" a run** — even when authorities sized assistance to cover *all* potential outflows, withdrawals continued until structural measures (capital injections, guarantees, or a merger) followed. So the threshold question is not "can we plug the liquidity gap?" but "**is this firm viable as a going concern — either on its own or after intervention we are prepared to commit to?**"

Note also that "solvency" is very hard to assess in real time; the corpus recommends assessing **viability** (business-model-based, forward-looking cash-flow capacity, inclusive of intended policy support) rather than accounting solvency.

### 2. Determine whether the firm is genuinely systemic

Government help should not be predicated on saving every firm that might fail, only those "whose failure could jeopardize the stability of the system" (Geithner, in the AIG Overview). For AIG, the factors were: sheer size and global reach; complexity and interconnectedness (a $2.7T derivatives book concentrated among the 12 largest international banks); retail dimension (pensions, policyholders, municipalities); likely disruption to the commercial paper and money-market fund complex; and the fragile state of the broader system. **Apply this same systemic-risk test to your insurer** before committing public resources, and document the analysis.

### 3. Exhaust private-sector solutions first

In the AIG episode, authorities' first instinct — correctly — was to use their convening power to assemble a **private-sector bridge (a syndicate of banks)** before deploying public money. Only when that failed (post-Lehman) did they move to government lending. Consider forced mergers/acquisition by a healthier institution, which the resolution survey notes is a common "private" solution. Notably, the AHEL survey observes that a merger or committed capital injection can even serve as *additional security* for any bridge liquidity you extend.

### 4. If you must provide emergency liquidity, structure it as a bridge — and resist "penalty" terms

If the firm is systemic and viable (or you commit to making it viable), emergency liquidity buys time. But the corpus is emphatic that AHEL works **only as a bridge** to structural measures, and that of Bagehot's "lend freely, against good collateral, at a penalty rate," essentially **only "lend freely" survives** for individual-institution rescues:

- **Penalty rate — caution.** A punitive rate "is liable to instead accelerate the drain on the affected institution's financial resources (and be disfavored by the market and the rating agencies)." This is precisely what went wrong with AIG's original Revolving Credit Facility: the 12% rate and onerous terms were intended to limit moral hazard and speed repayment, but they *worsened the firm's leverage ratios and drew rating-agency alarm*, forcing the government to soften terms in the November 2008 restructuring.
- **Collateral — interpret flexibly.** Collateral sufficiency should be interpreted as flexibly as needed to get sufficient liquidity to the firm, especially when later structural steps (a capital injection or merger) will provide additional security.
- **Don't manage moral hazard through the liquidity terms.** "Moral hazard can be addressed in the more structural policy responses that will need to follow." Save punitive/costly features for the later, stabilizing stages.

### 5. Plan the structural follow-through *now* — liquidity must be paired with capital and asset relief

The AIG rescue succeeded only because liquidity was followed by structural measures that addressed the *sources* of the cash drain and repaired the balance sheet:
- **Capital injection** (Treasury's ~$70B TARP equity), which reduced leverage and reassured rating agencies;
- **Asset-purchase vehicles** (Maiden Lane II & III) that removed the toxic RMBS from the balance sheet and *terminated the collateral-call-generating contracts* — attacking the root cause;
- **Term extension and rate reduction** on the credit facility.

For your natural-disaster-driven insurer, the analogue is: bridge liquidity to meet immediate claims/obligations, followed by **recapitalization** and, if needed, **relief of the specific loss-generating exposures**.

### 6. Mind the rating agencies at every step

A recurring, explicit lesson: **credit ratings are a binding constraint** on how a rescue can be structured. Treasury's Jim Millstein: "a financial institution cannot operate without at least an investment-grade rating." Every intervention term should be evaluated from the rating agencies' perspective, because a further downgrade would trigger more collateral calls and counterparty flight — potentially causing failure *despite* the assistance.

### 7. Do NOT impose haircuts on creditors/counterparties in the acute phase

This is counterintuitive but well-supported. Millstein's *Lessons Learned*: haircuts "may sound like a good thing… but for several reasons they may, in fact, backfire and increase the government's total spend." A distressed-exchange/haircut can trigger a "D" (default) rating, massive collateral calls, and contagion to counterparties who may themselves then need rescuing. In a crisis, "any hint of insolvency" makes financing impossible and accelerates the run. Preserve the firm's ability to pay obligations as they come due — that is the first thing the market looks for.

### 8. Protect taxpayers and capture upside — but calibrate

Legitimate ways to protect the public purse (from the AIG case):
- **Collateralize** loans and take a **senior secured** position (though watch the rating-agency implications of subordinating unsecured creditors);
- Purchase assets **at market value** with the firm absorbing first losses;
- Take an **equity interest / "equity kicker"** to compensate for risk and give taxpayers a share of any upside (AIG ultimately returned a **$22.7B profit**). Structure creatively (e.g., convertible preferred held via an independent trust) — but proceed cautiously: the AIG equity stake drew "nationalization" charges and shareholder litigation. Note the **79.9% ceiling** to avoid consolidating the firm's liabilities onto the government balance sheet.

### 9. Coordinate authorities, use the right tool for each job, and be prepared for "whatever it takes"

The rescue required **cooperation between the monetary authority (liquidity) and the fiscal authority (capital/guarantees)** — a central bank can provide liquidity but "cannot make up for a lack of adequate capital." Coordinate with the firm's insurance supervisor(s) too (in AIG, state insurance regulators could have seized subsidiaries, triggering a domino effect). Be aware of the **"whatever it takes" trap**: once you make an initial commitment, you may be bound to escalate — so size and structure the *initial* commitment thoughtfully, and consider a modest cushion to avoid having to "come back."

### 10. Prefer a resolution framework if one exists; otherwise document everything

The overarching post-crisis lesson (from the *Resolution and Restructuring in Europe* survey and the FSB *Key Attributes*) is that the ideal is a **"third option"** — a special resolution regime that keeps essential functions running and imposes losses on shareholders/creditors (bail-in) *without* a taxpayer bailout, rather than the bankruptcy-vs.-bailout binary AIG faced. **If your jurisdiction has a resolution regime covering systemic non-banks/insurers, use it.** If not — as in 2008 — you will be improvising under emergency lending authority, so: assess options rigorously (bridge loan, guarantee of a private loan, prepackaged restructuring, etc.), and **contemporaneously document the facts known, options considered and rejected, time constraints, and the basis for decisions**, because your actions will face intense subsequent scrutiny.

---

### Bottom line
Do not simply hand the company cash because it asked. First establish that it is (a) genuinely **systemic** and (b) **viable** or capable of being made viable. Exhaust **private-sector solutions** (merger/syndicate). If public support is warranted, provide **bridge liquidity structured to buy time — not a punitive penalty facility** — and pair it immediately with a **credible structural plan** (recapitalization plus relief of the specific disaster-driven loss exposures) that repairs the balance sheet, satisfies the rating agencies, and lets the firm meet obligations as they come due. **Avoid creditor haircuts in the acute phase.** Protect taxpayers via collateral, market-value asset purchases, and an equity stake capturing upside. Coordinate the central bank and fiscal authority, and — if available — resolve the firm through a formal resolution regime rather than an ad hoc bailout.

*(Sources: YPFS surveys "Ad Hoc Emergency Liquidity Programs in the 21st Century" and "Survey of Resolution and Restructuring in Europe: Pre- and Post-BRRD"; the "Rescue of American International Group" case modules Z and E; and the Millstein "Lessons Learned" interview.)*