# Query 1 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: agent/system_prompt.md
Tool calls: {"search_corpus": 6}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

I have enough to build a grounded, decision-useful plan. Here it is.

---

# Summary of Core Design Dimensions

Before selecting an instrument, resolve the diagnosis. A rating downgrade and investor flight are almost always **symptoms of a viability judgment by the market, not a standalone "liquidity problem."** The disaster imposed a real, one-time capital loss; the run is the market's assessment that the going concern may be impaired. This matters because emergency liquidity buys time but **cannot fix a viability problem** — that requires structural tools (capital, guarantees, restructuring).

The AIG precedent is the closest analog on record: a globally significant insurer, downgraded by all three agencies, hit with cascading collateral calls and counterparty flight, nearly forced into bankruptcy. Critically, even an $85B facility sized to cover all short-term outflows did **not** stop the run there — it took subsequent capital and structural measures ([vol3_iss1_2][The Rescue of American International Group Module A: The Revolving Credit Facility][case_study][2021-04-16]; [vol3_iss1_3][The Rescue of American International Group Module B: The Securities Borrowing Facility][case_study][2021-04-16]).

The core decisions you must make:
1. **Is the group viable as a going concern**, assuming feasible official support? (Not "is it accounting-solvent today?" — asset and franchise values are endogenous to your response.)
2. **Where does the strain sit** — at the (typically less-regulated) holding company, or in the regulated insurance subsidiaries? Regulated insurers often hold liquid assets above policyholder-protection minimums; the parent is usually the pressure point.
3. **What can serve as collateral** — specific marketable assets, or the equity/business of viable operating subsidiaries?
4. **Speed, size, pricing, and the exit path**, including how you handle moral hazard and taxpayer compensation.

# Program Archetypes

## Option 1: Collateralized emergency liquidity line (the AIG RCF template)
A secured revolving credit facility large enough to meet obligations as they come due, secured on the group's best available collateral. Where specific marketable assets are insufficient, the lender can take the **equity of the viable operating subsidiaries** as collateral — the Fed essentially took AIG's stakes in operating subsidiaries it viewed as having ongoing viability, effectively taking the business as collateral rather than applying haircuts to specific assets ([vol3_iss1_2][The Rescue of American International Group Module A][case_study][2021-04-16]).

- **When appropriate:** you judge the group viable, and the run is a bridge-financing problem while the disaster loss is absorbed and assets/units are sold in an orderly manner.
- **Pricing — a caution:** AIG's original terms (LIBOR+8.5%, ~12%, plus an 8.5% commitment fee) were deliberately "onerous." They backfired: the high rate raised leverage and eroded interest-coverage ratios, threatening *further* downgrades, and the Fed had to cut the rate roughly in half within weeks ([vol3_iss1_2][The Rescue of American International Group Module A][case_study][2021-04-16]). For a targeted rescue, "make it sting" pricing is counterproductive — it brands the borrower as desperate and can accelerate the very run you're arresting. **Lend freely; do not bake a punitive rate into the emergency loan.** Handle taxpayer compensation and moral hazard through the equity/structural terms instead.

## Option 2: Targeted facility addressing the specific collateral-call channel (the AIG SBF template)
If the cash drain runs through an identifiable channel — e.g., collateral demands on specific contracts, or a securities-lending / reinvestment book that has gone illiquid — a facility that directly unwinds that channel can be more surgical than a general line. AIG's Securities Borrowing Facility provided cash so counterparties could be made whole and return securities, which AIG then posted to the Fed ([vol3_iss1_3][The Rescue of American International Group Module B][case_study][2021-04-16]).

- **When appropriate:** the run is concentrated in one product/counterparty channel created by the disaster and downgrade (e.g., reinsurance collateral, derivative margin, funding-agreement redemptions).
- **Design note:** target the asset class the market has abandoned to free up better collateral, but be confident you are backstopping an oversold market, not propping up a genuinely impaired book.

## Option 3: Liquidity bridge explicitly paired with a structural fix (capital / guarantee / restructuring)
Because liquidity alone did not stop the AIG run, treat any facility as a **bridge to** a structural intervention, decided up front. Structural options, drawn from comparable interventions:
- **Capital injection with conditionality** — preferred shares/subordinated debt tied to a management-improvement or restructuring plan, with conversion rights letting the state act as an activist shareholder if progress lags ([vol3_iss3_15][Prompt Recapitalization Act][case_study][2021-11-15]; [vol3_iss3_16][Financial Functions Stabilization Act][case_study][2021-11-15]).
- **Capital injection with mandated balance-sheet restructuring and shareholder bail-in** — the Swiss Volksbank rescue halved existing shareholders' value as a condition of state capital, an explicit loss-absorption/moral-hazard mechanism ([vol6_iss3_21][Switzerland: Schweizerische Volksbank Capital Injection, 1933][case_study][2024-10-09]).
- **Equity kicker on the loan** — AIG's 79.9% equity stake (held via an independent trust) compensated taxpayers for risk, gave control, and preserved upside, while staying under the 80% consolidation threshold ([vol3_iss1_2][The Rescue of American International Group Module A][case_study][2021-04-16]; [vol3_iss1_8][The Rescue of American International Group Module Z: Overview][case_study][2021-04-16]).

- **When appropriate:** the disaster loss is large enough that the market questions the going concern — i.e., most cases matching your description. This is likely the realistic path.

# Complementary Considerations

- **Reframe the vocabulary deliberately.** Avoid "insolvent" in any public communication — the label itself can trigger runs even where the business is viable. Anchor internal and external framing on **viability as a going concern, inclusive of expected official support**.
- **Ring-fence the regulated insurance subsidiaries.** Policyholder assets are typically protected and above minimums; a New York proposal briefly let AIG borrow surplus liquid assets from insurance subsidiaries, but it was abandoned once it became clear the problem was not a brief cash-flow gap ([vol3_iss1_3][The Rescue of American International Group Module B][case_study][2021-04-16]). Confirm you are solving the parent's problem, not draining policyholder protection.
- **Speed and legal authority.** AIG's first draw went out the day the facility was announced via a demand promissory note ahead of full documentation ([vol3_iss1_8][Module Z: Overview][case_study][2021-04-16]). Pre-clear your legal authority for lending to a nonbank and for taking equity; the AIG equity kicker drew years of litigation over authority to hold shares.
- **Seniority and collateral perfection.** Secure seniority in the liability stack so you are protected through any sale or restructuring; where collateral cannot be posted in time, consider taking preferential rights in bankruptcy instead.
- **Sizing is necessary but not sufficient.** Multiple surveyed interventions sized liquidity to cover all short-term outflows, yet outflows continued until structural measures landed. Plan the second step before the first fails.
- **Parity.** If your terms look harsher (or softer) than support given other firms, expect to justify the difference — a point flagged pointedly in the AIG oversight review.
- **Private-sector solution first.** AIG's rescuers attempted a private syndicated loan before the public facility; a private (re)insurance-industry or bank consortium bridge is worth a fast attempt, but do not let it delay a public backstop if markets are moving.

# Suggested Framing

Frame the recommendation to your principal as a **two-stage, viability-anchored response**, not a bailout-versus-let-fail binary:

1. **Immediate:** an emergency liquidity bridge (Option 1, possibly narrowed to the specific drain channel per Option 2), sized to obligations coming due, secured on the viable operating units, priced to *sustain* the firm rather than punish it, and senior in the stack.
2. **Contingent and pre-planned:** a structural fix (Option 3) — capital injection and/or guarantee with conditionality, shareholder loss-absorption, and a taxpayer upside instrument — that actually resolves the going-concern question the market is pricing.

The decision hinges on one judgment that is yours, not mine to make: **is this globally significant insurer viable as a going concern once the disaster loss is absorbed and with feasible official support?** If yes, the AIG template (modernized on pricing) is well-precedented. If the answer is genuinely no, the tools shift toward orderly resolution rather than rescue — a different analysis I can prepare if useful.

I can also draft an indicative term sheet, or pull the full AIG or Volksbank case studies to detail the equity/conditionality mechanics, on request.