# Query 3 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 8}

**Prompt:** A Chinese company has just announced that it has achieved recursive self-improvement of a frontier LLM, without using Nvidia chips. This causes the equity prices of U.S. AI companies to crash, and the collateral used to back AI-company loans to fall significantly. This causes solvency concerns at several financial intermediaries, with a liquidity crisis feared to come. What should the government do?

---

I have gathered comprehensive, well-corroborated evidence. Here is my analysis.

# What Should the Government Do? A Playbook Grounded in Crisis History

## First, diagnose correctly: is this liquidity or solvency?

The single most important lesson from the corpus is that governments must not misdiagnose the problem. The scenario you describe has a specific structure worth naming precisely:

- A **real, fundamental shock** to asset values (the value of U.S. AI equity and the collateral backing AI-company loans has fallen because a genuine technological development impaired the earnings prospects of those companies).
- A **feared liquidity crisis** at intermediaries that hold those impaired assets or lent against them.

This ordering matters enormously. As Paul Volcker put it, "I long ago came to the conclusion there are very few liquidity crises that aren't related to a solvency question," and Mervyn King echoed that "almost every financial crisis starts with the belief that the provision of more liquidity is the answer, only for time to reveal that beneath the surface are genuine problems of solvency" (Ad Hoc Emergency Liquidity Programs survey). The AHEL survey is emphatic: policymakers should "take care to not misdiagnose the run on an institution's liquidity as the cause rather than the effect of its problems."

In your scenario, the collateral fell because of a fundamental repricing, not a temporary panic. That means **liquidity support alone will not be a cure** — it can only buy time.

## The two-phase framework

The surveys consistently frame crises and responses in two phases:

- **Acute phase:** Obvious liquidity problem (runs, funding markets seizing), but underlying solvency is hard to judge in the heat of the moment. Response must be *fast* and emphasize *liquidity/liability protection*. The goal is to arrest runs and prevent fire sales. (Blanket Guarantees, Account Guarantee, and Broad-Based Emergency Liquidity surveys all use this framing.)
- **Chronic phase:** Liquidity pressures ease, but solvency problems remain. As the BBEL survey states bluntly, "Solvency is ultimately an equity problem and *cannot be solved* simply by lending. To fix solvency problems, policymakers typically need to deploy fiscal tools, either directly through capital injections or indirectly through the purchase and sale of bank assets."

## Sequenced recommendations

### 1. In the acute phase — stop the run, don't fight moral hazard yet

If short-term funding is fleeing intermediaries and a run is developing, the central bank should act as **lender of last resort** along modernized Bagehot lines: as the BBEL survey restates it, "In the acute (panic) phase of a crisis, a lender of last resort should lend freely and broadly against good collateral, at rates set by auction, taking care to avoid disclosing details about individual borrowers."

Two important nuances from the corpus:

- **Do not impose a strict, literal solvency test in the panic.** The BBEL survey argues that "defining what solvency means in the midst of the panic would be difficult and even counterproductive." Assets are being sold at "temporarily depressed prices," and there is "simply no time to make such judgments" for the broad population of firms.
- **Set moral-hazard concerns aside temporarily for creditors.** Both the Account Guarantee and Blanket Guarantee surveys argue that in the acute phase, "the over-riding priority is to stop runs," and authorities should not pursue moral-hazard measures (like harsh terms or executive-comp restrictions) that discourage participation. But they *should* use non-punitive measures — interest-rate caps, bans on aggressive marketing — to prevent banks from exploiting any guarantee.

**Watch the fire-sale spiral.** The Fed's primary-dealer case study describes exactly the dynamic to be feared here: "Asset price declines… lead to margin calls… Dealers respond by liquidating collateral. This puts downward pressure on asset prices… A vicious circle ensues of higher haircuts, fire sales, lower prices, higher volatility… and financial intermediaries start to break as a liquidity crisis potentially leads to insolvency when assets are sold at fire sale prices." Breaking this loop — e.g., by lending against the impaired collateral, or a "market maker of last resort" intervention in a specifically dysfunctional market (Nakaso lessons; ECB SMP; TALF) — can be justified as arresting contagion.

### 2. Crucially — distinguish liquidity from a fundamental repricing before you deploy the public balance sheet

Here your scenario needs a sharp caveat that the corpus supplies. There is a real analytical question, examined in "Revisiting Subprime Pricing Irrationality," about whether asset-price declines reflect *liquidity/panic* (in which case public purchases of temporarily impaired assets "would mitigate such crises at no risk," even profiting taxpayers) or reflect *fundamentals*. That paper warns: "If… price declines are fundamental in nature, then… programmes where the U.S. Treasury takes a leveraged first-loss position on credit risky instruments expose the taxpayer to undue risks when solvency rather than liquidity is the dominant problem."

In your scenario, the AI shock is a genuine, fundamental impairment of the earnings prospects of these companies. That strongly suggests the collateral decline is **not merely a liquidity phenomenon**. The government should therefore be cautious about propping up AI-company equity prices or buying AI-linked assets at pre-crash values — that would be transferring fundamental losses to taxpayers and bailing out equity holders who made a bet that a technological shift rendered unprofitable.

The proper government objective is to protect the **financial system and the flow of credit to the real economy**, not to protect the equity value of AI companies or the shareholders/subordinated creditors of failing intermediaries.

### 3. In the chronic phase — force recognition, then recapitalize with private capital where possible

Once the acute run is contained, the durable fix for the intermediaries is solvency repair. The corpus points to a specific, well-tested sequence — the U.S. SCAP/stress-test approach:

- **Run credible, disclosed stress tests** to size the hole. Matthew Kabaker's lessons describe how, by late 2008, "it was increasingly clear… that we had a solvency, not a liquidity crisis," and initial capital injections weren't shifting perceptions. The breakthrough was a stress test that (a) disclosed banks' actual exposures, and (b) came with an assurance that banks meeting the bar would survive as private firms, backed by "an unlimited backstop to the purchase of common equity" if private capital fell short. This made the sector "investable" and mobilized private capital rather than public. Malaysia's Danamodal, Spain's FROB, and Ireland's NAMA/PCAR are further examples of stress-test-driven recapitalization.
- **Recapitalize — mobilizing private capital first**, with government as backstop. The point is to fill capital holes, not to substitute the public balance sheet for private markets.

### 4. Impose burden-sharing in the chronic phase to address moral hazard

Once the acute danger has passed, moral-hazard and political-legitimacy concerns should reassert themselves. The Survey of Ad Hoc Capital Injections argues that authorities should "address the political backlash and moral hazard concerns with tough measures such as bail-in — imposing losses on shareholders and creditors — and discipline for management." Parex Bank (Latvia) is a clean example: shareholders and subordinated debtholders were wiped out while insured depositors and senior creditors were protected — a "valuable signal against moral hazard."

**A caution on bail-in mechanics:** the same survey warns that surprise losses can spook markets (the Credit Suisse AT1 episode froze the broader AT1 market). So burden-sharing should be clear, legally grounded, and consistent with the documented capital hierarchy.

## Cross-cutting requirements

**Communicate with a clear, single voice.** Kabaker stressed getting "one capital 'bogey'" and regulators speaking with one voice. Miguel Carcaño: "you need to be able to give to the market a clear diagnosis… and communicate what solutions… you put in place." Veerathai Santiprabhob adds that you should disclose sensitive information "together with supportive measures."

**Credibility must match fiscal resources.** The Blanket Guarantee survey warns that guarantees fail if the amount guaranteed exceeds credible fiscal backing, and that clear political support is decisive (Sweden's cross-party announcement worked; political turmoil undermined Ecuador, Indonesia, Thailand). Subba Rao Duvvuri's caution is directly relevant: a blanket guarantee can *backfire* — India declined one during the GFC precisely because a wholesale guarantee would have run counter to reassurances and made markets "suspect that we were hiding something."

**Identify what is actually systemic.** Your scenario involves financial intermediaries — but note that AI-linked credit and equity exposures may sit substantially in *nonbanks* (hedge funds, private credit, CLOs, mutual funds). The AHEL survey notes systemic importance turns on interconnectedness, not just size ("too interconnected to fail"), and Mark Van Der Weide flags shadow banking as the area where crisis tools are least developed. The government must map where the AI exposure actually resides before choosing tools, since the LOLR framework is best-developed for banks.

**Don't withdraw support prematurely.** David Wilcox warns that pulling back relief and fiscal support too quickly slowed the recovery and worsened inequality after the GFC.

## Summary

1. **Diagnose:** Treat the collapse as fundamentally a *solvency/repricing* event, not a pure liquidity panic — because the AI shock genuinely impaired asset values.
2. **Acute phase:** Have the central bank lend freely against good collateral, broadly, at auction rates, to halt runs and break the fire-sale spiral — without a strict real-time solvency test and without punitive terms that deter participation.
3. **Do not** use the public balance sheet to reflate AI equity prices or protect the shareholders of failing firms; protect the *system and credit flow*, not the losing bets.
4. **Chronic phase:** Run credible, disclosed stress tests to size losses; recapitalize intermediaries, mobilizing private capital with a government backstop; and impose clear, legally grounded burden-sharing (bail-in of shareholders/junior creditors) to address moral hazard.
5. **Throughout:** Communicate with a single credible voice, keep commitments within fiscal capacity, map where the exposures actually sit (including nonbanks), and avoid exiting support too soon.

A caveat on the evidence: the corpus is drawn from historical banking crises. The core diagnostic and sequencing lessons transfer well, but an AI-driven shock concentrated in equity markets and nonbank credit may test the bank-centric LOLR toolkit — which is precisely the gap the corpus itself flags as under-developed.