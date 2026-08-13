# Query 2 — no-rag

Model: anthropic/claude-opus-4.8 | Retrieval: no-rag | System prompt: none
Tool calls: none (plain model)

**Prompt:** A large private-debt fund has just incurred a major loss, and the investors in this fund are facing significant write-downs on their positions. You have just learned that two large regional banks in your jurisdiction have made large commitments to this fund, and now have solvency concerns of their own. Investors and depositors are now worried about exposures at other regional banks, and since the exact pattern of exposures is unknown, the whole sector is facing runs. What, if anything, should the government do?

---

# Assessing the Situation and Policy Response

This scenario describes a classic **contagion problem** where uncertainty about which institutions are exposed drives indiscriminate runs. Here's how I'd think through the response.

## First, Diagnose the Problem

The critical distinction is **illiquidity vs. insolvency**:

- **Liquidity crisis**: Fundamentally sound banks facing runs purely because depositors can't distinguish healthy from exposed institutions. This is an information problem.
- **Solvency crisis**: Banks that are genuinely underwater regardless of the run.

The scenario suggests *both* are present—two banks have real solvency concerns, but the sector-wide runs are driven by uncertainty ("exact pattern of exposures is unknown"). This mixed picture shapes everything.

## Core Principles for Response

**1. Address illiquidity aggressively; treat insolvency carefully**

The Bagehot principle applies: lend freely, at a penalty rate, against good collateral, to solvent institutions. A central bank liquidity facility can stop runs on healthy banks without committing taxpayer funds to losses.

**2. Resolve uncertainty quickly**

Much of the panic stems from opacity. Rapid, credible **stress testing or supervisory review** to identify actual exposures can restore discrimination between sound and unsound banks. Panics thrive on ambiguity.

**3. Protect the system, not necessarily every institution**

- Insured depositors should be protected (this is what deposit insurance exists for).
- Equity and unsecured creditors of genuinely insolvent banks should generally bear losses to preserve market discipline and limit moral hazard.

## Concrete Tools

| Tool | When appropriate |
|------|-----------------|
| Emergency liquidity provision | Immediately, for solvent-but-illiquid banks |
| Temporary deposit guarantee expansion | If runs threaten fundamentally sound institutions |
| Rapid supervisory review | To resolve the information problem |
| Orderly resolution of the two exposed banks | If genuinely insolvent—wind down or force sale |
| Bridge bank / purchase & assumption | To preserve function while imposing losses on shareholders |

## Key Tensions to Weigh

- **Moral hazard**: Bailing out the *fund's* investors or bank shareholders rewards risk-taking. The private-debt fund losses should generally *not* be socialized.
- **Speed vs. discrimination**: Acting fast prevents cascade but risks protecting the undeserving. Liquidity support is reversible; bailouts are not.
- **Precedent**: Whatever you do here becomes the expectation for the next crisis.

## My Recommendation

1. **Immediately** open a liquidity facility for the sector to stop runs on healthy banks.
2. **Rapidly and transparently** assess actual exposures to break the uncertainty.
3. **Guarantee insured deposits** and consider temporary broader guarantees if runs continue.
4. **Resolve the two exposed banks** through the normal resolution framework—imposing losses on shareholders and possibly creditors, protecting depositors.
5. **Let the fund's investors take their losses.** The original private-debt loss is not the government's problem to absorb.

The government's proper role is to prevent an *information-driven panic* from destroying *solvent* institutions—not to prevent losses on bad investments.

---

*Note: This is a general analytical framework, not specific policy or legal advice. Real decisions would depend on the jurisdiction's legal authorities, fiscal capacity, and precise institutional details.*