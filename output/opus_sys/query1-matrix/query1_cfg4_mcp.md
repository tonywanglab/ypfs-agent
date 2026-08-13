# Query 1 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: agent/system_prompt.md
Tool calls: {"search_corpus": 4, "get_document": 1}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I have what I need. The AIG case is a direct analogue—a globally significant insurer hit by a shock, downgraded, facing collateral-call/counterparty runs, seeking government help—and it carries clear lessons that map onto your terminology framework. Here is my recommendation.

---

# Summary of Core Design Dimensions

Before choosing an instrument, resolve the questions that actually determine the outcome. Note first a reframing: this is being described as a "short-term liquidity crisis," but a rating downgrade plus investor flight is almost always the market rendering a **viability** judgment, not a standalone plumbing problem. The disaster losses have raised doubts about whether the insurer can continue as a going concern; the funding run is the *symptom*, not the disease. Treat "liquidity crisis" accordingly.

The core dimensions to decide:

1. **Viability determination (the gating question).** Is the insurer viable as a going concern—inclusive of any support you are prepared to commit? Distinguish the healthy core insurance operations (typically stable, cash-generative, saleable) from the specific pocket of disaster losses driving the run. In the AIG case, the authorities' entire willingness to lend rested on a judgment that the insurance subsidiaries were "stable enough and valuable enough to support a loan large enough to prevent default" ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]). If your insurer's core franchise is sound and only the catastrophe pocket is impaired, that supports viability.

2. **Systemic importance.** Emergency assistance to a single firm is only justified by systemic importance—size, interconnectedness, or the risk that its failure triggers contagion in the acute environment. Confirm this is truly "too interconnected/systemic to fail," not merely a large private loss.

3. **Collateral.** What good collateral exists? The insurer's regulated subsidiaries and their equity are the natural candidates. A well-collateralized loan neutralizes most solvency and moral-hazard worries because you can sell the collateral if things go wrong.

4. **Liquidity vs. structural need.** Emergency liquidity only buys time. It does not cure a run. Decide up front what the *structural* follow-on will be (capital injection, guarantee, run-off/restructuring of the loss pocket, or sale).

5. **Pricing and stigma.** Resist "make it sting" instincts—see the Complementary Considerations.

---

# Program Archetypes

## Option 1: Secured emergency credit facility, bridging to a structural fix (recommended baseline)
A collateralized revolving or term facility sized to cover potential short-term outflows, secured on the insurer's assets and the equity of its regulated subsidiaries, explicitly framed as a bridge to a permanent solution.

This is the AIG template. The Fed extended an $85B Revolving Credit Facility secured on substantially all of AIG's assets, including the stock of its insurance subsidiaries, to stop the collateral-call/securities-lending run and to "make appropriate dispositions of certain assets over time" ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]).

Two hard lessons from that case that should shape your design:
- **Liquidity alone did not cure the run.** Despite the large facility, AIG's counterparty outflows and downgrade pressure continued; the RCF "was insufficient to stabilize AIG" and the situation only stabilized once structural measures followed—a $40B capital injection and the Maiden Lane III vehicle that purchased the CDO exposures and cancelled the loss-generating contracts, ending the collateral calls ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]; [vol3_iss1_6][The Rescue of American International Group Module E: Maiden Lane III][case_study][2021-04-16]). For your insurer, the analogue is a mechanism to ring-fence or run off the disaster-loss pocket.
- **The facility's own terms can trigger further downgrades.** The large loan raised AIG's leverage and the punitive rate hurt its interest-coverage ratio, making a *further* downgrade more likely and forcing the authorities to restructure within weeks ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]). Design the facility so it does not itself worsen the metrics the rating agencies watch.

## Option 2: Liquidity facility *plus* a simultaneous capital/loss-absorption commitment
Rather than lending first and restructuring later under duress, announce the liquidity bridge together with the structural commitment (capital injection, or a vehicle to absorb/run off the catastrophe losses, or a public guarantee of the affected liabilities). This front-loads the viability signal to markets and rating agencies.

AIG's experience is the cautionary tale that motivates this: the sequencing—lend heavily on onerous terms, then restructure four times—prolonged instability and cost credibility ([vol3_iss1_8][The Rescue of American International Group Module Z: Overview][case_study][2021-04-16]). If your viability assessment already concludes the firm needs capital or loss relief, commit to it up front. Moral-hazard concerns are best handled here, in the structural layer (e.g., equity participation, management change, restrictions), *not* baked into the emergency loan's price.

## Option 3: Facilitated private solution / assisted sale, with public backstop
If the core insurance franchise is attractive, the cleanest resolution may be a private capital raise or acquisition by a stronger insurer, with the government providing only a temporary liquidity backstop or a guarantee over the disaster-loss tail to make the deal executable.

AIG initially attempted exactly this—Geithner tried to arrange a private syndicated loan—and it failed only because of the concurrent Lehman collapse ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]). If your market is not simultaneously frozen, a private-led solution is often preferable: less taxpayer risk, less nationalization controversy. The public role shrinks to backstopping the specific uncertainty (the catastrophe losses) that private parties won't price.

---

# Complementary Considerations

- **Pricing: lend freely, do not "make it sting."** The strongest, most transferable lesson from AIG is a warning against punitive pricing. The RCF's initial rate (~12%, LIBOR + 8.5%) plus an 8.5% undrawn commitment fee was explicitly intended to be "onerous"; internal staff called it "extremely high and a burden to AIG and thus… contrary to the idea of trying to sustain the firm," and one senior official called it a "loan shark" rate. It worsened AIG's ratios, contributed to downgrade risk, and had to be cut roughly in half within weeks ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]). For a targeted rescue, only "lend freely" survives from Bagehot's dictum; price to sustain the firm, not to punish it. If a well-collateralized loan is in place, the collateral—not the rate—protects the public.

- **Collateral over covenants.** Secure the loan on the insurer's sound subsidiaries and assets. Good collateral is what makes solvency and moral-hazard debates largely moot, and it is what distinguished the AIG rescue (viable insurance subsidiaries as collateral) from the Lehman non-rescue (inadequate collateral) ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]).

- **Address the loss source directly.** A catastrophe-loss pocket is analogous to AIG's CDS/CDO exposures: it will keep draining cash regardless of how much liquidity you supply. Consider a dedicated vehicle or reinsurance-style arrangement to cap and run off that exposure, as Maiden Lane III did for AIG ([vol3_iss1_6][The Rescue of American International Group Module E: Maiden Lane III][case_study][2021-04-16]).

- **Equity participation and moral hazard belong in the structural layer.** If you take an equity stake for taxpayer upside and incentive discipline, note that AIG's 79.9% "equity kicker" via an independent trust achieved control while avoiding balance-sheet consolidation, but drew litigation and "nationalization" criticism ([vol3_iss1_8][The Rescue of American International Group Module Z: Overview][case_study][2021-04-16]). Structure it deliberately, with attention to legal authority and genuine independence of any holding trust.

- **Watch the rating-agency lens.** Every term should be evaluated for how the agencies will read it. Reducing leverage (debt-for-equity), improving interest coverage, and demonstrating a credible restructuring path were what ultimately satisfied the agencies in the AIG case ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]).

- **Communication and language.** Public framing matters. Loose talk of "insolvency" can itself accelerate a run on a firm whose core business is viable. Communicate the viability rationale, the collateral, and the structural plan clearly and early.

---

# Suggested Framing

Frame your advice to the principal as a two-part decision, sequenced correctly:

1. **First, make the viability call, not a liquidity call.** The disaster losses have prompted the market to question the firm's future. If, after separating the sound core insurance operations from the catastrophe-loss pocket, you judge the firm viable—or committable to viability with defined support—and systemically important, then intervention is warranted. If it is not viable and cannot be made so, emergency liquidity will only transfer losses to the public and delay an inevitable failure.

2. **If viable, deploy liquidity and structure together, priced to sustain, not to punish.** Provide a well-collateralized bridge facility (Option 1) *paired with* a pre-committed structural fix—capital, a loss-absorption vehicle for the catastrophe pocket, or a facilitated private sale/backstop (Options 2 and 3). Keep the loan's price non-punitive; rely on collateral for protection; and place any equity, governance, and moral-hazard conditions in the structural layer where they belong.

The central caution, drawn directly from the closest analogue: **liquidity buys time; it does not cure a viability-driven run, and a punitively-priced loan can make the situation worse by triggering the very downgrades it was meant to forestall.** Decide the structural fix before, not after, you lend.

Would you like me to sketch indicative term-sheet parameters (facility size logic, collateral scope, pricing bounds) or develop the catastrophe-loss ring-fencing vehicle in more detail?