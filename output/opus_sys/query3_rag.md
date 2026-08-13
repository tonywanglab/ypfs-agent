# Query 3 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: agent/system_prompt.md
Tool calls: {"search_corpus": 5}

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

I have enough to build a decision-useful plan. Before I do, one important reframe on your question's premise, per my analytical discipline.

---

# A Note on Your Framing (before the plan)

You've described this as a **"solvency" concern with a "liquidity crisis feared to come."** I'd gently reframe. What's actually happening is an **asset-price shock** (an AI-productivity surprise) that has repriced a collateral class — AI-company equity and the loans backed by it. The question at each affected intermediary is not "is it solvent on a mark-to-market snapshot today" (asset values are endogenous to how you respond and to how the panic evolves) but **"do creditors and markets believe it can continue as a going concern?"** — i.e., **viability**.

That distinction drives everything below, because it forces a **prior question you must answer first**: is the AI-equity collateral **oversold in a panic** (temporarily depressed, fundamentally viable), or has it been **fundamentally and permanently repriced** by a genuine technological shift? These call for opposite responses. Liquidity tools bridge a run; they do **not** fix a real, permanent loss of asset value — that is an equity/capital problem no amount of lending can solve.

---

# Summary of Core Design Dimensions

1. **Triage the shock, not the institutions first.** Determine whether the collateral repricing is a fundamental, permanent revaluation or a panic-driven overshoot. This is the "propping up a failed asset class vs. stepping into an oversold market" judgment the Bank of England explicitly flagged when it warned it did *not* want to "permanently underpin markets that were not fundamentally viable."
2. **Match the tool to the breadth of the shock.** A repricing that hits *several* intermediaries through a *common* asset class is a systemwide/broad problem, not a single idiosyncratic firm — which favors broad-based facilities and market-support tools over one-off rescues, at least initially.
3. **Liquidity bridges; capital repairs.** Emergency lending buys time. If the loss is real, the endgame is capital (recapitalization/restructuring), and moral-hazard/punitive terms belong *there*, not in the emergency loan.
4. **Lend freely; drop the penalty-rate reflex for targeted help.** For any *targeted* lending, a "sting" rate accelerates the drain and stigmatizes the borrower into a run. Penalty pricing may still suit a *broad backstop* everyone can use without a scarlet letter.
5. **Collateral flexibility with seniority protection.** You can lend against the disfavored asset class itself to stop fire sales, provided you take seniority and can be patient.

---

# Program Archetypes

## Option 1 — Broad-Based Backstop First (the default given a *common* shock)
Because the same collateral class is stressing *multiple* intermediaries simultaneously, the cleanest first move is a **broad-based facility** open to all eligible institutions, with expanded collateral eligibility and (optionally) a market-support facility targeting the specific stressed asset. Making the facility broad-based avoids branding any one borrower as the weak link, and pricing can carry a modest premium without triggering stigma precisely because everyone can use it. In the GFC, central banks repeatedly widened collateral schedules and coordinated broad facilities to precisely this end. This is the least intrusive, fastest-to-deploy option and is usually implementable under existing authority.

- **Use when:** the shock looks like a liquidity/fire-sale spiral in an *oversold* market and no single firm is yet at the point of failure.
- **Caution:** if the collateral is *fundamentally* impaired, a broad facility just delays recognition and risks "permanently underpinning" a genuinely repriced asset.

## Option 2 — Targeted Ad Hoc Liquidity to a Systemic Institution (bridge)
If one or two intermediaries are **individually systemic** — by size *or interconnectedness* — and cannot get enough from broad facilities (insufficient eligible collateral, or non-bank status), a bespoke emergency line is warranted. The canonical analogue is the **Fed's $85B Revolving Credit Facility for AIG**, a leveraged non-bank hit by collateral calls in a market panic: the Fed took the *whole business* as collateral (equity in viable operating subsidiaries) and secured seniority via a Guarantee and Pledge Agreement ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]). The systemic-importance test itself — "too interconnected to fail," judged at the moment of crisis rather than ex ante — is exactly the AIG/Bear logic you'd apply to an AI-lending intermediary that turns out to be a hidden hub.

- **Design terms:** lend freely, size it generously (undersizing is the most common documented mistake), *avoid* a punitive rate that would accelerate the drain, take flexible collateral with **seniority**.
- **Caution:** the AIG RCF was initially priced too punitively and had to be restructured — a direct warning against baking moral-hazard "stings" into the emergency loan.

## Option 3 — Fiscal Collateral Swap / Bridge-to-Recapitalization (when collateral is genuinely impaired)
If the AI-collateral loss is **real and permanent**, lending alone can't fix the resulting hole; you need the fiscal authority. The **Latvia–Parex** model is instructive: the Treasury placed government securities as term deposits at the bank, which the bank then posted as collateral to borrow cash from the central bank — a fiscal swap that upgraded unusable collateral into central-bank-eligible collateral, explicitly as a **bridge to restructuring** (good-bank/bad-bank split and recapitalization) ([vol7_iss1_13][Latvia: Parex Bank Emergency Liquidity Program, 2008][case_study][2025-04-15]). This is where moral-hazard discipline properly lives: government took control, wiped out shareholders, and imposed conditions.

- **Use when:** the intermediaries are non-viable at current asset values and need *equity*, not just time.
- **Caution:** watch the **bank-sovereign nexus** — Parex-style swaps shift counterparty risk onto the sovereign and can accrete to a sovereign problem (as in Ireland–Anglo Irish).

---

# Complementary Considerations

- **Answer the triage question explicitly and honestly.** Recursive self-improvement without Nvidia is a genuine *technological* signal, not a pure funding accident. That raises real odds this is a **permanent repricing**, which tilts you *away* from Option 1's "step into an oversold market" and *toward* recognizing losses and Option 3's capital repair. Do not let liquidity tools disguise a solvency problem.
- **Language discipline is a policy tool.** Publicly labeling these intermediaries "insolvent" can itself trigger the run you fear. Frame official communication around viability and the backstop's availability.
- **Sequencing.** Liquidity first to stop the run (Options 1/2), capital/restructuring second to fix the hole (Option 3). Moral-hazard and punitive terms attach to the *second* stage.
- **Sizing.** Across the capital-injection and liquidity literature, the recurrent failure is going too small. Announce capacity generously.
- **Simplicity in the acute phase.** Complex, conditional programs invite counterparties to run; keep acute-phase terms simple.
- **You are not the only central bank.** A US AI-equity shock has global holders; coordinate, as GFC central banks did.

# Suggested Framing for Your Principal

> "This is an asset-price/collateral shock transmitting through the intermediaries that lent against AI equity. Our first decision is diagnostic, not financial: **is this collateral oversold in a panic, or genuinely and permanently repriced by the technology news?** If the former, a broad-based backstop with widened collateral eligibility arrests the fire sale at low cost and low stigma. If the latter — which the nature of this shock makes plausible — liquidity only buys time, and the real fix is capital: targeted bridges to systemically interconnected firms (AIG-style, generously sized, non-punitive, senior-secured), backstopped by a fiscal recapitalization/restructuring path (Parex-style) where firms are non-viable. We save moral-hazard conditions for that capital stage, not the emergency loan. Under no framing should we describe these firms as 'insolvent' publicly — that invites the run we're trying to prevent."

Would you like me to (a) develop the triage test — what signals distinguish an oversold panic from a permanent repricing — or (b) draft detailed term sheets for any one of the three archetypes?