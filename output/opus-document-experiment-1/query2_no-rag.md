# Query 2 — no-rag

Model: anthropic/claude-opus-4.8 | Retrieval: no-rag | System prompt: none
Tool calls: none (plain model)

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

# Assessing the Situation

This scenario has the hallmarks of a **contagion-driven liquidity crisis** with potential solvency problems underneath. The key challenge is distinguishing between the two, because they call for different responses. Let me work through the considerations rather than jump to a prescription.

## The Central Diagnostic Question

**Is this fundamentally a liquidity problem or a solvency problem?**

- **Liquidity problem:** Banks are basically sound but face runs because depositors can't tell who's exposed. The panic itself is the main threat. This is the classic case for intervention.
- **Solvency problem:** The losses are real and large enough that some banks are genuinely insolvent. Propping these up wastes public money and creates moral hazard.

The honest answer early in a crisis is that you *don't know yet*, and the exposures are opaque by your own description. This uncertainty is what's driving the indiscriminate runs.

## The Case for Acting

The strongest argument for intervention is **Bagehot's principle**: in a panic, lend freely, against good collateral, at a penalty rate. If the runs are hitting solvent banks simply because investors can't distinguish them from the two troubled ones, doing nothing risks turning a contained problem into a systemic collapse—healthy institutions fail simply because everyone withdraws at once.

## The Case for Restraint

- **Moral hazard:** Bailing out investors in a risky private-debt fund, or the banks that overcommitted to it, rewards bad risk management and encourages future recklessness.
- **Fiscal and political cost:** Public money is at stake, and the perception of rescuing wealthy fund investors is corrosive to legitimacy.
- **The private-debt fund itself is not a public concern.** Its investors chose that risk and should bear losses.

## A Layered Response

Rather than "bail out" or "do nothing," I'd sequence tools by escalating cost and intrusiveness:

1. **Information first.** The runs are driven by *unknown* exposure patterns. Rapidly gather and, where possible, disclose which banks are actually exposed and how much. Transparency can halt indiscriminate panic by letting markets distinguish sound banks from troubled ones.

2. **Liquidity support to solvent institutions.** Central bank lending against good collateral to banks that are illiquid but solvent. This addresses the run without underwriting losses.

3. **Deposit guarantees.** Reaffirm or temporarily expand deposit insurance to stop depositor flight. Depositors typically aren't the ones who should be punished for taking risk.

4. **Resolution, not rescue, for the insolvent.** For genuinely insolvent banks, use orderly resolution—wipe out equity, impose losses on unsecured creditors and the fund's investors, protect depositors, and transfer viable operations. Owners and risk-takers bear losses; the system is stabilized.

## What the Government Should *Not* Do

- Bail out the private-debt fund or its investors.
- Rescue bank shareholders and management who made the bad commitments.
- Guarantee everything indiscriminately, which maximizes moral hazard.

## Bottom Line

The government should act, but the intervention should target the **panic and the payment/deposit system**, not the losses. Protect the solvent through liquidity and credible guarantees; resolve the insolvent while imposing losses on those who took the risk. The guiding principle: **stabilize the system, not the speculators.**

Two caveats worth flagging: the speed of a run often forces decisions before you have full information, and there's an inherent tension between the credibility of "no bailouts" (good for long-run incentives) and the need to be reassuringly generous during an acute panic (good for stopping it now). Managing that tension is the real art here.