# Query 3 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: agent/system_prompt.md
Tool calls: {"search_corpus": 5, "get_document": 1}

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

I have what I need. Here is the decision-useful analysis.

---

# Summary of core design dimensions

First, a framing note on your terminology. You've described "solvency concerns" driven by a **collateral repricing**, with "a liquidity crisis feared to come." Per our analytical framework, I'd reframe the central question away from solvency/liquidity and toward **viability**: do creditors and counterparties believe the affected intermediaries can continue as going concerns, inclusive of expected official action?

This distinction matters because the shock you describe is fundamentally a **repricing of a collateral asset class** (AI-company equity and AI-company loans), not a revelation that the intermediaries themselves are broken businesses. That closely mirrors the GFC pattern, where asset values on the balance sheet became temporarily impossible to value and short-term funding began to run. The critical judgment for your principal: is AI-linked collateral genuinely *oversold* in a panic (in which case a liquidity backstop can put a floor under it and buy time), or is this a **permanent revaluation** of a franchise the market has correctly abandoned (in which case lending merely delays a solvency reckoning and props up a "market that was not fundamentally viable")? A central bank should be confident it is "stepping in as emergency liquidity provider in an oversold market, rather than propping up a failed asset class."

The core design dimensions across all options below:
1. **Breadth** — market-wide/broad-based vs. targeted to named intermediaries;
2. **Instrument** — cash-for-collateral, securities-for-securities, or asset purchase;
3. **Collateral treatment** — what you accept, and at what haircut;
4. **Pricing** — backstop/penalty vs. accommodative;
5. **Sequencing** — emergency liquidity first, structural (capital/guarantee) measures later.

# Program Archetypes

## Option 1: Broad-based, securities-for-securities backstop (the "buy time without adding cash" option)

Lend high-quality government securities against the now-distressed AI-linked collateral, on a market-wide basis, through auctions to a defined class of counterparties. This is the closest analogue to the Fed's **Term Securities Lending Facility (TSLF)**, which lent up to $200bn of Treasuries against collateral "that was relatively illiquid at the time," specifically to head off fire sales in the repo market and restore financing-market liquidity ([vol2_iss3_8][Term Securities Lending Facility (TSLF) (U.S. GFC)][case_study][2020-10-08]).

Key design features worth borrowing:
- **Tiered collateral schedules with calibrated pricing.** The TSLF ran "Schedule 1" (routine collateral) and "Schedule 2" (broader, less-liquid collateral at a higher minimum bid) "to better calibrate the interest rate on TSLF loans to the level of risk associated with the collateral" ([vol2_iss3_8][Term Securities Lending Facility (TSLF) (U.S. GFC)][case_study][2020-10-08]). You could place AI-linked collateral in the riskier tier.
- **Auction format to suppress stigma.** Awarding through auction was chosen precisely to "encourage broad participation and avoid any stigmatization," with borrower identities undisclosed during operation and borrowing caps ensuring spread across institutions ([vol2_iss3_8][Term Securities Lending Facility (TSLF) (U.S. GFC)][case_study][2020-10-08]).
- **Self-liquidating design.** Minimum bid rates were "set to be attractive when markets were disrupted but unattractive when markets functioned well" — the facility naturally falls into disuse as conditions normalize.
- **Progressive collateral expansion.** As stress intensified around Lehman, the Fed widened eligible Schedule 2 collateral to all investment-grade securities — a template for staged escalation if the AI shock deepens.

Advantage over cash lending: securities-for-securities "did not affect the supply of bank reserves," so it can be scaled up/down without complicating monetary policy. This is the least-intrusive first move.

## Option 2: Indirect asset purchase to restart the frozen collateral market (the "reopen the market" option)

If the problem migrates from *funding* the intermediaries to a *shut* market for AI-linked credit/securities (no new issuance, spreads blown out), a facility modeled on the **Term Asset-Backed Securities Loan Facility (TALF)** targets the market rather than the institutions. TALF extended term, largely non-recourse loans to *investors* to buy high-quality asset-backed securities, reopening a market that had "come to a near halt," while the Fed took risk only in the loss of collateral value and let private investors bear first loss ([vol2_iss3_11][The Term Asset-Backed Securities Loan Facility (TALF) (U.S. GFC)][case_study][2020-10-08]).

Salient design points:
- **Fiscal first-loss backing.** TALF was explicitly a Fed–Treasury partnership, with Treasury capital (from TARP) absorbing losses — the mechanism that let the central bank lend against an asset class it was uncertain about ([vol2_iss2_6][The Federal Reserve's Financial Crisis Response E: The Term Asset-Backed Securities Loan Facility][case_study][2020-07-16]).
- **Haircuts as the risk control**, with private capital absorbing initial losses, so the government's exposure is remote.
- **Deliberately narrow eligibility.** TALF focused on "securities that will have the greatest macroeconomic impact and that could most efficiently be added … at a low and manageable risk to the government," and it *excluded* the most-tainted assets ([vol2_iss2_6][The Federal Reserve's Financial Crisis Response E: The Term Asset-Backed Securities Loan Facility][case_study][2020-07-16]).

This is the right archetype only if the shock threatens the *flow of credit through the securitization/market channel*, not just a handful of balance sheets. Its downside is complexity — TALF took four months from announcement to first subscription — so it is a chronic-phase tool, not an acute-phase firebreak.

## Option 3: Ad hoc emergency liquidity to named, systemic intermediaries (the "firebreak for a specific institution" option)

If one or a few intermediaries are so concentrated in AI-linked exposure that they face an imminent run before any broad facility can be stood up, targeted ad hoc emergency lending is the tool — but with important design discipline.

- **Collateral: take the whole business, or the best exit-linked assets.** In acute cases lenders "loosen their collateral eligibility requirements as much as necessary." When the Fed lent to AIG it "primarily took as collateral the holding company's stakes in its operating subsidiaries, which the Fed viewed as having ongoing viability" ([vol7_iss1_3 discusses; cite the underlying case] — see US–AIG RCF). You would lend against the intermediary's viable non-AI franchise, not the impaired AI collateral itself.
- **Seniority as balance-sheet protection.** Where collateral can't be posted fast enough, lenders have taken preferential rights in bankruptcy instead — the SNB's approach with Credit Suisse and the Fed's with Signature both used subordination/priority rather than waiting on collateral transfer.
- **Pricing: resist the urge to "make it sting."** This is the most important lesson for your scenario. Punitive rates are counterproductive in targeted lending: usage is *already* disincentivized by stigma and supervisory scrutiny, and a high rate can "make survival of the institution … less likely." Both **Latvia–Parex** and **US–AIG RCF** imposed punitive rates and had to *reverse* them to arrest further deterioration — AIG's initial LIBOR+850bps was cut (first by 550bps) once it "portended further credit rating downgrades" ([vol7_iss1_3 survey discussion; cite US–AIG RCF and Latvia–Parex case studies]). Lend freely; handle moral hazard later in the structural phase.

The tradeoff: ad hoc lending brands the borrower and can itself signal distress. Use only when a specific institution's failure is the systemic threat and speed is paramount.

# Complementary Considerations

- **Watch the language.** Publicly framing this as "insolvency" among intermediaries risks *manufacturing* the run you fear. Bad verbiage ("insolvent") can trigger panic even where the underlying businesses are viable. The AI shock has repriced *collateral*; it has not necessarily made the intermediaries nonviable. Communications should describe a collateral-repricing event and a liquidity backstop, not a solvency crisis.

- **Liquidity cannot fix solvency.** If, on examination, some intermediaries are genuinely non-viable once AI exposures are marked, no amount of lending resolves that — a capital problem needs equity, delivered in the chronic phase via capital injections, guarantees, or restructurings. Sequence accordingly: emergency liquidity to arrest the run *now*, structural tools *later*, with moral-hazard terms attached to the structural interventions rather than baked into the emergency loan.

- **Where to draw the moral-hazard/penalty-rate line.** A *penalty rate is appropriate for the broad-based backstop* (Options 1/2) — it ensures the facility recedes as markets normalize. It is *not* appropriate for targeted lending (Option 3). Don't conflate the two.

- **Pre-positioned authority and speed.** The BoE's ECTR was valued precisely because it could be activated for "actual or prospective market-wide stress" *before* the need fully materialized ([vol4_iss2_51][United Kingdom: Extended Collateral Term Repo Facility][case_study][2022-07-18]). If your principal has standing emergency authority, the ability to move pre-emptively is itself a stabilizer.

- **Distinguish the genuinely oversold from the genuinely broken.** The novel wrinkle here is that the shock is a *technological* revaluation (a credible substitute for the incumbents' core asset — compute/Nvidia dependence). Unlike GFC housing, where prices were plausibly temporarily depressed, part of the AI equity decline may be a *permanent* repricing. The BoE's own caution applies with force: avoid "permanently underpinning the existence of markets that were not fundamentally viable." A liquidity backstop is defensible to prevent a *disorderly* fire-sale cascade; it is not defensible as a floor under a genuinely obsolete valuation.

# Suggested Framing

Advise your principal to think in two phases and to reframe the presenting problem:

1. **Acute phase — arrest the run, buy time (days).** Lead with the **broad-based securities-for-securities backstop (Option 1)**: it is fast, reserve-neutral, self-liquidating, auction-based (low stigma), and puts a floor under the collateral without committing the government to a permanent view on AI valuations. Reserve **Option 3** for any single intermediary whose failure would be systemic before the backstop is operational — and if used, lend against its *viable* franchise, take seniority, and price accommodatively, not punitively.

2. **Chronic phase — resolve viability (weeks/months).** Only after the run is arrested, assess which intermediaries are genuinely non-viable once AI exposures are honestly marked. Address those with capital and restructuring tools, where moral-hazard conditions belong. Deploy an **Option 2 (TALF-style)** market-restart facility *only if* the AI-credit market itself stays frozen and that freeze is choking real-economy credit — and back it with fiscal first-loss capital.

The one judgment your principal cannot delegate to any facility design: **is AI-linked collateral oversold in a panic, or correctly repriced by a genuine technological shift?** Every option above is justified in the first case and hard to justify in the second. I'd recommend commissioning a rapid viability assessment of the most-exposed intermediaries in parallel with standing up Option 1 — the backstop buys the time to answer that question without prejudging it.

*A caveat on sourcing:* the TSLF and TALF precedents are strong structural analogues but arose from a housing/securitization shock; the technological-substitution character of your scenario has no clean corpus precedent, so the "oversold vs. obsolete" judgment is where I'd want your principal's sector expertise to override any historical template. I can pull the full AIG RCF or Latvia–Parex case studies if you'd like the granular pricing and collateral mechanics for Option 3.