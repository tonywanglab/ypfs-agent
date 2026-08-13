# Query 2 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: agent/system_prompt.md
Tool calls: {"search_corpus": 5}

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

I have strong, directly analogous material. The 2023 US regional banking turmoil is an almost perfect precedent: correlated exposures, opaque cross-holdings, sector-wide runs on regional banks, and a menu of responses (broad-based facility, systemic-risk-exception guarantees, private consortium liquidity, resolution). Let me synthesize into the plan format.

# Summary of Core Design Dimensions

Before choosing tools, note how your situation maps to a well-documented precedent. The 2023 US regional banking turmoil began with idiosyncratic exposures (SVB's uninsured, concentrated, tech/VC deposit base and unrealized securities losses), but the run then spread by *perceived similarity* rather than confirmed exposure — First Republic was run on despite operating a different business model, simply because the market perceived it as similar and could not distinguish which banks were exposed ([vol7_iss1_24][United States: First Republic Bank Emergency Liquidity Program, 2023][case_study][2025-04-15]). That is precisely your problem: **the runs are driven by an information gap about the pattern of exposures, not (yet) by confirmed insolvency at most banks.**

The core design dimensions you must decide:

1. **Diagnose viability vs. panic.** Reframe your stated "solvency concerns." The relevant question is not a point-in-time accounting comparison but **viability** — whether each institution can continue as a going concern inclusive of expected official support. The two banks with large fund commitments may have a genuine capital hole (a chronic problem liquidity cannot fix); the rest of the sector is likely suffering a *panic* over unknown exposures (an acute problem liquidity/guarantees can address). Do not misdiagnose the sector-wide run as a pure liquidity event — but equally, do not let the word "insolvent" (even loosely applied) propagate to viable banks and manufacture the very failures you fear.

2. **The information problem is the crisis.** Because the exact pattern of exposures is unknown, the market is pricing *every* regional bank as if it might be the next one. Two families of remedy: (a) *resolve the information asymmetry* (rapid supervisory data-gathering / disclosure of who is actually exposed), and (b) *make the information irrelevant* by backstopping liabilities broadly so depositors no longer need to guess.

3. **Broad vs. targeted intervention.** A sector-wide run calls for a broad-based response so that no single institution is singled out and stigmatized. Targeted ad hoc lending to the two exposed banks alone will brand them and may accelerate their deterioration without calming the sector.

4. **Liquidity vs. guarantee vs. capital.** These are sequenced tools for different phases, not substitutes.

# Program Archetypes

## Option 1: Broad-based liquidity facility open to the whole sector (first move, acute phase)

Stand up (or expand a standing facility into) a broad-based emergency liquidity program available to *all* regional banks against good collateral, designed explicitly to be **non-stigmatizing**. This is the archetypal acute-phase first response: fast, implementable under existing authority, and it protects fragile liabilities without requiring you to first sort exposed from unexposed banks.

Design points grounded in precedent:
- **Lend freely; do not make it sting.** A punitive penalty rate and steep collateral demands would deter borrowing and brand any user as desperate — reproducing the discount-window stigma that historically prevented banks from taking liquidity they needed. In 2023 the Fed's Bank Term Funding Program lent against collateral valued at *par* (not marked-to-market) precisely to neutralize the unrealized-loss problem driving fear ([vol6_iss4_1][The 2023 Banking Turmoil: Lessons for EU Resolution Authorities][article][2024-12-17]).
- **Destigmatize by design.** Broad eligibility, many participants, and no contemporaneous disclosure of individual borrowers. Disclosure of individual users historically triggers exactly the depositor pullback you're trying to stop — Northern Rock ran after its borrowing leaked; RFC "revealed banks" during the Depression lost deposits faster and were more likely to close.
- **Operational readiness matters.** SVB and Signature were *not* operationally ready to pledge collateral at the discount window when they needed to ([vol6_iss4_1][The 2023 Banking Turmoil][article][2024-12-17]). Confirm your regional banks can actually access the facility in hours, not days.

*Limitation:* liquidity buys time; it does not cure a capital hole. In no 2023 case did liquidity alone stop a run at a bank the market judged nonviable — First Republic drew heavily on Fed facilities and still ran until it was resolved ([vol7_iss1_24][United States: First Republic Bank Emergency Liquidity Program, 2023][case_study][2025-04-15]).

## Option 2: A liability guarantee to sever the run incentive (if a facility alone doesn't hold)

If broad liquidity does not calm depositors — likely, given that the fear is about *unknown* solvency, and depositors have "only a nuisance cost but potentially a large benefit" from running — escalate to guaranteeing liabilities. This directly addresses the information problem: if deposits are protected, depositors no longer need to know which banks are exposed.

Calibrate scope to the run:
- **Account (deposit) guarantee** — raise or temporarily remove coverage limits. Note the 2023 lesson: statutory insured limits did nothing to stop runs at banks where the runnable money was *uninsured* (89% at Signature, ~94% at SVB) ([vol6_iss4_1][The 2023 Banking Turmoil][article][2024-12-17]). If your regional banks have concentrated uninsured/wholesale funding, a limited guarantee won't bind.
- **Systemic-risk-exception-style full guarantee of the failed/failing institutions' depositors** — in 2023 the US invoked the systemic risk exception to make *all* depositors (insured and uninsured) whole at SVB and Signature, explicitly to stem contagion to the wider system ([vol7_iss1_24][United States: First Republic Bank Emergency Liquidity Program, 2023][case_study][2025-04-15]).
- **Broader blanket guarantee of bank liabilities** — the most powerful and most expensive; requires credibility relative to your fiscal resources and clear political backing. This is a fiscal act, not a central-bank act.

*Design discipline:* handle moral-hazard concerns through the *structure of the guarantee* (interest-rate caps, bans on aggressive marketing, heightened supervision as you move to the chronic phase) — not by making acute-phase support punitive or grudging. In the acute phase, stopping the run dominates; market-discipline-via-run is inefficient and dangerous here.

*Credibility caveat:* a guarantee only works if the market believes you can fund it. Announce only what you can credibly stand behind, ideally with visible political/fiscal unity — fractured political support undermined blanket guarantees in several historical cases.

## Option 3: Ring-fence the two exposed banks — resolve/recapitalize, with a private-sector bridge if available

The two banks with large fund commitments are a different problem from the panicked sector. If, on inspection, they have a genuine capital hole, liquidity and guarantees will not restore them — they need a **structural** fix in the chronic phase: capital injection, or a purchase-and-assumption / merger into a stronger institution.

- **Resolution/P&A.** In 2023, SVB and Signature were moved to bridge banks and sold; First Republic was ultimately sold to JPMorgan via P&A ([vol6_iss4_1][The 2023 Banking Turmoil][article][2024-12-17]). Resolving the clearly-nonviable institutions cleanly can *reduce* contagion by removing the ambiguity — the market can stop guessing about them.
- **Private consortium bridge — with caution.** A consortium of large banks placed $30bn of uninsured deposits into First Republic to buy time. It stabilized funding for only ~five weeks and did not restore confidence because it did not address the underlying capital/viability question; the bank still failed ([vol7_iss1_24][United States: First Republic Bank Emergency Liquidity Program, 2023][case_study][2025-04-15]). Treat private bridges as a time-buying measure, never as a cure, and never as a substitute for resolving viability.

*Sequencing insight:* recognizing up front that liquidity will be *followed* by structural measures actually lets you provide the liquidity more effectively and with fewer strings — you're not pretending the loan will fix solvency ([vol7_iss1_24][United States: First Republic Bank Emergency Liquidity Program, 2023][case_study][2025-04-15]).

# Complementary Considerations

- **Resolve the information asymmetry directly.** Because the panic is fed by *unknown* exposure patterns, a fast supervisory exercise to map which banks are actually committed to the fund — and credible communication of the results — can be as powerful as balance-sheet support. The moment the market can separate exposed from unexposed banks, indiscriminate runs on the latter lose their rationale.

- **Watch the private-debt / nonbank channel.** The shock originates in a private-debt fund (a nonbank). Your LOLR tools reach banks readily but reach NBFIs poorly, owing to information asymmetries and the fact that you don't supervise them. If contagion runs through fund redemptions and further write-downs, consider indirect channels (e.g., access via supervised intermediaries, as the Bank of Canada did through primary dealers in the GFC) rather than lending directly into the fund.

- **Sequence moral-hazard tools into the chronic phase.** Bake incentive corrections (supervisory conditions, capital raises, management/ownership consequences) into the *structural* interventions — capital injections, guarantees, restructurings — not into the emergency liquidity. Emergency liquidity should be clean and fast.

- **Speed and technology.** The 2023 runs were historically fast — SVB lost ~30% of deposits in a single day, digitally coordinated ([vol6_iss4_1][The 2023 Banking Turmoil][article][2024-12-17]). Your response window is hours-to-days. Pre-cleared legal authority and operational readiness are decisive.

# Suggested Framing

Frame the decision to your principal as a **phased, escalation-ready package**, not a single choice:

1. **Immediately (acute):** Open broad, non-stigmatizing liquidity to the *whole* regional sector against good collateral valued generously — lend freely, no penalty pricing, no individual-borrower disclosure. This protects the many viable banks caught in an information-driven panic and buys time.

2. **In parallel:** Deploy supervisory forces to map actual fund exposures across the sector, and prepare (but hold in reserve) a liability-guarantee escalation calibrated to your banks' uninsured/wholesale funding mix. Announce guarantees only at a scope you can credibly and fiscally back, with visible political unity.

3. **On the two exposed banks (chronic):** Diagnose viability honestly. If viable-with-support, pair liquidity with a committed recapitalization or merger path and say so up front. If nonviable, resolve cleanly (P&A/bridge) to *remove* the ambiguity feeding the panic — a private-sector bridge may buy time but will not substitute for resolving the capital question.

The throughline: **your central problem is not liquidity per se — it is that the market cannot tell viable banks from exposed ones.** Every tool above works by either supplying that information or making it irrelevant. Language discipline matters here too: publicly characterizing banks as "insolvent" can itself trigger runs on institutions that are in fact viable — so speak in terms of viability and backstops, not solvency verdicts.

A note on trust levels: the phased acute/chronic logic and terminology framework above are drawn from survey-level synthesis; the specific, citable precedents are the 2023 First Republic case study and the 2023 banking-turmoil article. I can pull the full First Republic case or the blanket-guarantee/account-guarantee design details if you want to go deeper on any one archetype. This is decision-support, not a recommendation — the choice among these is yours.