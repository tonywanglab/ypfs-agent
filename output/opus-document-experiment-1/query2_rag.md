# Query 2 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 9, "get_document": 1}

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

I now have all the pieces I need to give a well-grounded answer.

# What should the government do?

## The nature of this crisis

The distinctive feature of your scenario is not the fund loss itself, but the **informational contagion** it triggers. Because the exact pattern of bank exposures to the failed fund is unknown, depositors and creditors can't tell which banks are safe. Two mechanisms are at work simultaneously, and the corpus describes both:

- **Confidence/correlated-information contagion**: When investors can't distinguish healthy from exposed banks, "it is easier for investors to abandon that firm rather than figure out its true situation" (Lehman Brothers H, *Global Contagion*). One failure "makes many," in Bagehot's phrase.
- **Liquidity/fire-sale contagion**: Banks selling assets to meet withdrawals push down prices, which impairs *other* banks holding the same assets — a "downward spiral in overall market liquidity" that can turn a solvency problem at two banks into a solvency problem across the sector.

The runs are therefore partly rational (some banks really are exposed and possibly insolvent) and partly self-fulfilling (solvent banks can be taken down purely by the *expectation* that others will run — the classic Diamond-Dybvig logic described in *Containing Runs on Solvent Banks*). This dual character dictates the response: you cannot treat the whole sector as either solvent or insolvent, and you cannot rely on any single tool.

## The core problem: you don't yet know who is insolvent

The central lesson across the corpus is that **liquidity support and solvency support solve different problems, and you must not confuse them**:

> "Lending can help reduce the risk that the strong become illiquid, but it cannot make viable the fundamentally nonviable." (*Reflections on the Lender of Last Resort*)

So the government's first job is **triage** — separating the merely-illiquid-but-solvent banks (which should be kept alive) from the genuinely insolvent ones (which must be recapitalized or resolved). But triage is hard mid-panic: solvency "depends on the value of the assets… These are particularly hard to assess in the midst of a crisis." That tension shapes the sequence below.

## A layered, escalating response

The corpus repeatedly stresses that no single instrument suffices; you need a "framework for escalation," deploying tools **preemptively** because "if you establish the backstop after the run has too much momentum, then it will not be effective."

**1. Lender of last resort — provide liquidity first, and broadly.**
Have the central bank lend freely against good collateral to banks facing outflows (Bagehot's dictum). This is the fastest tool and directly counters the fire-sale channel: if banks know they can borrow to replace lost funding, they won't dump assets, and creditors who know a backstop exists are less likely to run. Crucially, because the shock originated in a **fund** (a nonbank), watch whether the run spreads through nonbank funding channels (money-market-fund-style runs, dealer funding) — the LOLR may need to reach beyond banks, as the Fed found it had to in 2008. But LOLR alone "cannot make up for a lack of adequate capital, and it does not have the force of a guarantee."

**2. Diagnose exposures with a transparent, coordinated stress test.**
This is arguably the most important step given that *the crisis is driven by uncertainty about exposures*. The 2009 U.S. SCAP is the paradigm: a simultaneous, consistent assessment of the largest banks under an adverse scenario, with **public disclosure of results**. Its explicit purpose was "reducing uncertainty and restoring confidence." Applied to your situation, a supervisory exercise that quantifies each bank's exposure to the fund (and to correlated assets) and publishes the results directly attacks the informational root of the runs — it lets depositors distinguish safe banks from exposed ones, so runs stop on the healthy majority. A caveat from *Stress Tests and Policy*: transparency is "a double-edged sword" — in a live panic, publishing a bad result can spark the very run you fear, so disclosure must be paired with a credible capital backstop (below) so that a "shortfall" comes with an immediate remedy rather than a death sentence.

**3. Recapitalize the solvent-but-undercapitalized banks; resolve the truly insolvent.**
For banks the stress test finds short of capital but viable (this may include your two regional banks if their fund losses are survivable), provide a capital backstop. The SCAP/CAP model works well: give banks a window to raise **private** capital, with a government facility standing behind them for any shortfall. This design largely destigmatized participation and, in 2009, meant almost no public capital was actually drawn. For banks found genuinely insolvent, use **resolution** rather than throwing good money after bad — recapitalization is "a gamble that leads to even larger expected fiscal losses" if the bank isn't viable. Note that recapitalization is "often ineffective without an NPL strategy" — so pair it with a plan for the impaired fund-related assets.

**4. Consider a guarantee — but scaled to what you can credibly back.**
If liquidity + diagnosis + recapitalization don't calm the runs, a **guarantee of bank liabilities** (deposits and possibly other short-term funding) directly removes the incentive to run by eliminating exit as "a one-way sure bet." The 2008 U.S. Temporary Liquidity Guarantee Program and the broader Blanket Guarantee survey are the references here. But the corpus is emphatic about the constraints:
   - **Credibility depends on fiscal capacity.** A guarantee "too large relative to fiscal resources" fails and can bankrupt the sovereign — the Irish 2008 blanket guarantee is the cautionary tale. Do not guarantee more than your government can actually pay.
   - **A guarantee doesn't fix underlying problems** — it must be paired with liquidity support and restructuring.
   - **Manage moral hazard**: restrict guaranteed banks' behavior during the acute phase (interest-rate caps, no aggressive marketing) and ramp up supervision.
   - Prefer a **targeted** guarantee (matched to the actual run pressure) over an unlimited blanket guarantee if fiscal room is limited.

**5. As a true last resort: a bank holiday / withdrawal restrictions.**
If runs continue despite the above and you simply cannot complete triage fast enough, a temporary **bank holiday** is the "high-risk… measure of last resort" that stops the run and buys time. Its value is precisely that it "allows for the implementation of a coordinated response." Two lessons apply directly here:
   - **Reopen only viable banks** (recapitalizing them first), so runs don't immediately restart; keep the insolvent ones closed for resolution.
   - If you can't resolve the distress quickly, reopen with **withdrawal restrictions** to control activity until full resolution.
   - Announce it **short and extend if needed** rather than announcing a long shutdown (as Cyprus 2013 and Greece 2015 did). Notably, because the shock here **originated outside the banking system** (the fund), "stigma and contagion may be more contained… and trust in the banks less damaged when they reopen," since the government's focus is visibly on the external problem.

## Communication and political backing run through everything

Two cross-cutting requirements: **clear, credible communication** (a muddled message amplifies runs), and **political/legislative support**, since guarantees and capital injections carry "potentially substantial fiscal costs, which authorities may be unable to quantify at the time of the announcement." In practice this may require emergency authority from the legislature, as the U.S. needed TARP/EESA before it could deploy capital and broad guarantees.

## So, "what, if anything"?

Doing nothing is not advisable: self-fulfilling runs can take down solvent banks and inflict real economic damage (the FDIC estimated even a 5% uninsured-deposit run could cut GDP growth ~2%). But the government should **not** simply bail everyone out. The right posture is a **graduated, conditional response**:

1. **Immediately**: open the LOLR to stem fire sales and buy time.
2. **Quickly**: run a transparent stress test to identify who is actually exposed/insolvent — this attacks the informational root of the panic.
3. **In parallel**: stand up a capital backstop so the diagnosis comes with a cure (private capital first, public as backstop), and resolve genuinely insolvent banks.
4. **If runs persist**: add a fiscally-credible guarantee with moral-hazard safeguards.
5. **Only if all else fails**: a short bank holiday, reopening only recapitalized/viable banks, possibly with withdrawal limits.

The guiding principle throughout: **support liquidity for the solvent, force loss-recognition and resolution on the insolvent, and resolve the uncertainty about exposures** that is the true driver of the sector-wide runs.