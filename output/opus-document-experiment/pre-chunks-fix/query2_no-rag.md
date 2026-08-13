# Query 2 — no-rag

Model: anthropic/claude-opus-4.8 | Retrieval: no-rag | System prompt: none
Tool calls: none (plain model)

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

# Assessing the Situation

This scenario has the classic features of a financial crisis: an initial loss, opacity about who is exposed, and contagion driven by uncertainty rather than confirmed insolvency. The core problem is that depositors can't distinguish solvent-but-illiquid banks from genuinely insolvent ones, so they run on everyone.

Before acting, I'd want to establish some facts—though crisis decisions are often made with incomplete information.

# Key Diagnostic Questions

1. **Liquidity vs. solvency?** Are banks failing because they can't meet withdrawals (liquidity) or because their assets are genuinely worth less than their liabilities (solvency)? This is the central question and often unknowable in real time.
2. **How large are actual exposures?** The fear is driven by *unknown* exposure. Rapid supervisory data-gathering could shrink the problem.
3. **Systemic importance?** Are these banks interconnected enough that failures cascade, or can some be allowed to fail cleanly?

# A Tiered Response

**1. Address the information problem (cheapest, most targeted)**
- Supervisors should rapidly assess and, ideally, *disclose* the true pattern of exposures. If most banks have minimal exposure, transparency alone can stop the run. Ambiguity is what makes runs universal.
- A credible, fast stress test/audit can separate the healthy from the impaired.

**2. Provide liquidity to solvent institutions (Bagehot's rule)**
- The central bank should lend freely, against good collateral, at a penalty rate, to institutions that are solvent but illiquid. This is the textbook lender-of-last-resort function and stops liquidity-driven runs without subsidizing bad actors.

**3. Backstop depositors to halt the panic**
- Since runs are driven by depositor fear, a credible deposit guarantee (or temporary expansion of existing insurance) can be more effective and cheaper than bailing out institutions. It protects the people the system exists to serve, not shareholders.

**4. Resolve the genuinely insolvent institutions**
- Banks that are actually insolvent should be resolved—wound down, sold, or restructured—with losses falling on shareholders and, where appropriate, creditors, *before* taxpayers. Modern resolution regimes aim to preserve critical functions while imposing losses on those who took the risk.

# Guiding Principles

- **Don't bail out the fund or its investors.** They took private-debt risk knowingly; write-downs should stand. Protecting them creates severe moral hazard.
- **Distinguish protecting the *system* from protecting *firms*.** The public interest is in payment systems, credit availability, and depositor confidence—not in any particular bank's survival.
- **Impose losses in the right order.** Equity and risk-taking creditors first; taxpayers last and only if systemically necessary.
- **Move fast but avoid permanent distortions.** Emergency measures should be temporary and priced to be unattractive once conditions normalize.

# What I'd Be Wary Of

- **Overreacting** and guaranteeing everything, which teaches markets that risk is socialized (the 2008 moral hazard critique).
- **Underreacting** and letting a solvable liquidity panic become a solvency crisis through fire sales and credit contraction.
- **Political pressure** to protect connected losers (the fund's investors) under cover of "financial stability."

# Bottom Line

The government's job here is narrow but important: **stop the panic and protect depositors and the payment system, while letting the actual bad bets—and the institutions that made them—bear their losses.** In practice that means transparency first, liquidity to the solvent, guarantees to halt runs, and orderly resolution for the insolvent—not a rescue of the fund or its investors.

There's genuine debate about where to draw the line (how generous guarantees should be, how much to intervene in "maybe-solvent" cases), and reasonable experts disagree. But the framework of *diagnose the problem, target the intervention, and put losses where the risk was taken* is broadly accepted.