# Query 2 — no-rag

Model: anthropic/claude-opus-4.8 | Retrieval: no-rag | System prompt: none
Tool calls: none (plain model)

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

# Assessing the Situation

This scenario describes a classic **contagion problem**: the actual losses may be contained to a few institutions, but *uncertainty* about who is exposed is causing indiscriminate runs across the sector. This distinction matters enormously for the policy response.

## First, Diagnose: Illiquidity vs. Insolvency

Before acting, the key question is whether affected banks are:

- **Illiquid but solvent** — fundamentally sound, but facing runs because depositors can't distinguish them from the truly exposed banks. This is a coordination failure that intervention can genuinely fix.
- **Insolvent** — their commitments to the fund actually exceed their capital. No amount of liquidity support makes them viable.

The problem is you often can't tell these apart in real time, which is precisely why runs spread.

## Tools Available

**1. Information / Transparency (often the cheapest fix)**
- Rapid supervisory review to identify actual exposures, then disclose which banks are sound.
- A credible stress test can break the "unknown pattern of exposures" dynamic that drives indiscriminate panic. This was arguably the most effective single US action in 2009.

**2. Liquidity Support (Bagehot's classic prescription)**
- Central bank lends freely to solvent institutions against good collateral, at a penalty rate.
- Addresses runs without bailing out bad decisions. This is the least distortionary intervention.

**3. Guarantees**
- Temporary expansion of deposit insurance or blanket guarantees can stop runs by removing the incentive to flee.
- Powerful but blunt — creates large contingent liabilities and moral hazard.

**4. Resolution / Recapitalization**
- For genuinely insolvent banks: orderly resolution, wiping out equity and imposing losses on those who took the risk, while protecting depositors and critical functions.

## What I'd Recommend

1. **Triage immediately** — supervisors identify the real exposures. Separate the two troubled banks from the rest.
2. **Provide liquidity to solvent institutions** as lender of last resort to stop the panic bleeding while diagnosis proceeds.
3. **Disclose credibly** to break the information asymmetry driving the sector-wide run.
4. **Resolve the truly insolvent banks** through the resolution regime — protect depositors and systemic functions, but impose losses on shareholders, management, and where appropriate creditors of the failed institutions.
5. **Do not** provide blanket bailouts to the private-debt fund investors or the banks' equity holders.

## Key Principles Underlying This

- **Distinguish protecting the *system* from protecting *individual actors*.** The goal is preventing a solvent, functioning sector from being destroyed by panic — not sparing those who made the losing bets.
- **Moral hazard is real but secondary in an acute crisis.** Refusing to act to "teach a lesson" can convert a containable problem into a systemic collapse. But rescues should be structured to punish risk-takers (equity wiped out, management removed) so the lesson is still learned.
- **Speed and credibility matter more than precision.** Half-measures that don't convince markets can be worse than nothing.

## Honest Caveats

- The right answer depends on facts I've assumed: how large the true losses are relative to sector capital, whether these are systemically important banks, and your jurisdiction's fiscal capacity and legal resolution powers.
- There's genuine disagreement among economists here — some would argue for a stricter "let insolvent institutions fail" stance to preserve market discipline, accepting more short-term pain.
- If the whole sector is *actually* insolvent (not just panicked), that's a different and much harder problem requiring recapitalization or restructuring, not just liquidity.

Would you like me to work through a specific variation — say, if the two banks turn out to be genuinely insolvent, or if fiscal capacity is constrained?