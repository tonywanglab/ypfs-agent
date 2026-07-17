# Query 3 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 5}

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

I now have a strong evidentiary base. Let me synthesize the corpus lessons into a coherent, phased answer tailored to your scenario.

---

## Framing the scenario

Your scenario has three distinct problems, and the corpus is emphatic that conflating them leads to bad policy:

1. **An asset-price shock** — U.S. AI equities crash on news of a Chinese recursive-self-improvement breakthrough. This is a repricing of fundamentals, not a market failure per se.
2. **A collateral / potential liquidity problem** — loans backed by AI-company collateral fall in value, funding markets may seize as lenders hoard and haircuts rise.
3. **A potential solvency problem** — several intermediaries may be genuinely underwater once the collateral is honestly marked.

The single most important lesson from the corpus is that **the right tool depends on which of these you actually face**, and that acute liquidity problems and chronic solvency problems require completely different instruments deployed in sequence.

---

## Step 1: Do *not* treat a fundamental repricing as a crisis to be reversed

A critical caution first. The corpus repeatedly notes that financial crises are "typically preceded by credit booms, though not all credit booms end in a crisis" (Ireland/Iceland case). If AI-company valuations were inflated and the Chinese announcement simply reveals that Nvidia-dependent business models are less valuable than believed, then **the fall in equity and collateral values is a correction of fundamentals, not a liquidity failure.** Government intervention to prop up those asset prices would be misguided—it would prevent price discovery, protect equity holders who took the risk, and create moral hazard.

The market liquidity program survey (`vol2_iss3_2`) is careful to define its remit as stabilizing *funding markets under stress*, not defending the price level of a specific asset class. The government's job is to prevent a *disorderly* unwind and contagion, **not** to reverse the revaluation of AI companies.

So the threshold question is: *Is there genuine contagion into systemically important funding markets and intermediaries, or is this contained pain for AI-sector investors?* Only the former justifies intervention.

---

## Step 2: In the acute phase, protect fragile liabilities — lend freely (modernized Bagehot)

If a genuine run / funding freeze is developing at systemically important intermediaries, the corpus is clear about the first response. From `vol4_iss2_3` (Broad-Based Emergency Liquidity Programs), the modernized dictum is:

> *"In the acute (panic) phase of a crisis, a LOLR should lend freely and broadly against good collateral, at rates set by auction, taking care to avoid disclosing details about individual borrowers."*

Key design points from the corpus:

- **Lend freely and broadly.** Timothy Geithner's essay (`vol1_iss1_1`) stresses that in a modern system where *nonbanks* and direct funding markets matter, the LOLR must reach beyond banks. The TSLF example (`vol2_iss2_3`) is directly analogous to your scenario: it let dealers **swap illiquid collateral the market refused to fund against for Treasuries**, breaking the "vicious dynamic" of "margin calls → forced liquidation → lower prices → higher haircuts → more fire sales." If AI-collateral-backed lending is seizing, a collateral-swap facility is the natural tool.

- **"Good collateral" is judged at pre-panic values.** The survey stresses that "good" collateral for Bagehot "referred to the status of that collateral before the panic began." This is exactly the mechanism for distinguishing a *temporary* fire-sale discount from a *permanent* fundamental revaluation—but note the danger: if the AI-collateral decline is *fundamental*, lending against pre-shock values means taking real credit risk.

- **Don't over-engineer moral-hazard penalties in the acute phase.** The Ad Hoc Emergency Liquidity survey (`vol7_iss1_3`) finds that of "lend freely, against good collateral, at a penalty rate," often *only "lend freely" survives in practice*. Penalty rates during a run can *accelerate* the drain on an institution and be punished by the market and rating agencies. Auctions are the best way to get penalty-like pricing with minimal stigma (`vol4_iss2_3`). Save punitive terms for the later structural response.

- **Minimize stigma / protect confidentiality** during the acute phase; disclose later to serve taxpayers and address moral hazard.

**Crucially, liquidity does not fix insolvency.** As `vol4_iss2_3` states: "Solvency is ultimately an equity problem and *cannot be solved* simply by lending." Lending buys time; it does not repair a hole in the balance sheet.

---

## Step 3: Assess solvency honestly — the illiquidity vs. insolvency judgment

Once liquidity has bought time, the government must determine which intermediaries are merely illiquid and which are genuinely insolvent.

The corpus pushes back hard on the fatalistic claim that this is impossible. Paul Tucker's article (`vol2_iss2_1`) argues that while it is "at times nearly impossible" to distinguish solvency from liquidity problems, it is usually **"a prosaic task, requiring a team and good organization"**: value the assets, ask how much you'd lend against more and more of them, and if the borrower "has not got assets that would cover more than a modest fraction of its liabilities, it becomes likely that it has solvency problems."

The mechanism to operationalize this is the **stress test** (`vol4_iss2_39` on Greek ELA restricting to solvent/viable banks; and the U.S. SCAP case). Note the `vol5_iss3_1` "signal extraction / zombification" concern: lending indiscriminately to insolvent institutions creates zombies and destroys central-bank credibility. An independent central bank should *not* knowingly lend to fundamentally insolvent firms.

---

## Step 4: For the chronic (solvency) phase — recapitalization, guarantees, or asset removal

If the stress test reveals genuine capital holes, the corpus offers a menu, and the U.S. GFC experience (Matthew Kabaker, `vol3_iss3_39`; the 2009 stress test case `vol2_iss1_5`) is the clearest playbook:

1. **Diagnose correctly.** Kabaker: by late 2008 "it was increasingly clear... that we had a solvency, not a liquidity crisis, and that the solvency response... was not having an effect on the perception of solvency." Don't keep applying liquidity tools to a solvency problem.

2. **Use a public stress test to create clarity and crowd in private capital.** The SCAP/CAP combination worked because of two elements: (a) transparency on losses in tail scenarios, and (b) a government backstop—"if they met the test, the bank would survive... there is no bigger volatility-reducing exercise than that." The aim is to make the sector *investable* again with **as little public capital as possible**, letting private capital do the recapitalization.

3. **Capital injections** where private capital cannot fill the gap (TARP CPP). These are "the most direct method to solve an undercapitalization problem," but "both fiscally and politically expensive" (`vol6_iss3_1`).

4. **Guarantees** as a complement—they create only *contingent* liabilities and are politically more palatable. But note: a *liability* guarantee addresses a liquidity/run problem, not solvency; if the market worries about *asset quality* (very plausible with impaired AI-collateral loans), you may need **asset guarantees** or ring-fencing (the Citi/BofA loss-sharing structures in `vol6_iss3_1`).

5. **Asset removal / "bad bank."** If impaired AI-linked assets are clogging balance sheets and preventing markets from believing recaps will restore solvency, an asset-management-company approach (Ireland's NAMA, `vol3_iss2_26`) can remove them—though NAMA's mixed record shows it is no panacea.

---

## Step 5: Manage moral hazard, timing, and communication

- **Package and sequence.** `vol6_iss3_1` shows capital injections almost always work alongside ELA, guarantees, and resolution/restructuring—not as standalone measures.
- **Speak with one voice.** Kabaker stresses that Treasury, the Fed, and the FDIC must not run competing tests or send mixed signals; "one capital 'bogey'" and a shared narrative were essential.
- **Address moral hazard in the chronic phase, not the acute one** (`vol4_iss4_4`): use behavioral restrictions (dividend/buyback bans, comp limits, heightened supervision) *after* stabilization, and impose losses on the right parties. The Blanket Guarantee and dividend cases (`vol4_iss2_1`) show that letting failing firms keep paying out equity holders while backstopped by the public is exactly the transfer to avoid.
- **Resolution for the truly insolvent.** Volcker (`vol2_iss2_7`) notes Orderly Liquidation Authority "deals with the stockholder problem"—wipes out equity, bails out debt where necessary. Flowers (`vol7_iss1_29`) cautions that in a genuinely *systemic* event, governments will (and, he argues, must) backstop core institutions regardless of "too big to fail" rhetoric.

---

## Bottom line: what the government should do

1. **Don't defend AI equity prices.** Let the fundamental revaluation happen; that is not the government's problem to fix.
2. **Diagnose contagion.** Only intervene if the shock is genuinely spilling into systemically important funding markets and intermediaries.
3. **Acute phase — lend freely.** Provide broad-based, minimally-stigmatized liquidity (including a TSLF-style collateral-swap facility) to arrest runs and stop the fire-sale/haircut spiral. Reach nonbanks if they are systemic. Don't obsess over penalty rates now.
4. **Assess solvency** via a credible, transparent stress test. Distinguish the illiquid from the insolvent—this is a hard but doable task.
5. **Chronic phase — fix capital.** Use the stress test to crowd in private capital with a government backstop; deploy targeted capital injections, asset guarantees, and asset-removal only as needed for genuinely undercapitalized-but-viable firms; resolve the unviable ones, imposing losses on equity (and where appropriate, unsecured debt) holders.
6. **Throughout:** coordinate agencies, communicate with one voice, and defer moral-hazard penalties to the stabilization/chronic phase.

The overarching lesson from the corpus: **liquidity tools buy time but cannot repair balance sheets; solvency problems require equity (fiscal) solutions**—and the great error is applying one when you face the other.

**Two caveats on the mapping.** First, the corpus is built on crises where the fall in collateral value was largely a *panic-driven* fire-sale discount that later reversed. If the AI-collateral decline reflects a *permanent* technological obsolescence of Nvidia-dependent businesses, then "lend against pre-panic collateral values" means the government is knowingly taking real losses—closer to a bailout than classic LOLR, and that argues for faster movement to honest recapitalization/resolution and loss-recognition rather than prolonged liquidity support. Second, none of the sources address an AI-specific shock directly; I've reasoned by analogy from asset-price-shock-driven intermediary crises, which is the closest available precedent.