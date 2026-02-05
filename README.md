# Crunch Protocol CLI Skill

An AI skill that provides a natural language interface to the [Crunch Protocol](https://www.crunchdao.com/) CLI (`crunch-cli`). It translates plain-English requests into the correct CLI commands for managing coordinators, competitions (crunches), rewards, checkpoints, and certificates on Solana.

Supports output formatting for Slack, Telegram, Discord, or plain text.

## What's in this repo

| File | Purpose |
|---|---|
| `SKILL.md` | The skill definition — command mappings, profile resolution, output formatting rules |
| `references/cli-reference.md` | Full `crunch-cli` command reference |
| `profiles.json.example` | Example profile configuration |
| `profiles.json` | Your local profiles (git-ignored) |

## Prerequisites

```bash
npm install -g @crunchdao/crunch-cli
crunch-cli --version
```

## Profile Setup

Profiles let you switch between networks / wallets / multisigs by name (e.g. _"list crunches for mainnet-crunch-coordinator"_).

1. **Copy the example file:**
   ```bash
   cp profiles.json.example profiles.json
   ```

2. **Fill in your values:**
   - `url` — RPC endpoint or moniker (`mainnet-beta`, `devnet`, …)
   - `wallet` — path to your Solana keypair
   - `multisigAddress` — Squads multisig address (if applicable)
   - `coordinatorWallet` — coordinator owner address

See the **Profiles** section in [`SKILL.md`](SKILL.md) for the full format and resolution rules.

## Examples

Just ask in plain English. The skill resolves profiles, builds the CLI command, runs it, and formats the output.

---

### **You:** _"get me information about the Synth crunch on mainnet"_

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

### **You:** _"list all crunches for mainnet-autonity"_

```
🏆 Crunches for coordinator RRs8...ttZQ
════════════════════════════════════════════════════════════
  1. Synth          🟢 Started    5000 USDC    132 models
  2. Chaos          🟢 Started    8000 USDC    453 models
  3. Q4 Challenge   ⚫ Ended      10000 USDC   1452 models
```

---

### **You:** _"create a checkpoint multisig proposal for the Synth crunch"_

```
crunch-cli -m "9WzDX..." crunch checkpoint-create "Synth" prizes.json
```

```
✅ Multisig proposal created
  Proposal:   https://v4.squads.so/transactions/...
  Crunch:     Synth
  Prize file: prizes.json (12 entries, 4800.00 USDC total)
  Status:     Awaiting signatures (1/2)
```

---

### **You:** _"what's the current checkpoint for Chaos, format for slack"_

```
crunch-cli crunch checkpoint-get-current "Chaos"
```

```
*📍 Checkpoint: Chaos*
━━━━━━━━━━━━━━━━━
• *Index:* 5
• *Total Payout:* 8,000 USDC
• *Distributed:* 2025-02-01
• *Claims:* 89/142
```

---

When a profile is active, its flags (`-u`, `-w`, `-m`) are injected automatically — you just ask in plain English.

## Security

- **Never commit `profiles.json`** — it contains API keys and wallet paths.
- The file is git-ignored by default.
