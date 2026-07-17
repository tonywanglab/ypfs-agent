# Query 3 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 5}

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

I now have a strong evidentiary basis. Let me synthesize the corpus's lessons into concrete guidance for your scenario.

---

## Framing the problem: this scenario is not (yet) a textbook banking panic

Your scenario has an unusual origin. The trigger is not fraud, bad mortgages, or a housing bust—it's a *technology shock* that revalues AI equity and the collateral behind AI-company loans. But the corpus is clear that **the origin of a shock matters less than its transmission mechanism**. What determines the government's response is whether falling asset prices are threatening the *core of the financial system* through runs and fire sales—not the fact that some asset class fell.

Two threshold questions frame everything:

1. **Is the price decline fundamental or a fire sale?** If Chinese firms have genuinely achieved cheaper frontier AI without Nvidia, then a large part of the drop in U.S. AI equity and collateral values is a *fundamental* repricing, not a liquidity-driven overshoot. The corpus warns sharply against confusing the two. As one article puts it, if "price declines are fundamental in nature," then programs where "the U.S. Treasury takes a leveraged first-loss position on credit risky instruments … expose the taxpayer to undue risks when solvency rather than liquidity is the dominant problem" (*Revisiting Subprime Pricing Irrationality*). You should not deploy asset-purchase or collateral-backstop programs to prop up a valuation that the market is *correctly* marking down.

2. **Is the core of the system at risk, or just the weakest, most AI-concentrated intermediaries?** Geithner's central lesson is that the appropriate objective is "protecting the stability of the essential core of the financial system, not … preventing the failures of individual firms at the weakest end of the solvency continuum."

## Lesson 1: Diagnose before you deploy — but accept you can't diagnose perfectly

The corpus is emphatic that solvency and liquidity are hard to distinguish in real time. Geithner: *"There is no bright line between the insolvent and the merely illiquid, and therefore no purely objective, well-established set of rules for triage among firms."* The *Ad Hoc Emergency Liquidity* survey adds that "balance sheet solvency is particularly difficult to evaluate in real time" and stresses **viability** as the better lens—lending to a *nonviable* firm risks losses, stigma, and drifting into fiscal/political territory.

Practical implication: your regulators should immediately assess the affected intermediaries' *actual exposure* to AI equity and AI-backed loans, and how much of their funding is short-term and runnable. The key data are: how concentrated is AI collateral in each firm's balance sheet, and how much runnable funding sits on top of it?

## Lesson 2: Match the tool to the problem — liquidity tools cannot fix a capital hole

This is the single most important lesson in the corpus, and it directly determines what the government should *not* do first. Geithner:

> *"Liquidity support alone is a poor substitute for capital. There's no realistic amount of liquidity that can fully reassure creditors in a panic… They could mitigate a loss of funding, but they could not make up for a lack of adequate capital."*

If AI collateral has genuinely lost value, affected intermediaries face a **capital (solvency) problem, not merely a liquidity problem.** Pouring central-bank liquidity into an undercapitalized firm just "finances the exit of existing creditors" while the firm erodes—exactly the Bear Stearns / Lehman trap. The corpus's clean statement: *"Financial crises occur when the banking system is undercapitalized. For government authorities, the most direct way to fix an undercapitalization problem is by simply injecting [capital]"* (*Broad-Based Capital Injection Programs*).

So the tools split by diagnosis:
- **If genuinely a liquidity/funding run on solvent firms** → lender-of-last-resort funding backstops (à la the Fed's discount window, TAF, PDCF).
- **If a genuine capital hole** → the fix is **recapitalization**, potentially combined with **guarantees**, not liquidity.

## Lesson 3: An effective response usually requires the *combination* of funding, guarantees, and capital

Geithner: *"The mix of funding, guarantees, and capital that were essential in the last financial crisis will be as important in future financial crises. The absence of any one of these tools cannot practically be compensated for by the presence of the others."*

The capital-injection survey reinforces this: in 22 of its cases recapitalization was *combined* with a government guarantee of bank liabilities, and many argue the U.S. TARP capital program (CPP) *"did not stabilize the financial system alone—only when it was combined with a debt guarantee from the FDIC was the government able to calm financial markets."*

So if this metastasizes into a true systemic panic, the credible response is a *package*, not a single lever.

## Lesson 4: In an acute panic, be pre-emptive and err on the side of aggression — but only to protect the core

Geithner: *"If you establish the backstop after the run has too much momentum, then it will not be effective."* And: *"If you have full degrees of freedom … and the conditions suggest substantial risk of panic, then you want to err on the side of being aggressive sooner in providing credible protection against the catastrophic risk."*

But note the scope discipline: the Fed backstopped only the *most critical functions*—banks, primary dealers, GSEs, and key funding markets—**not** every specialty finance company. The equivalent question for you: are the threatened intermediaries systemically critical (core banks, key funding markets), or are they AI-focused specialty lenders and funds at the periphery? The answer determines whether aggressive backstopping is warranted or whether these firms should be allowed to fail.

## Lesson 5: Moral hazard is a real cost — but sequence it correctly

The corpus is nuanced: in the *acute* phase, "the over-riding priority is to stop runs… authorities need to prioritize the immediate behavior of creditors over the potential long-run moral hazard risks" (*Blanket Guarantees*). Punitive terms (executive-comp restrictions, penalty pricing) belong in the *later, structural* phase — "it behooves crisis-fighters to save the more punitive or costly design features for those later-stage responses" (*Ad Hoc Emergency Liquidity*). The CAP design offers a useful template: require capital shortfalls to be filled by *raising new capital*, not by *shrinking assets* (i.e., don't let banks meet ratios by cutting lending), and give firms a window to raise private capital before the government injects.

## Lesson 6: Beware the specific moral-hazard trap of *this* scenario

A distinctive danger here: if the government backstops AI-loan collateral or AI equity, it is not just insuring the financial system—it is effectively subsidizing a *specific technology bet that the market has just judged to be losing*. This is the corpus's warning about "removing the possibility of tail-risk scenarios" and encouraging market participants "to take excessive risk when they no longer internalize tail-risk scenarios" (*Central Bank Crisis Interventions*). Propping up AI valuations would signal that the government will absorb the downside of concentrated technology speculation. That is a policy the corpus's logic argues *against*.

## Lesson 7: Have the legal authority ready — don't try to legislate in the moment

Geithner's most durable lesson: *"If those tools are not available or require legislation in the moment, then the odds of a more severe crisis are much greater."* The Fed could lend (13(3)) but could not inject capital or guarantee liabilities without Congress—which is precisely why Lehman failed. Capital injections and broad guarantees typically require legislative authority (TARP was an act of Congress). If the government anticipates needing recapitalization or guarantee power, it should move to secure that authority *early*, in parallel with deploying the liquidity tools it already has.

---

## Recommended course of action

**Immediately:**
1. **Diagnose.** Have supervisors assess each stressed intermediary's exposure to AI collateral, the runnability of its funding, and its *viability* (not just paper solvency). Determine whether the problem is funding (liquidity) or a capital hole (solvency).
2. **Distinguish fundamental from fire-sale losses.** Do not backstop AI-equity or AI-collateral *values* — much of that decline is likely a fundamental, and possibly correct, repricing. The goal is to protect the financial system, not the AI-loan trade.

**If runs threaten solvent, systemically-important firms (liquidity problem):**
3. **Deploy lender-of-last-resort funding pre-emptively**, at penalty pricing with haircuts, scoped to the *core* of the system and key funding markets. Move before the run gains momentum.

**If the threatened firms have genuine capital holes (solvency problem):**
4. **Do not substitute liquidity for capital.** Push firms to raise private capital first, with a deadline; be prepared to inject public capital into *viable* systemically-important firms, and pair recapitalization with liability guarantees if a panic is spreading. Structure it CAP-style so firms fill holes by raising capital rather than cutting lending. Secure the necessary legal authority *now*, not mid-panic.

**Throughout:**
5. **Let non-viable, non-systemic AI-concentrated intermediaries fail** in an orderly way, using resolution tools. Backstopping the weakest is exactly what the corpus warns feeds moral hazard without protecting the core.
6. **Sequence moral-hazard controls:** stop the run first; impose punitive/structural conditions in the later phase.
7. Use **monetary and fiscal policy** to cushion the broader economy, recognizing (per Geithner) that even ample capital and funding can be overwhelmed without them.

The one-sentence synthesis from the corpus: **protect the core of the financial system aggressively and pre-emptively, match the tool to the diagnosis (capital for solvency, funding for liquidity, guarantees to stop panic), and resist the temptation to use the crisis apparatus to prop up AI valuations that the market may be correctly marking down.**

A caveat: the corpus is drawn from historical banking-centered crises. The AI-shock trigger, the role of possibly-fundamental technology-driven repricing, and the concentration of exposure in AI-focused lenders and funds are features these sources don't address directly, so the diagnostic step (Lessons 1–2) matters even more than usual here.