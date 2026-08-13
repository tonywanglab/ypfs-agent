# Query 2 — rag

Model: anthropic/claude-opus-4.8 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 10}

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

I have enough to give a well-grounded answer. Let me synthesize.

## Assessment and Recommendation

Your scenario has a specific structure that shapes the right response: the *underlying* loss (the private-debt fund) is relatively contained, but the *panic* is being driven by **uncertainty about which banks are exposed and how much**. That distinction — between a real solvency problem at a few institutions and an information-driven run across the whole sector — is exactly the situation the historical record addresses, and it points to a sequenced, multi-tool response rather than a single silver bullet.

### The core diagnostic problem

The runs are spreading because depositors and creditors can't tell healthy banks from exposed ones. As the *Blanket Guarantees Survey* notes, amid uncertainty about solvency, "it would not be rational for creditors to do any deep analysis of their banks. The simplest response to solvency concerns is to withdraw one's funds, since withdrawal has only a nuisance cost but potentially a large benefit." The central-bank literature adds a warning: **illiquidity tends to become insolvency the longer a crisis lasts** — so runs on genuinely-solvent banks can *create* the insolvency you're trying to avoid through fire sales and lost franchise value (*Broad-Based Emergency Liquidity Programs*). This means speed matters, and doing nothing is itself a costly choice.

### What the government should do — a sequenced package

**1. Provide emergency liquidity immediately (lender of last resort).**
This is the first-line tool and buys time. In the closest historical analogue to your scenario — the 2008 Reserve Primary Fund breaking the buck and triggering a **$439 billion run** on money market funds — the Fed's new liquidity facilities were central to subsiding redemptions. Central banks generally support LOLR lending to *solvent* banks; the practical difficulty is that solvency is nearly impossible to assess in real time. The pragmatic answer used repeatedly is to lend generously against collateral to buy time, while a separate process sorts out solvency.

**2. Address the run directly with a guarantee — sized to the actual problem.**
The single most relevant precedent is the **U.S. Temporary Guarantee Program for Money Market Funds (2008)**, which maps almost perfectly onto your situation (an investment fund's loss triggering a sector-wide run on institutions whose exact exposures were unknown). Key design features worth emulating:
- It guaranteed holdings **as of the announcement date** (so it stopped the run without subsidizing new risk-taking or letting money flood in to game the guarantee).
- Participating funds paid a **quarterly fee (1–1.5 bps)**, making it a priced, opt-in program.
- Result: it covered 93% of the market (~$3.2 trillion), **cost the taxpayer nothing** — no payouts — and generated a $1.2 billion surplus in fees.

The lesson is that a well-designed guarantee can break a panic at low or negative fiscal cost precisely *because* the underlying problem is limited and the panic is informational. A guarantee (whether of deposits or broader liabilities) removes the incentive to run, which is what you need when nobody can see the pattern of exposures.

**Critical caveat on guarantees — credibility relative to fiscal capacity.** The *Blanket Guarantees Survey* is emphatic that a guarantee only works if it is credible relative to the state's resources. Where guarantees were **too large relative to fiscal capacity** — Ecuador, Ireland, Thailand — they *failed to reassure* and, in Ireland's case, the state ended up bearing costs totaling **~40% of GDP** (second-costliest advanced-economy crisis since the Depression). So: guarantee no more than you can credibly stand behind, and don't blanket-guarantee everything reflexively if a narrower guarantee (matched to the actual run) will do.

**3. Restore information — a coordinated stress test / asset-quality review.**
Because the crisis is fundamentally about *not knowing who is exposed*, the durable fix is to make the exposures known and credibly bound the losses. The **2009 U.S. SCAP stress test** is the model here. Earlier point-in-time capital injections had left "investors remained skittish"; the stress test worked because it "credibly sized the potential capital needs of the largest banks" in a forward-looking way and is "broadly seen as having done much more to reassure markets than those earlier efforts" (*Stress Tests and Policy*). A transparent, common-methodology review of exposures to this fund — paired with a credible public capital backstop for any bank found short — converts a panic driven by fear of the unknown into a manageable, bounded problem.

**4. Triage and recapitalize the genuinely troubled banks.**
For your two regional banks with real solvency concerns, distinguish clearly:
- **Solvent but undercapitalized** → recovery/recapitalization. As *Containing Runs on Solvent Banks* argues, in this phase "time is not on the side of regulators"; forbearance is "a gamble that leads to even larger expected fiscal losses." Move to recapitalize (private capital first where possible, public backstop behind it).
- **Insolvent** → resolution. If a bank is genuinely insolvent, resolution is "the sole legitimate policy."

The *Broad-Based Capital Injection Programs* survey stresses that recapitalization is "often ineffective without an NPL strategy, and vice versa" — so pair capital injections with a plan for the impaired fund exposures. Structure public capital to **incentivize rapid private replacement** (warrants, step-up dividends, as in the UK/Ireland/US programs).

### On moral hazard and timing

Don't let moral-hazard concerns paralyze the acute-phase response. The survey's clear guidance: in the acute phase "the over-riding priority is to stop runs," and authorities should *not* attach punitive conditions (e.g., harsh executive-pay limits) that discourage banks from using liquidity/guarantee facilities. Instead, manage moral hazard with proportionate measures that don't deter participation — **caps on deposit interest rates and bans on aggressive advertising of the guarantee** — to stop guaranteed banks from competing destructively for funds. Save the structural discipline (heightened supervision, capital norms) for the chronic phase.

### Exit

Any guarantee should be temporary with a **pre-planned, phased wind-down** back to normal (limited) deposit insurance. Kane and Klingebiel note that the hardest part is *cutting back* the guarantee; a sudden withdrawal can itself be destabilizing, so several programs used pre-defined step-downs. The MMF program's fixed one-year sunset is a clean example.

---

### Bottom line

**Yes, the government should act — and quickly, because delay converts a liquidity panic into real insolvencies.** The recommended package:
1. **Open liquidity taps** to solvent banks now, to stop the bleeding.
2. **Deploy a priced, temporary guarantee** covering existing liabilities, sized credibly to fiscal capacity, to remove the incentive to run — the MMF program is your template.
3. **Run a fast, transparent stress test / exposure review** with a public capital backstop, to replace fear-of-the-unknown with bounded, known losses — the SCAP template.
4. **Triage the two troubled banks**: recapitalize if solvent-but-undercapitalized, resolve if insolvent, and pair capital with a strategy for the fund exposures.
5. **Manage moral hazard lightly during the acute phase** (rate caps, ad bans), and **plan the exit** from the guarantee up front.

The through-line from the historical record is that no single tool suffices: guarantees stop runs but "cannot address underlying problems without complementary liquidity support and restructuring measures." The art is matching the *breadth* of the intervention to the *actual* problem — which here is a limited real loss amplified by information gaps — rather than over-guaranteeing in a way that strains credibility and the budget.

A caveat on scope: my recommendation draws on the crisis-management corpus above (the MMF, SCAP, blanket-guarantee, capital-injection, and LOLR literatures). The specifics — your jurisdiction's fiscal room, legal authorities for a guarantee, the actual size of the fund losses relative to bank capital, and whether the two banks are truly solvent — would need to be verified before committing to any particular tool, and would materially affect how large and broad the guarantee should be.