# Query 1 — rag

Model: anthropic/claude-fable-5 | Retrieval: rag | System prompt: none
Tool calls: {"search_corpus": 6}

**Prompt:** A natural disaster caused large losses at a globally significant insurance company in your jurisdiction. The credit rating of this company has been downgraded, investors are fleeing, and it is facing a short-term liquidity crisis. The company has asked the government for help. What do you recommend?

---

## Recommendation

Your scenario closely parallels the most instructive case in the corpus: the 2008 rescue of American International Group (AIG)—a globally significant insurer whose credit downgrades triggered cascading liquidity demands and a near-bankruptcy that the US government judged too dangerous for the financial system to absorb. Drawing on that case and on the cross-country surveys of emergency lending, here is what I recommend.

### 1. First, diagnose the problem precisely — and quickly

- **Distinguish liquidity from solvency, but don't expect a clean answer.** A natural-disaster loss is a genuine *capital* event, not just a funding squeeze. The AIG experience warns that the initial diagnosis is often wrong: the Fed's $85 billion Revolving Credit Facility (RCF) "proved insufficient to meet AIG's needs" because "the firm's problems were not only liquidity constraints but also issues such as devaluation of assets that weakened it and risked downgrades." Central bankers surveyed also concede that "distinguishing illiquid from insolvent institutions is not easy and may be impossible in times of crisis" — and that illiquidity tends to become insolvency the longer a crisis lasts.
- **Map every channel of cash drain.** At AIG, the downgrade itself was the accelerant: it triggered ~$20–32 billion in collateral calls on derivatives *and* a run by securities-lending counterparties demanding their cash collateral back. Ask: what claims, collateral triggers, policyholder surrenders, commercial paper rollovers, or counterparty terminations does *this* downgrade set off? Size the hole before committing — AIG's projected shortfall grew "from $20 billion to $40 billion and eventually close to $80 billion" in a single week.
- **Embed a monitoring team.** The FRBNY "had little information about AIG's true financial situation" at the outset and later stationed roughly 15 officials at the firm full-time. Do this from day one.

### 2. Test whether intervention is warranted at all

- **Confirm systemic significance, not just size.** The Fed justified acting because "a disorderly failure of AIG could add to already significant levels of financial market fragility and lead to substantially higher borrowing costs, reduced household wealth, and materially weaker economic performance." If a disorderly failure of this insurer would *not* propagate through counterparties, funding markets, or policyholder confidence, the right answer is the normal insurance resolution/guaranty framework, not a rescue.
- **Exhaust private options first — but with a public backstop ready.** The Fed initially tried to arrange a $75 billion private syndicated loan for AIG; Lehman's bankruptcy that same morning made it impossible. Pursue private capital raises, reinsurance and catastrophe-bond recoveries, asset sales, or a merger — but have the public option prepared in parallel, because private solutions collapse fast in stressed markets.
- **Be transparent about *why* you act.** Studies of the AIG decision scored the Fed's transparency poorly, finding that unclear rationales "contributed to market destabilization" and public distrust. Publish your systemic-risk rationale.

### 3. If you lend: lend freely, take security creatively, but do not over-punish

- **Take the whole business as collateral if needed.** When conventional collateral is insufficient, ad hoc lenders have taken equity in operating subsidiaries (the Fed with AIG, the Riksbank with Carnegie) or all assets "right down to the paper clips" (Bank of England–Northern Rock), or seniority in bankruptcy (SNB–Credit Suisse). An insurer with sound underlying subsidiaries is well suited to this approach.
- **Avoid a punitive rate — this is the clearest lesson in the corpus.** The AIG RCF's initial LIBOR + 850bps pricing was described as "harsh," "onerous," and "punitive"; it threatened further downgrades and had to be cut by 550bps within two months. The ad hoc lending survey concludes that a penalty rate on a targeted institution "is liable to instead accelerate the drain on the affected institution's financial resources (and be disfavored by the market and the rating agencies)." Price above market norms but below the level that makes recovery impossible — moral hazard is better managed through later restructuring terms. This is doubly true here: a natural disaster is an exogenous shock, not reckless risk-taking, so the moral-hazard case for punitive terms is weaker than it was for AIG.
- **Design with the rating agencies explicitly in mind.** Ratings are the trigger mechanism in your scenario. Both TARP investments in AIG succeeded partly because Moody's and S&P responded by maintaining ratings, saying the support "improves capital adequacy and reduces pressure on debt holders." Size and structure the package so agencies can affirm the rating; an underpowered facility invites further downgrades and a second, larger rescue.

### 4. Treat liquidity support as a bridge, not the destination

- **Plan the structural solution now.** The survey evidence is emphatic: ad hoc liquidity "almost always" works only as a bridge to more structural responses — capital injections, asset sales, restructuring, or merger. AIG ultimately required the RCF, a securities borrowing facility, two asset-purchase vehicles (Maiden Lanes II and III), ~$70 billion of Treasury capital, two restructurings, and a recapitalization. If disaster losses have impaired capital, a fiscal capital injection (with the legislature involved) will likely be needed alongside central bank liquidity — and forthcoming capital can itself serve as part of the lender's security.
- **Require an orderly divestiture/de-risking plan,** as with AIG, which shrank from $1.02 trillion to $551 billion in assets — but calibrate the timeline. Overly tight deadlines force fire sales into weak markets.

### 5. Protect taxpayers — carefully

- **Take upside compensation (equity/warrants) for the risk assumed,** as the government's ~79.9% AIG stake did — the overall AIG rescue ultimately returned a net gain of about $22.7 billion. But heed the legal lessons: verify your statutory authority to take equity and structure any shareholding vehicle for genuine independence, since the AIG trust arrangement spawned years of litigation (the *Starr* case) and congressional criticism.
- **Impose governance conditions:** board/management accountability (the AIG trust replaced the board), dividend restrictions, and—critically—**compensation controls up front.** The $165 million in retention bonuses paid to the very division that caused AIG's losses generated enormous public outrage and nearly derailed political support. Do not let a similar oversight poison your program.
- **Consider counterparty/creditor burden-sharing.** A persistent criticism of AIG is that counterparties were paid at full face value with no concessions, leaving the entire cost on shareholders and taxpayers. Where feasible, negotiate haircuts or contributions from those who benefit from the rescue.

### Bottom line

Intervene only if failure is genuinely systemic; move fast with a fully secured, adequately sized liquidity facility priced firmly but not punitively; design it to stabilize the credit rating; and treat it explicitly as a bridge to a capital-and-restructuring solution with equity upside, governance conditions, and clear public communication. The AIG record shows this can end with the firm stabilized, the system protected, and taxpayers repaid with a profit — but only if the government commits sufficient resources early, expects surprises, and avoids terms so harsh they defeat the rescue's own purpose.