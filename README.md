# Crunch Protocol Skill

Skills for [Crunch Protocol](https://www.crunchdao.com/) to help you (or your agents) build out new competitions and participate in them. 

1. **Coordinator Skill** — Translates plain-English requests into `crunch-cli` commands for managing coordinators, competitions, rewards, and checkpoints on Solana.

2. **Cruncher Skill** — Helps participants discover, understand, improve, backtest, and submit solutions for CrunchDAO competitions.

## What's in this repo

```
crunch-skill/
├── coordinator-skill/               # Skill: Solana coordinator management
│   ├── SKILL.md
│   └── references/
│       └── cli-reference.md
├── cruncher-skill/        # Skill: competition participation
│   └── SKILL.md
├── profiles.json.example            # Example profile configuration
└── profiles.json                    # Your local profiles (git-ignored)
```

Two independent skills, each with their own `SKILL.md`:

| Skill | Description |
|---|---|
| `crunch-cli` | Translates plain English → `crunch-cli` commands for managing coordinators, crunches, rewards, checkpoints |
| `competition-quickstarters` | Discover, explain, improve, backtest, and submit competition solutions |

## Prerequisites

```bash
# Coordinator CLI (Solana operations)
npm install -g @crunchdao/crunch-cli
crunch-cli --version

# uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Competition workspace (one venv per competition — example: Synth)
mkdir -p ~/.crunch/workspace/competitions/synth && cd ~/.crunch/workspace/competitions/synth
uv venv && source .venv/bin/activate
uv pip install crunch-cli crunch-synth jupyter ipykernel --upgrade --quiet --progress-bar off
python -m ipykernel install --user --name synth --display-name "CrunchDAO - Synth"
# Get your token from: https://hub.crunchdao.com/competitions/synth/submit
crunch setup synth my-project --token <YOUR_TOKEN>
cd synth-my-project
```

## Profile Setup

Profiles let you switch between networks / wallets / multisigs by name (e.g. _"list crunches for m-jeremy"_).

1. Copy the example: `cp profiles.json.example profiles.json`
2. Fill in your RPC URL, wallet path, multisig address, coordinator wallet.

See the **Profiles** section in [`SKILL.md`](SKILL.md) for details.

## Examples

### Coordinator CLI

---

**You:** _"get me information about the Synth crunch on mainnet"_

```
📋 Crunch: Synth
════════════════════════════════════════════════════════════
  Address:         7AJj...KNBP
  Coordinator:     RRs8...ttZQ
  State:           🟢 Started
  Payout Amount:   5000.000000 USDC
  Vault Balance:   6110.000000 USDC
  Max Models:      2
  Checkpoints:     0
  Reward Vault:    77UU...yDiC
```

---

**You:** _"create a checkpoint multisig proposal for the Synth crunch"_

```
✅ Multisig proposal created
  Proposal:   https://v4.squads.so/transactions/...
  Crunch:     Synth
  Prize file: prizes.json (12 entries, 4800.00 USDC total)
  Status:     Awaiting signatures (1/2)
```

---

**You:** _"what's the current checkpoint for Chaos, format for slack"_

```
*📍 Checkpoint: Chaos*
━━━━━━━━━━━━━━━━━
• *Index:* 5
• *Total Payout:* 8,000 USDC
• *Distributed:* 2025-02-01
• *Claims:* 89/142
```

---

### Competition Quickstarters

---

**You:** _"show me quickstarters for Falcon"_

```
📚 Quickstarters for Falcon
════════════════════════════════════════
  1. NGBoost              Python  Submission   📓 notebook
     by Alexis GASSMANN
  2. EWMA Variance        Python  Submission   📓 notebook
     by Alexis GASSMANN
  3. Quantile Lin. Reg.   Python  Submission   📓 notebook
     by Alexis GASSMANN
```

---

**You:** _"set up synth and explain the example tracker"_

```
📖 Quickstarter Walkthrough: Example Tracker (Synth)
════════════════════════════════════════════════════════════

🎯 Goal
  Predict probability distributions of future crypto price changes
  across multiple assets (BTC, ETH, SOL, ...) and time horizons.

🔌 Interface
  Extend TrackerBase and implement: predict(asset, horizon, step) → distributions

🧠 Approach
  Gaussian model — computes mean/std of 5-min returns, scales by √(step/300).

⚠️ Limitations
  - Assumes normal distribution (ignores fat tails)
  - No volatility regime detection
  - No cross-asset correlation
```

---

**You:** _"propose improvements and test them"_

```
📊 Evaluation Results: MixtureTracker vs Baseline
════════════════════════════════════════════════════════════

                     Baseline      Yours        Δ
  BTC (24h CRPS)     0.4231       0.3812      -9.9% ✅
  ETH (24h CRPS)     0.3987       0.3654      -8.3% ✅
  SOL (24h CRPS)     0.5102       0.4890      -4.2% ✅
  ────────────────────────────────────────────────
  Overall             0.3856       0.3586      -7.0% ✅
```

---

**You:** _"submit my tracker to synth"_

```
✅ Ready to submit to Synth
  File:        my_tracker.py
  Interface:   TrackerBase.predict() ✓
  Imports:     all resolved ✓
  Platform:    https://hub.crunchdao.com/competitions/synth
```

---

## Security

- **Never commit `profiles.json`** — it contains API keys and wallet paths.
- The file is git-ignored by default.
