# Query 2 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 5}

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

I now have a comprehensive evidence base. Let me synthesize the answer.

---

## Framing the Problem

Your scenario has three distinct layers that the crisis-fighting literature treats very differently, and the single most important move is to **not conflate them**:

1. **The private-debt fund's loss** — a realized, private-sector loss that must be allocated to someone.
2. **The two named regional banks with large fund commitments** — a potential *solvency/viability* problem at specific institutions.
3. **The sector-wide runs driven by unknown exposures** — an *acute liquidity* problem born of opacity, spreading "even to well-run financial institutions" (Blanket Guarantees Survey).

The literature's central organizing idea is the distinction between the **acute ("panic") phase** and the **chronic ("debt overhang") phase** of a crisis, and the recognition that *liquidity tools and solvency tools solve different problems* (Broad-Based Emergency Liquidity survey; Blanket Guarantees Survey).

> "In the initial acute phase, the financial system has an obvious liquidity problem—runs on banks…are easy to spot—but the underlying solvency of banks is difficult to judge… Solvency is ultimately an equity problem and *cannot be solved* simply by lending." (Broad-Based Emergency Liquidity Programs)

You are squarely in an acute phase. So the sequencing matters as much as the tool choice.

---

## What the Government Should Do

### Step 1 — Stop the run first; save solvency judgments for later

The over-riding priority in the acute phase is to arrest the runs, because runs turn illiquidity into insolvency and fire sales.

> "In the acute phase… the over-riding priority is to stop runs by depositors and other creditors… authorities need to prioritize the immediate behavior of creditors over the potential long-run moral hazard risks." (Blanket Guarantees Survey)

Crucially, this is exactly the situation where trying to be surgical is counterproductive. Because the *exact pattern of exposures is unknown*, creditors and depositors cannot rationally distinguish the safe banks from the exposed ones:

> "Amid uncertainty about bank solvency… it would not be rational for creditors to do any deep analysis of their banks. The simplest response to solvency concerns is to withdraw one's funds, since withdrawal has only a nuisance cost but potentially a large benefit." (Blanket Guarantees Survey)

The literature also warns explicitly against demanding solvency certification as a precondition for support during the panic, because that judgment cannot be made credibly in real time and attempting it induces stigma and delay:

> "Any strict solvency condition is doomed to failure—there is simply no time to make such judgments." (Broad-Based Emergency Liquidity Programs)

**Practical tools for Step 1:**

- **Broad-based emergency liquidity (lender of last resort).** Lend freely against good collateral to the full population of banks, not just the two named ones. This is the fastest tool, usually deployable under existing authority, and it targets the run behavior of short-term creditors. (Broad-Based Emergency Liquidity Programs)
- **Consider a broad guarantee if liquidity alone doesn't stem the panic.** Because the funding at risk here is not only insured retail deposits but potentially wholesale and other short-term liabilities, an account guarantee may be insufficient; a broader (blanket) guarantee eliminates the incentive to run across a wider range of runnable liabilities. (Blanket Guarantees Survey)

### Step 2 — Guarantees and liquidity buy time; they do not fix the problem

Be clear-eyed that these acute-phase tools are a *bridge*, not a cure. Both the guarantee and the emergency-lending literatures make the same point emphatically:

> "BG programs cannot address underlying problems within financial systems and typically must be part of a comprehensive liquidity support and restructuring package to be successful." (Blanket Guarantees Survey)

> "Crisis-fighters should design ad hoc emergency liquidity provision to buy time to address fundamental viability issues at the borrower. They shouldn't expect these programs to help a bank avoid insolvency by addressing illiquidity." (Ad Hoc Emergency Liquidity Programs in the 21st Century)

Note also the finding that even fully covering all short-term outflows sometimes *does not* stop a run when the market doubts *viability* — which is why the guarantee/liquidity step must be paired with a credible plan to resolve the underlying uncertainty.

### Step 3 — Two design cautions on the guarantee

1. **Credibility versus fiscal capacity.** A guarantee only works if the market believes you can honor it. Cases such as Ireland, Ecuador, and Thailand show that a guarantee too large relative to fiscal resources fails to reassure — and can itself endanger the sovereign. (Blanket Guarantees Survey)
2. **Manage moral hazard with light, non-punitive constraints, not with conditions that deter participation.** During the panic, avoid punitive conditions (e.g., aggressive executive-comp restrictions) that discourage banks from using the facility. Instead use measures like deposit interest-rate caps and bans on aggressive marketing of the guarantee — they curb abuse without seeming punitive. (Blanket Guarantees Survey)

### Step 4 — Resolve the opacity: this is the real cure

The runs are being driven by *not knowing where the exposures are*. The durable fix is to remove that uncertainty. This is where **triage / stress testing** comes in — but the timing is delicate:

> "Triage of banks, through stress tests or other means, is good practice in a chronic phase but may not be desirable (or even feasible) in an acute phase… better data and frequent stress-testing since the GFC make it possible that some countries could now conduct a credible triage even in the acute phase." (Broad-Based Capital Injection Programs)

The GFC template is instructive: broad, simple support first (like the US CPP in the acute phase), then a *credible* scenario-based stress test (like the US CAP) once the immediate panic was contained, to identify which banks actually need capital. A triage attempted too early or with a non-credible methodology backfired in pre-GFC cases (Thailand, Indonesia), slowing intervention without reassuring counterparties. (Broad-Based Capital Injection Programs)

So: use the liquidity/guarantee bridge to buy the time needed to run a credible exposure review, then publish enough to let counterparties tell the sound banks from the impaired ones.

### Step 5 — Fix the genuinely impaired banks (the two named regionals, and any the review flags)

Once you can distinguish liquidity from solvency, treat them differently:

- **Viable banks:** recapitalize if they are short of capital. Solvency is an equity problem and can only be fixed with equity (capital injections or asset purchases), never with lending. (Broad-Based Emergency Liquidity Programs; Broad-Based Capital Injection Programs)
- **Nonviable banks:** resolve, restructure, sell/merge, or (only if there is compelling national interest) nationalize. Recapitalizing a nonviable bank wastes public funds and repeats errors like Cyprus/Laiki. (Survey of Ad Hoc Capital Injections)

Key recapitalization design lessons that apply here:

- **Don't go too small** — "the most common mistake is for programs to be too small." Size the injection to fully solve the problem so you don't have to return. (Broad-Based Capital Injection Programs)
- **Recognize losses and impose them on private stakeholders first.** Before public funds go in, existing equity (and, per bail-in principles, subordinated/other creditors as appropriate) should absorb losses — this addresses moral hazard and political backlash and puts the cost "where it best belongs." (Survey of Ad Hoc Capital Injections)
- **But do bail-ins with clarity and consistency.** Surprise or inconsistent loss allocation (Credit Suisse AT1, Novo Banco senior bonds, Yes Bank) triggered lawsuits and re-ignited contagion in adjacent markets — the opposite of what you want mid-panic. (Survey of Ad Hoc Capital Injections)
- **Combine tools.** A guarantee may stop the run but won't convince anyone a specific bank is *solvent*; pairing capital injections with liability (and sometimes asset) guarantees is a "force multiplier." (Survey of Ad Hoc Capital Injections)

### Step 6 — Communication and political support throughout

- **Communicate clearly and, ideally, with cross-party support.** Sweden's joint announcement with the political opposition bolstered credibility; political turmoil and secrecy (Indonesia's IBRA, Thailand) undermined programs. (Blanket Guarantees Survey)
- **Secure legal authority in advance where possible.** In several cases (e.g., Russia/Otkritie) the lack of a ready bail-in/resolution framework caused months of delay while runs continued. A recurring meta-lesson is to legislate emergency authorities in quiet times. (Survey of Ad Hoc Capital Injections)

---

## Bottom Line

**Yes, the government should act — but in sequence, and it should not begin by trying to figure out which banks are solvent.**

1. **Contain the panic broadly and fast** with lender-of-last-resort liquidity to the whole sector, and, if runs continue, a credibly-sized (fiscally-backed) guarantee covering the runnable liabilities — applied across the sector, precisely because the exposure map is unknown.
2. **Treat these as a bridge**, understanding they buy time but cannot cure underlying losses.
3. **Remove the opacity** with a credible exposure review / stress test once you have breathing room, and disclose enough to let markets re-discriminate between banks.
4. **Then triage:** recapitalize the viable banks (large enough, with losses imposed on private stakeholders first, done transparently), and resolve or restructure the nonviable ones.
5. **Let the private-debt fund's losses fall on the fund's investors** — the government's job is to stop the contagion and repair the banking system, not to make the original private loss disappear. Public capital should go only where there is systemic risk, and only after private stakeholders bear their share.

Throughout, communicate clearly, line up political and legal authority, and shift from "prioritize stopping the run over moral hazard" in the acute phase to "impose discipline, conditions, and exit plans" as you move into the chronic phase.

A caveat on scope: the corpus I searched is the financial-crisis intervention literature (guarantees, emergency liquidity, capital injections, resolution). It speaks directly to the *banking-contagion* dimension of your scenario. It says comparatively little about regulating the private-debt fund itself or the fund investors' write-downs, which the literature generally treats as private losses to be borne privately.