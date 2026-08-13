# Query 3 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 9}

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

I now have a solid, corpus-grounded basis for a recommendation. Here is my analysis.

## First, a caveat on the framing

The corpus is a body of research on financial-crisis interventions (largely drawn from the Global Financial Crisis and analogous episodes). Its lessons about **how governments should respond to solvency scares and feared liquidity crises at financial intermediaries** transfer well to your scenario. But note one key diagnostic point up front, because it shapes everything: the *trigger* here (a foreign AI breakthrough crashing AI-firm equity and loan collateral) is a **fundamental shock to asset values**, not a pure liquidity accident. The corpus repeatedly warns that "liquidity crises are rare in the absence of deeper-seated solvency or viability concerns" (*Ad Hoc Emergency Liquidity Programs in the 21st Century*). So this is likely a genuine solvency problem dressed up as a looming liquidity one — which affects which tools are appropriate.

## Step 1: Recognize you're in the "acute phase" — act fast, protect liabilities first

The *Broad-Based Emergency Liquidity Programs* survey frames crises as having two phases:

> "In the initial acute phase, the financial system has an obvious liquidity problem… but the underlying solvency of banks is difficult to judge in the heat of that moment… During this acute phase, policy responses need to be fast and emphasize protection of the fragile liabilities… The goal in this phase is to arrest runs and prevent fire sales. Any strict solvency condition is doomed to failure — there is simply no time to make such judgments."

**Implication:** Do *not* wait until you can perfectly sort solvent from insolvent intermediaries. In the acute phase the priority is to stop the self-reinforcing spiral — the "liquidity channel" contagion documented in the Lehman case studies, where firms facing higher haircuts and funding withdrawals dump assets, depressing prices further, impairing more balance sheets, and triggering more forced selling. Breaking that feedback loop is the immediate objective.

## Step 2: Deploy the lender-of-last-resort function — lend freely against collateral

The classic first tool is central-bank liquidity, following Bagehot's dictum — "lend freely at a high rate against good collateral" (*Early Phases of the Financial Crisis*). The intended aim is "to prevent an institution that is 'illiquid but solvent' from tipping into insolvency."

Two design lessons from the corpus are directly relevant here:

- **The collateral is the problem.** Your scenario is precisely the case the survey flags: "a liquidity constraint can easily disrupt the underlying assumptions and cause collateral to quickly lose value." Central banks can and do **adjust haircut schedules** for stressed collateral classes rather than mechanically applying peacetime schedules. But there's a limit — LOLR lending "cannot make viable the fundamentally nonviable," and it can only be extended "up to, but not in excess of, the value of the available security." If AI-company loan collateral has genuinely and permanently repriced, liquidity lending alone won't fix an intermediary that is actually insolvent.

## Step 3: Because this looks like a solvency shock, prepare capital and guarantees in parallel

The *Ad Hoc Emergency Liquidity* survey is explicit that liquidity programs "should not be expected to prevent or solve the chronic, or 'debt overhang,' phase," which "demands more structural policy responses — such as capital injections, liability guarantees, balance sheet restructurings, or orderly resolutions." Two tools stand out:

**(a) Guarantees to stop runs.** The GFC response leaned heavily on guarantees — deposit-insurance expansion, debt guarantees (the FDIC's DGP to restore interbank lending), transaction-account guarantees, and the money-market-fund guarantee that stopped the MMF run. The *Account Guarantee Survey* concludes guarantees "by and large fulfilled their foremost purpose of preventing open runs." A critical warning, though: guarantees "can cause a flight of funds from other parts of the financial system… that lack similar guarantees" — so design for **coverage of existing balances** and coordinate internationally to avoid simply moving the run elsewhere.

**(b) Capital injections for the genuinely undercapitalized-but-viable.** The *Broad-Based Capital Injection* survey stresses **triage via stress testing** — but with a crucial timing caveat: triage "is good practice in a chronic phase but may not be desirable (or even feasible) in an acute phase," and "capital injections will not achieve their goal… if the size and features of the program are based on a non-credible test." So: use guarantees and liquidity to buy time, then conduct a **credible stress test** to size and target recapitalization.

## Step 4: Consider targeted asset-market support to arrest the fire-sale spiral

Because the shock runs through collateral/asset prices, market-support facilities are relevant — the GFC's Commercial Paper Funding Facility, for example, provided a "liquidity backstop" that stabilized funding markets. Analogously, backstopping the specific funding markets that are seizing up can prevent forced liquidation of AI-linked assets at distressed prices. (The corpus also notes the debate over whether fair-value/mark-to-market accounting should be relaxed during fire-sale conditions — a possible supplementary measure, though contested.)

## Step 5: Attach conditions and an exit — but don't let them slow the rescue

Once you move into capital injections, the corpus supports **burden-sharing and conditions**: bans on dividends, share buybacks, and executive bonuses while public capital is outstanding; imposing losses on shareholders and subordinated/preferred creditors before taxpayers; pricing designed to incentivize prompt repayment; and a clear exit path (e.g., the Danish scheme's stepped-up repurchase price). Balance "generous vs. punitive": too punitive and firms won't participate (stigma); too generous and you create moral hazard and political backlash.

## Step 6: Communicate decisively and be willing to overwhelm

The lessons-learned interviews are unanimous on posture:
- **Confidence is the objective.** Bo Lundgren: "concrete moves to support confidence are key… Interventions create great expectations and panic can occur when these expectations are not adhered to." Half-measures that disappoint expectations are worse than nothing.
- **Keep it simple and pragmatic, but be bold** (Wojick).
- **Narrow the focus** — "first put out the fire and later ask how the fire started" (Malik). Don't try to fix the structural AI-lending problem mid-crisis.

## Summary recommendation

1. **Diagnose honestly:** treat this as a solvency shock manifesting as a liquidity fear, not a pure liquidity accident.
2. **Immediately (acute phase):** open/expand LOLR facilities with adjusted haircuts to solvent-but-illiquid intermediaries; stand up guarantees (debt/deposit/relevant funding markets) to halt runs and fire sales — protect liabilities first, don't demand strict solvency findings yet.
3. **Backstop the seizing funding markets** to stop the collateral fire-sale spiral.
4. **In parallel, prepare a credible, fast stress test** to triage viable-but-undercapitalized firms from nonviable ones.
5. **Recapitalize the viable** with burden-sharing conditions (dividend/buyback/comp restrictions, losses on shareholders and junior creditors first) and a clear repayment/exit path; **resolve the nonviable** in an orderly way rather than propping them up.
6. **Communicate overwhelming, credible force** and don't underdeliver on stated commitments.

One honest limitation: the corpus is centered on bank and near-bank intermediaries in past crises. To the extent the exposed lenders here are lightly regulated non-bank entities (as in the pre-GFC US "shadow" system the *Early Phases* piece describes), your legal authority to lend, guarantee, or inject capital may be constrained — the Fed's Section 13(3) allowed lending but "not… capital, or guarantee creditors against loss" — so a real-world response may require additional legislative authority, exactly as the corpus notes was needed in 2008.