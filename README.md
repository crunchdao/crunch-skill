# Crunch Protocol Skills

Skills for [Crunch Protocol](https://www.crunchdao.com/) to help you (or your agents) manage competitions and participate in them.

## Skills

| Skill | Description |
|---|---|
| [coordinator-skill](coordinator-skill/) | Manage coordinators, competitions, rewards, checkpoints, staking via `crunch-cli` |
| [cruncher-skill](cruncher-skill/) | Discover, set up, develop, test, and submit competition solutions |

## Prerequisites

```bash
# Coordinator CLI (Solana/protocol operations)
npm install -g @crunchdao/crunch-cli

# Coordinator node scaffolding is built into crunch-cli:
# crunch-cli init-workspace my-challenge

# Competition participation
curl -LsSf https://astral.sh/uv/install.sh | sh  # uv for Python env management
```

## Examples

### Coordinator CLI

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
```

**You:** _"show my staking positions"_

```
📊 Staking Positions
════════════════════════════════════════
  Coordinator      Delegated    Rewards
  AI Research Lab  5,000 CRNCH  120.5 CRNCH
  Data Science     2,000 CRNCH   45.2 CRNCH
```

### Competition Participation

**You:** _"set up synth and explain the example tracker"_

```
📖 Quickstarter Walkthrough: Example Tracker (Synth)
════════════════════════════════════════════════════════════
🎯 Goal: Predict probability distributions of future crypto price changes
🔌 Interface: Extend TrackerBase and implement predict()
🧠 Approach: Gaussian model — computes mean/std of 5-min returns
```

**You:** _"test my solution and submit"_

```
✅ crunch test — passed
✅ crunch push -m "Improved model" — submitted
```

## Security

- **Never add a Solana wallet keypair without knowing what you are doing and how to make this secure**
