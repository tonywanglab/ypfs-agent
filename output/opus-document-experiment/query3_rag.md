# Query 3 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 5, "get_document": 1}

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

I now have a strong, well-grounded basis for answering. Let me synthesize the corpus findings into a structured recommendation.

---

# What Should the Government Do?

The corpus offers a surprisingly clear framework for this scenario. Below I lay out (1) the threshold diagnostic question you must answer first, (2) the sequenced toolkit if intervention is warranted, and (3) the key design cautions—each grounded in documented crisis experience.

## 1. First, run the diagnostic: is this actually going to be a crisis?

Before deploying any emergency tools, the government should apply the **two-pronged test** from Klein's *Incorporating Macroprudential Financial Regulation into Monetary Policy*. His central thesis: **both a fundamental mispricing of an asset AND excessive leverage are necessary to produce a financial crisis. One alone produces, at most, a bubble or a slowdown—not a panic.**

- An **asset bubble without leverage** deflates without systemic contagion. Klein cites the dot-com bust: "central bankers did not move to aggressively pop the bubble, and when the bubble eventually popped no financial crisis ensued."
- **Excess leverage without a fundamental asset mispricing** likewise fails to metastasize—Klein's example is the S&L debacle, where thousands of banks failed (leveraged 100:1–200:1) yet "this bank regulatory failure did not metastasize into a financial panic," because the leverage was not "coupled with a fundamental mispricing of an asset class."

**Your scenario has both ingredients potentially in play:** AI equity valuations may have been fundamentally mispriced (the DeepSeek-style shock reveals that the moat/capex thesis was wrong), and those valuations are being used as loan collateral, implying leverage in the financial system. So the government's very first job is a *forensic assessment of the transmission channels*:

- **How much leverage is actually built on AI-equity collateral?** Is this concentrated in a few intermediaries or diffused across the system? What are the interconnections and common exposures (the macroprudential lens Klein emphasizes)?
- **Is the collateral fall a repricing (markets correctly re-rating an overvalued asset) or a fire-sale-driven overshoot?** This distinction determines whether intervention would be "stepping in as emergency liquidity provider in an oversold market, rather than propping up a failed asset class" (the Bank of England's phrasing in the AHEL survey).

Klein's key policy prescription applies directly: **focus on the leverage, not the asset price.** "Markets are far better at asset-price valuation." The government should *not* try to defend AI equity valuations. Its legitimate concern is only whether excess leverage will break the "transmission"—the point at which markets seize, institutions hoard liquidity, and fire sales cascade into the broader credit system.

## 2. If a genuine panic is forming, act in the correct sequence

The surveys converge on an **acute-phase / chronic-phase framework**. Different tools belong to different phases, and getting the sequence right matters more than any single instrument.

### Acute ("panic") phase — stop the run first

In the acute phase, the surveys are emphatic: **policy must focus on the behavior of the running counterparties, not on the intermediaries themselves** (*Broad-Based Capital Injection Programs*). The tools, roughly in order of speed:

**(a) Liquidity provision as the fastest first response.** The *Ad Hoc Emergency Liquidity Programs* survey notes AHEL is "generally the quickest possible policy response to implement and can help the institution meet the demands of a run." For a broader problem, **broad-based emergency liquidity** and **market liquidity programs** (à la the Fed's GFC alphabet-soup facilities) are appropriate. Given the problem centers on a specific, now-distrusted collateral class, the AHEL survey's guidance is relevant: central banks can "loosen their collateral eligibility requirements as much as necessary," and *Market Liquidity Programs* documents how the Fed repeatedly **expanded eligible collateral as conditions worsened** to target "asset classes about which the market has become uncertain."

**(b) Guarantees to halt creditor runs.** The *Blanket Guarantees* survey and the finding that "the US CPP…did not stabilize the financial system alone—only when it was combined with a debt guarantee from the FDIC was the government able to calm financial markets" both point to guarantees as a powerful acute-phase tool.

**Crucially — do NOT expect liquidity alone to solve it.** The single most important lesson from the AHEL survey: *"liquidity crises are rare in the absence of deeper-seated solvency or viability concerns."* In none of 22 surveyed cases did illiquidity simply "pass" after liquidity was provided. Even where authorities sized liquidity to cover *all* possible outflows, "counterparty and customer outflows continued until additional measures were implemented." **Liquidity buys time; it does not cure insolvency.**

### Chronic ("debt overhang") phase — repair the balance sheets

If intermediaries are genuinely insolvent (not merely illiquid) because their AI-loan collateral has permanently repriced, the structural tools apply:

**(c) Capital injections.** *Broad-Based Capital Injection Programs* finds strong evidence that "recapitalization of banks appears particularly effective in channeling the intervention effects from financial to nonfinancial sectors." Design guidance:
- **In the acute phase, simpler is better** — favor common or plain preferred shares over complex instruments.
- **Ensure wide participation to minimize stigma** — e.g., the US CPP model of getting nine major banks to take capital simultaneously so participation didn't signal weakness.
- **Combine recapitalization with an NPL / impaired-asset strategy** — "recapitalization is often ineffective without an NPL strategy, and vice versa." Here, that means addressing the impaired AI-collateralized loans directly (purchase, guarantee, or bad-bank).
- **Don't let banks hit capital ratios by shrinking assets** (the US CAP lesson) — force the fix through new capital, not by cutting lending.

## 3. Design cautions specific to this scenario

- **Assess *viability*, not just accounting solvency.** The AHEL survey stresses that central banks should evaluate a firm's "viability as a going concern," recognizing solvency is nearly impossible to judge in real time at fire-sale prices. But there's a warning: lending to a *nonviable* firm risks losses, mispriced support, and "drifting into fiscal policy." If an intermediary's business model was fundamentally built on a mispriced AI thesis, propping it up may be throwing good money after bad.

- **Do not permanently underpin a nonviable asset class.** The Bank of England's own words: it would lend against distressed securities to reduce economic costs "but…would wish to avoid permanently underpinning the existence of markets that were not fundamentally viable." If AI-company equity was genuinely overvalued, the government's role is to prevent a *fire-sale overshoot and disorderly deleveraging*—not to restore pre-shock valuations. Let the markets do the repricing; contain only the leverage-driven contagion.

- **Sequence moral-hazard concerns correctly.** The AHEL and Blanket Guarantee surveys agree: in the acute phase, don't burden emergency support with punitive terms (penalty rates can "accelerate the drain" on a running institution). Save moral-hazard discipline—executive-comp limits, fees, warrants, tougher supervision—for the later structural interventions, "when the institution has been stabilized as a going concern."

- **Political support and communication are decisive.** Guarantees and capital injections that carry large potential fiscal cost require credible, unified political backing (Sweden's joint opposition announcement is the positive example; Thailand/Indonesia/Ecuador the negative).

## Bottom line

1. **Diagnose before acting.** Establish whether real, systemic leverage sits on AI-equity/AI-loan collateral. If leverage is limited or contained, this is a bubble deflating—painful but not a crisis—and the government should largely let markets reprice while monitoring transmission channels. Klein: worry only when *both* mispricing and excess leverage are present.

2. **If a panic is forming, move fast in the acute phase** with broad liquidity (flexible collateral) and, if needed, guarantees—aimed at stopping the run by counterparties.

3. **Follow immediately with structural repair** in the chronic phase—recapitalization paired with an impaired-asset strategy—because liquidity buys time but cannot cure insolvency.

4. **Contain the leverage, don't defend the asset price.** The policy goal is to keep the financial "transmission" in gear so credit keeps flowing to the real economy—not to rescue AI equity valuations that the market may be correctly writing down.

*(Sources drawn from the corpus: Klein, "Incorporating Macroprudential Financial Regulation into Monetary Policy"; "Ad Hoc Emergency Liquidity Programs in the 21st Century"; "Broad-Based Capital Injection Programs"; "Broad-Based Emergency Liquidity Programs"; "Market Liquidity Programs: GFC and Before"; and the "Blanket Guarantees Survey.")*