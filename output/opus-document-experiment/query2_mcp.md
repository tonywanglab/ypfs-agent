# Query 2 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 6}

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

I now have enough grounded material to give a structured answer. Let me synthesize.

# What Should the Government Do?

Your situation has a specific and dangerous signature: a **nonbank loss (the private-debt fund) is bleeding into the banking system through opaque, interconnected exposures**, and because *the exact pattern of exposures is unknown*, healthy and unhealthy banks are being run on indiscriminately. The corpus offers clear guidance on how to think about this. Below is a diagnosis, the menu of tools, and a recommended sequence.

## 1. First, diagnose correctly: is this illiquidity or insolvency?

The most important intellectual step, and the one the corpus repeatedly warns against getting wrong. Two named commitments have created *real* solvency questions at two banks, while the runs on the rest of the sector are being driven by **confidence contagion**, not (necessarily) by real losses.

- The Broad-Based Emergency Liquidity survey frames every crisis as having an **acute phase** (obvious liquidity problem, solvency impossible to judge in real time) and a **chronic phase** (liquidity eased, but underlying solvency problems remain). Solvency "cannot be solved simply by lending"—it is an equity problem requiring fiscal tools.
- The Ad Hoc Emergency Liquidity survey warns explicitly: *"Policymakers should take care to not misdiagnose the run on an institution's liquidity as the cause rather than the effect of its problems."* It notes several cases where authorities sized liquidity support to cover *all* possible outflows, yet runs continued until solvency measures (capital, guarantees, restructuring) were added. **Assuring repayment of all maturing obligations is not sufficient to stop runs when viability is in doubt.**

Practical implication: you likely have a mix. The two exposed banks may be solvency cases; the rest of the sector is probably a liquidity/confidence case. **You must treat them differently**, and the whole strategy hinges on *differentiation*.

## 2. The tools, roughly in order of intervention intensity

**(a) Liquidity support / lender of last resort — the immediate first line.**
Provide broad-based emergency liquidity so runnable banks can meet withdrawals without fire-selling assets. In the acute phase, don't impose a strict solvency test as a precondition—the surveys note that on-the-day solvency/viability tests (e.g., the UK Discount Window Facility during the GFC) generate **stigma** so severe that facilities go unused, defeating the purpose. Design against the **moral-hazard-vs-stigma** trade-off: broad eligibility, structured so participation doesn't itself signal distress.

**(b) Guarantees — to stop the run directly.**
Because your run is spreading on *fear of unknown exposures*, a credibly funded guarantee is the tool that most directly kills the incentive to run:
- **Deposit insurance/expansion**: The India–Yes Bank 2020 case is the closest analogue to your problem—India raised deposit insurance 400% *before* imposing a moratorium on the distressed bank, and runs on other banks stayed minimal. But: guarantees only work **if credible**. Cyprus 2013 and Ecuador 1999 show that guarantees perceived as underfunded (or subject to haircuts) actually *accelerate* runs.
- **Blanket guarantee**: If runnable liabilities extend beyond insured deposits (wholesale funding, uninsured deposits), a broader guarantee may be needed. But the Blanket Guarantees survey stresses guarantees **cannot fix underlying problems without complementary liquidity and restructuring**, and their credibility depends on guaranteed liabilities being small relative to fiscal resources. Ireland's GFC experience is the cautionary tale: guaranteeing bank liabilities *transferred* the solvency question from the banks to the sovereign itself.

**(c) Capital injections / recapitalization — for the genuinely undercapitalized (the two exposed banks).**
A liability guarantee addresses liquidity, not solvency; the two banks with real losses may need capital. The Ad Hoc Capital Injection and Broad-Based Capital Injection surveys show these are fiscally and politically expensive but are the only direct fix for an equity hole. They are frequently combined with **asset guarantees** (as in US Citi/BofA) to reduce risk-weighted assets and reassure the market about asset quality.

**(d) Resolution / moratorium — for nonviable institutions.**
For a bank that is genuinely insolvent, resolve or ring-fence it rather than propping it up. A moratorium (India–Yes Bank) buys time to build a resolution plan.

## 3. The special problem: exposures are unknown

This is the crux. When *nobody knows who is exposed*, investors run indiscriminately because—per the Lehman contagion case study—**"when in doubt about a firm's stability, it is easier for investors to abandon that firm rather than figure out its true situation."** Two responses in the corpus target exactly this:

- **A system-wide diagnostic exercise (asset quality review / stress test).** The corpus's central lesson from the GFC (Citi/BofA) is that even after guarantees *and* capital, market concerns about *asset quality* persisted until the US ran the large banks through a **credible stress test** and disclosed the results. The stress test's power is precisely that it **resolves the uncertainty that drives indiscriminate runs**—it lets the market distinguish sound banks from unsound ones. The Stress Tests and Policy article notes stress testing's value in probing "hidden exposures" and "bank and nonbank linkages"—exactly your problem.

- **Ring-fencing to differentiate.** If you cannot immediately produce a credible diagnostic, you may need to ring-fence the affected banks. The Bank Holidays survey shows this is what US–Rhode Island 1991 and Argentina–Funds 2019 did: isolating distressed institutions identifies which banks are affected and mitigates contagion to healthy ones. But a bank holiday is a **"high-risk tool… measure of last resort"**—use it only if more circumscribed measures fail, because the mere act of imposing it can *hasten* contagion (Duvvuri's lesson: the public knows banks are interconnected).

## 4. Don't neglect the source of the shock

The distress *originated in the private-debt fund*, a nonbank. Dudley's lesson learned emphasizes that the nonbank sector is a persistent weak spot outside the usual supervisory perimeter. The US–Reserve Fund 2008 case shows the Fed calmed runs on prime funds by standing up facilities to provide liquidity to the funds themselves. Depending on your jurisdiction's toolkit, you may need to backstop the fund/investor side too, not only the banking side—otherwise losses keep flowing back into the banks.

## 5. Communication is a policy tool, not an afterthought

Every survey converges here. Roosevelt's 1933 "fireside chat," India's reassurance when Yes Bank reopened, and Sweden's *bipartisan* joint announcement all built credibility; Argentina, Ecuador, and Thailand's inconsistent or non-transparent messaging (e.g., Thailand not disclosing suspension criteria, then reversing a guarantee) actively *worsened* runs. Communicate **clearly, consistently, and only what you can credibly deliver**. Overpromising and reneging (Ecuador) is worse than a smaller credible promise.

---

## Recommended sequence

1. **Immediately (acute phase):** Open broad-based liquidity to all banks against good collateral, designed to minimize stigma; do not gate it behind hard solvency tests. Simultaneously announce a **credible guarantee** (expanded deposit insurance, extended to uninsured/wholesale liabilities if those are running) calibrated to your fiscal capacity—this is your fastest run-stopper, per Yes Bank.
2. **In parallel:** Launch a **rapid, credible diagnostic**—a stress test / asset quality review across the sector focused specifically on exposures to the fund and to each other. This is the direct antidote to "exposures are unknown."
3. **As the diagnostic clarifies (chronic phase):** **Differentiate.** Recapitalize the two exposed banks if viable but undercapitalized (potentially with asset guarantees); resolve or ring-fence any that are nonviable. Reopen/confirm the sound majority publicly.
4. **Address the source:** Backstop or wind down the private-debt fund's fallout so losses stop propagating back into banks.
5. **Throughout:** Communicate a coherent, credible narrative, and reserve a **bank holiday only as a genuine last resort** if targeted measures fail to arrest the runs.

## The single most important caveat

Do not let a liquidity response substitute for a solvency answer. The corpus's clearest, most repeated lesson is that liquidity buys *time*; it does not cure viability problems, and runs will continue until the market believes the underlying solvency question—here, *who is actually exposed and by how much*—has been credibly resolved. Your government's decisive act is therefore the **diagnostic that removes the uncertainty**, backed by enough guarantee and capital firepower to make the answer stick.

Whether the government "should" do all of this depends on two things the corpus repeatedly flags: **fiscal capacity** (guarantees and capital that exceed your resources destroy credibility and can drag down the sovereign, à la Ireland) and **whether the exposures, once revealed, are large enough to be systemic**. If the diagnostic shows the contagion is limited and the two banks are the only real casualties, the corpus counsels *against* a broad, disruptive response (Yes Bank's tailored approach over Ecuador's economy-wide holiday) in favor of a targeted one.