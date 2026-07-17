# Query 2 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: agent/system_prompt.md
Tool calls: {"search_corpus": 4}

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

I have enough to build a decision-useful plan. Let me frame this properly.

# Summary of Core Design Dimensions

Before options, a terminology check that shapes everything below. You describe "solvency concerns" and a sector-wide run. The operative question is not point-in-time accounting solvency but **viability** — whether creditors and depositors believe each bank can continue as a going concern (inclusive of expected official support). Your situation has one defining feature that should drive the design:

- **The exposure pattern is unknown.** Markets cannot tell the two genuinely-impaired regional banks from the rest, so they run on *all* regional banks. This is a classic information-driven contagion — the run is a viability judgment made under uncertainty, not a fundamental problem at most banks. The failure to disclose *which* institutions were affected, and on what criteria, is precisely what prolonged panic in the Thai finance-company suspensions ([vol4_iss4_15][Thailand: FIDF Blanket Guarantee, 1997][case_study][2022-12-21]).

The core dimensions you are choosing across:
1. **Triage** — separate the two problem banks from the sector as fast as possible (differentiation is the single most repeated lesson in the corpus).
2. **Confidence backstop** — a guarantee/liquidity measure broad enough to stop the run on the *healthy* majority.
3. **Structural fix for the genuinely impaired banks** — capital, restructuring, or resolution.
4. **Information** — resolve the exposure uncertainty; disclose criteria, not just outcomes.

# Program Archetypes

## Option 1 — Targeted liquidity + rapid differentiation (least disruptive first resort)
Open emergency liquidity to any regional bank that presents (against a broad collateral set), while supervisors rapidly assess each bank's actual fund exposure. The purpose is to buy time and let *access* to liquidity signal viability, so the market stops treating all regional banks alike.

- **Design note on pricing:** resist "penalty rate to make it sting." A punitive rate brands any borrower as desperate and can *trigger* the run you're trying to stop — the "Judas kiss" dynamic. For a broad-based backstop facility, modest pricing is defensible; for targeted lending to the two banks, only "lend freely" survives. Do not let borrowing be a scarlet letter.
- **Precedent for the risk:** inconsistent/limited liquidity commitments made runs *worse* in Hong Kong 1965 — HSBC's initial pledge halted a run, but its "not unlimited" clarification reignited it ([vol4_iss2_40][Hong Kong: Private Emergency Loans, 1965][case_study][2022-07-18]). Whatever you commit to, commit credibly and consistently.
- **Best when:** most regional banks are in fact viable and only two are impaired — which matches your facts. This is the survey-preferred starting point: use the least disruptive tool that fits the scope.

## Option 2 — Confidence backstop: (partial or full) deposit/creditor guarantee
If liquidity alone doesn't stop the run because depositors can't distinguish the exposed banks, a guarantee directly removes the incentive to run regardless of which banks hold fund exposure.

- **Make it credible and precisely scoped.** The blanket-guarantee cases succeeded or failed on credibility. Thailand's guarantee underperformed because the covered liabilities were ambiguous and messaging reversed ([vol4_iss4_15][Thailand: FIDF Blanket Guarantee, 1997][case_study][2022-12-21]). Indonesia's *partial* protection (only IDR 20m/account) actually *triggered* broader runs because large depositors weren't covered and the remaining banks looked suspect ([vol4_iss4_9][Indonesia: Blanket Guarantee, 1998][case_study][2022-12-21]). Lesson: a half-measure guarantee can be worse than none.
- **Back it with real fiscal authority.** Thailand only became credible once an emergency decree let the fund draw directly on the government ([vol4_iss4_15][Thailand: FIDF Blanket Guarantee, 1997][case_study][2022-12-21]).
- **Scope and sunset it.** Australia's wholesale-funding guarantee was closed cleanly once markets normalized and usage looked like pricing arbitrage rather than genuine need ([vol2_iss3_28][The Australian Government Guarantee Scheme for Large Deposits and Wholesale Funding][case_study][2020-10-08]) — a model for exit and for requiring participants to report exposures as a safeguard.
- **Best when:** the run is generalized and information asymmetry (unknown exposures) is the binding constraint — which is your explicit fact pattern.

## Option 3 — Structural fix for the two impaired banks: capital, or good-bank/bad-bank resolution
Liquidity and guarantees only buy time; they do not cure the two banks with real losses. Match the structural remedy to actual viability once triage is done.

- **If viable with a capital hole:** inject capital. Note Japan's ASFF was purpose-built as a *preemptive, broad-based* capital scheme specifically for **regional banks** — directly analogous to your sector ([vol3_iss3_17][Japan's Act on Strengthening Financial Functions (ASFF)][case_study][2021-11-15]). Terms can be tailored to each bank's need.
- **If nonviable:** use a good-bank/bad-bank purchase-and-assumption — transfer viable activities and deposits to an acquirer, park impaired assets in a bad bank, and wipe out equity/subordinated debt while protecting depositors. This is exactly how Greece resolved ATE Bank; the authorities explicitly weighed contagion, cost, and execution risk and chose P&A over outright liquidation ([vol6_iss1_8][Greece: ATE Bank Restructuring, 2012][case_study][2024-03-28]; [vol6_iss3_9][Greece: ATE Bank Capital Injection, 2011][case_study][2024-10-09]). Note the cautionary sequence there: an early capital injection into a nonviable bank was simply wiped out a year later — don't inject capital into a bank that isn't actually viable.

## Option 4 — Bank holiday / moratorium (last resort only)
A short holiday could ring-fence the two banks and pause runs while you diagnose exposures. But this is a high-risk, last-resort tool reserved for genuinely system-wide, comprehensive-solution situations (Argentina 2001, Cyprus 2013, US 1933). With only two banks confirmed impaired and contagion still exposure-uncertainty-driven rather than fundamental, the corpus counsels a **tailored** approach instead — as in the single-bank Yes Bank moratorium, where deposit-insurance expansion *preceded* the moratorium to contain contagion. Reserve this option; don't lead with it.

# Complementary Considerations

- **Differentiation is the master lesson.** Across the corpus, success turns on quickly separating viable from nonviable institutions and reopening/backing only the viable ones. Reopening or vouching for a nonviable bank restarts runs.
- **Disclose criteria, not just names.** Thailand's first suspension round failed partly because it never published the *criteria* for who was cut, breeding suspicion about survivors ([vol4_iss4_15][Thailand: FIDF Blanket Guarantee, 1997][case_study][2022-12-21]). Publishing how you assessed fund exposure is what actually resolves the uncertainty driving your sector-wide run.
- **Sequence matters.** Announce the confidence measure (liquidity access and/or guarantee) *alongside or before* any action against the two banks — as India did by expanding deposit insurance before the Yes Bank moratorium — so the healthy majority is protected before the market learns the bad news.
- **Handle moral hazard in the structural layer, not the emergency loan.** Impose the pricing, dilution, restructuring, and governance conditions on the *capital injection / resolution* of the two impaired banks (equity/sub-debt bail-in per ATE Bank), not on emergency liquidity to healthy banks. Baking "punishment" into the liquidity facility just suppresses uptake and worsens the run.
- **Communication discipline.** Consistent, credible, non-reversible messaging. The Hong Kong 1965 and Thailand reversals show that a wavering commitment is worse than a smaller firm one.

# Suggested Framing

Frame this to your principal as a **contagion driven by unknown exposures, not by widespread insolvency** — most of the sector is likely viable, and the binding problem is that markets can't tell which banks are the two exposed ones. That framing points to a staged response:

1. **Immediately** open broad, freely-priced emergency liquidity to regional banks and launch rapid supervisory triage of fund exposures.
2. **In parallel**, deploy a credibly-funded, precisely-scoped confidence backstop (guarantee) if liquidity alone doesn't halt the run — avoiding the Indonesian half-measure trap.
3. **As triage resolves**, recapitalize the two banks if viable (Japan ASFF-style) or resolve them via good-bank/bad-bank P&A protecting depositors (Greece ATE-style), placing all moral-hazard conditions here.
4. **Publish your assessment criteria** so the market can re-price banks individually, and set a clear exit for any guarantee (Australia-style).

Two caveats I owe you: I don't have your banks' actual balance sheets, so whether the two are viable-with-a-hole (→ capital) or nonviable (→ resolution) is the pivotal unknown that triage must answer first. And a system-wide guarantee is a large fiscal contingent liability — Thailand's fund accumulated ~THB 1.4 trillion in debt — so its scope should be the minimum that credibly stops the run. The decision on how far to extend the public balance sheet is yours; my role is to lay out the tradeoffs.