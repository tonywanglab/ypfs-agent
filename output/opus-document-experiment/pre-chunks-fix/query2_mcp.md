# Query 2 — mcp

Model: anthropic/claude-opus-4.8 | Retrieval: mcp | System prompt: none
Tool calls: {"search_corpus": 4}

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

I now have enough material from the corpus to give a well-grounded answer. Let me synthesize.

---

# What Should the Government Do?

Your scenario has a specific structure that the crisis-fighting literature speaks to directly. Let me first name the structure, then walk through the sequenced response the corpus supports, and finally flag the traps.

## The diagnostic frame

Three features define your situation:

1. **The originating shock is in a nonbank (the private-debt fund)**, but it is transmitting into the *regulated banking system* via the two regional banks' commitments.
2. **The pattern of exposures is unknown**, so the market cannot tell healthy banks from sick ones. This is the "acute phase" of a crisis, in the language of the corpus's Account Guarantee and Blanket Guarantee surveys — an *obvious liquidity problem* (visible runs) sitting atop *hard-to-judge solvency*.
3. **Runs are already generalizing across the sector** because of that opacity — depositors and investors are running not on the basis of analysis but because withdrawal is nearly costless and potentially very beneficial when you can't distinguish good from bad.

The single most important insight from the corpus is that **your response must be split into two problems and sequenced accordingly**: (a) *stop the run now* (liquidity/confidence), and (b) *diagnose and repair actual solvency* (viability). Conflating them is the classic error.

## Step 1 — Stop the run: broad, credible confidence measures (acute phase)

The Account Guarantee and Blanket Guarantee surveys are explicit that in the acute phase, when solvency is genuinely unknowable in real time, **policy should prioritize the behavior of depositors and short-term creditors over long-run moral-hazard concerns.** As the AG survey puts it, with uncertainty about bank solvency "it would not be rational for depositors to do any deep analysis of their banks. The simplest response to solvency concerns is to withdraw one's deposits." Relying on runs as market discipline "could be disastrous during the acute phase of a crisis."

Concrete tools, in rough order of preference:

- **Deposit insurance / account guarantees, credibly communicated.** The Bank Holidays survey repeatedly stresses that *credible* deposit insurance is the front-line run-stopper. The India–Yes Bank 2020 case is the model your scenario most resembles: authorities *expanded deposit insurance (by 400%) before* imposing a moratorium on the one troubled bank, and as a result "runs on other banks were minimal." That is precisely the sector-wide-fear-from-a-single-institution dynamic you describe.

- **Emergency liquidity to solvent-but-illiquid banks (lender of last resort).** Bagehot's principle as updated in the corpus: lend freely, against good collateral, at a penalty rate, to *solvent/viable* firms. This lets healthy regional banks meet withdrawals without fire sales.

- **If runs are broad and liquidity/insurance aren't stemming them, escalate to a broader guarantee** — potentially a blanket guarantee of a wider set of liabilities. The Blanket Guarantee survey warns these must be *credible relative to fiscal resources* and backed by clear political support (Sweden's joint announcement with the opposition is the positive example; political turmoil undermined Ecuador, Indonesia, Thailand).

**A note on the nonbank origin.** Because the shock started in a fund, the run may not be confined to insured deposits. The corpus's US–Reserve Primary Fund 2008 case is the direct analog: a fund "broke the buck," runs spread across *all* prime money funds regardless of their actual Lehman exposure, and the government stopped it with (a) Treasury's temporary guarantee of money-fund shares and (b) Fed liquidity facilities (AMLF, MMIFF) that financed purchases of the funds' assets. The lesson: **your guarantee/liquidity perimeter may need to extend beyond insured bank deposits to whatever runnable liabilities are actually running** — uninsured deposits, wholesale funding, and possibly investor claims on the fund vehicle itself. (The corpus notes the US did exactly this again in March 2023 for uninsured regional-bank depositors.)

## Step 2 — Ring-fence and diagnose (buy time, then differentiate)

Once the run is arrested, you must resolve the *actual* opacity, because guarantees don't cure underlying insolvency.

- **Ring-fencing / a targeted moratorium on genuinely troubled institutions.** The Bank Holidays survey emphasizes that a holiday or moratorium is useful precisely to "ring-fence distressed banks and differentiate them from healthy ones" (US–Rhode Island 1991; Argentina-Funds 2019). Critically, the survey's recommendation is to prefer the **narrowest tool that works**: if only a limited number of banks are distressed and contagion is containable, a *tailored* approach (moratorium/recapitalize/resolve the affected banks) is better than a system-wide bank holiday. A full bank holiday is a "high-risk tool" and "measure of last resort." Given that only two banks are known to be seriously exposed, aim for the targeted end of the spectrum, using the sector-wide guarantee (Step 1) to hold the line around the rest.

- **Run an asset-quality review / stress test to map the unknown exposures.** The whole problem is that "the exact pattern of exposures is unknown." The European cases (SSM Comprehensive Assessment, Ireland's PCAR/NAMA, Spain's Oliver Wyman AQR + stress test, Slovenia's BAMC) show the standard mechanism: a credible, disclosed AQR + stress test that measures each bank's fund exposure and resulting capital hole. This is what converts opacity into a sortable list of viable vs. nonviable banks.

**Heed the Ireland warning:** in the NAMA case, the asset haircuts came in *larger* than the earlier stress tests had projected, and disclosing that *increased* uncertainty rather than resolving it — forcing the government into a troika program. Lesson: **be conservative and credible in your loss estimates, and make sure you have the fiscal capacity to fill the holes you reveal before you reveal them.** A stress test you can't afford to backstop makes things worse.

## Step 3 — Repair solvency: recapitalize the viable, resolve the nonviable

The Bank Holidays survey's central conclusion is that success depends on **reopening/supporting only viable banks — injecting capital where needed — so runs don't restart.** Differentiation is critical (US 1933, US–Rhode Island 1991): reopening or backstopping nonviable banks "risks a restart of runs."

For your two exposed regional banks specifically, the LOLR literature (Tucker; the AHEL survey; the EU ELA note) is emphatic and gives you a hard constraint:

- **Do not use central-bank liquidity to prop up an insolvent/nonviable bank.** That is the "Fundamental Constraint." Liquidity is not the cure when the problem is a capital hole — as the AHEL survey shows, even covering *all* short-term outflows often fails to stop a run when the market's real fear is viability, not liquidity. Policymakers must "take care not to misdiagnose the run on an institution's liquidity as the cause rather than the effect of its problems."
- **Solvency repair is fiscal, not monetary.** If the two banks are genuinely insolvent after write-downs, the correct tools are *capital injection, restructuring, or resolution* (bail-in, sale, merger, or an asset-management-company carve-out of the bad fund exposures), decided by fiscal/resolution authorities — not central-bank lending disguised as liquidity. The AHEL survey does note that authorities in practice assess *viability* (going-concern value assuming feasible support) rather than strict accounting solvency, but the point stands that lending to a truly nonviable firm imposes losses, stigma, and drift into fiscal policy.

## Cross-cutting requirements

- **Communicate relentlessly and clearly.** Every survey stresses this. Explain what's guaranteed, the steps taken to verify soundness, and the limits of the guarantees. Yes Bank 2020 and US 1933 both paired action with reassuring communication about the soundness of surviving institutions.
- **Don't over-promise beyond your fiscal capacity.** Ecuador 1999 shows an over-promised guarantee that the public didn't believe voids its own stabilizing effect. Guarantee credibility scales with fiscal resources and political unity.
- **Address moral hazard in the chronic phase, not the acute phase.** While you're fighting the run, don't impose punitive conditions that discourage banks from using your facilities. Once stabilized, use heightened supervision, interest-rate caps on guaranteed deposits, and bans on aggressive marketing to manage the distortions — and revisit the regulatory gap that let opaque fund exposures build up unmonitored in the first place.

## Bottom line

**Yes, the government should act — but in a specific sequence.**

1. **Immediately** stop the run with credible, broadly-scoped confidence measures — expanded deposit insurance and LOLR liquidity to viable banks, escalating to a wider guarantee if the run doesn't break, and extending the perimeter to cover whatever runnable liabilities (including nonbank/fund claims) are actually running.
2. **Simultaneously, buy time and differentiate** — ring-fence the two clearly troubled banks with a *targeted* moratorium (not, at first, a system-wide bank holiday), and run a credible, disclosed asset-quality review + stress test to map the unknown exposures.
3. **Then repair actual solvency** — recapitalize or resolve institutions based on *viability*, never using central-bank liquidity to keep a fundamentally insolvent bank alive; solvency holes are a fiscal problem for capital injection or resolution.

Throughout: match the scope of the intervention to the scope of the actual problem, keep guarantees within credible fiscal limits, communicate clearly, and defer moral-hazard discipline to the chronic phase.

The scenario closest to yours in the corpus is **India–Yes Bank 2020** (pre-emptive deposit-insurance expansion + targeted moratorium on the one bad bank kept contagion minimal), reinforced by **US–Reserve Primary Fund 2008** for the nonbank-origin transmission and the need to guarantee beyond insured deposits. The cautionary tales are **Ecuador 1999** (over-broad holiday + non-credible guarantee) and **Ireland/NAMA** (a diagnosis you can't fiscally back can deepen the crisis).