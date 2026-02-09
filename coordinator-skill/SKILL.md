---
name: crunch-cli
description: Use when managing CrunchDAO coordinators, competitions (crunches), rewards, checkpoints, or certificates via the crunch-cli.
---

# Crunch Protocol CLI Skill

Translates natural language queries into `crunch-cli` commands. Supports profiles and output formatting for Slack, Telegram, Discord, or plain text.

## Setup

```bash
npm install -g @crunchdao/crunch-cli
crunch-cli --version
```

## Profiles

Profiles in `profiles.json` (repo root) map short names to CLI flags. Users say _"list crunches for m-jeremy"_ instead of typing full addresses.

```json
{
  "profiles": {
    "m-jeremy": {
      "url": "https://mainnet.helius-rpc.com/?api-key=...",
      "wallet": "/path/to/keypair.json",
      "multisigAddress": "9WzDXwBbmkg8...",
      "coordinatorWallet": "5abc..."
    }
  }
}
```

| Profile field | CLI flag | Notes |
|---|---|---|
| `url` | `-u <value>` | RPC URL or moniker: `mainnet-beta`, `devnet`, `testnet`, `localhost` |
| `wallet` | `-w <value>` | Path to Solana keypair (for multisig proposers) |
| `multisigAddress` | `-m <value>` | Squads multisig address |
| `coordinatorWallet` | appended to `coordinator get` | Default coordinator context |

When user references a profile, load from `profiles.json`, map fields to flags, prepend to command.

## Direct Phrase Mapping

| User Phrase | CLI Command |
|-------------|-------------|
| `get/show crunch <name>` | `crunch-cli crunch get "<name>"` |
| `get/show coordinator [address]` | `crunch-cli coordinator get [address]` |
| `list crunches` | `crunch-cli crunches list` |
| `get config` | `crunch-cli coordinator get-config` |
| `checkpoint for <name>` | `crunch-cli crunch checkpoint-get-current "<name>"` |
| `set/update certificate` | `crunch-cli coordinator cert set` |
| `get/show certificate` | `crunch-cli coordinator cert get` |
| `sweep tokens <name>` | `crunch-cli crunch sweep-token-accounts "<name>"` |
| `check prize accounts <name>` | `crunch-cli crunch check-prize-atas "<name>"` |
| `list scenarios/simulations` | `crunch-cli model list` |
| `run simulation <scenario>` | `crunch-cli model run "<scenario>"` |
| `validate scenario <scenario>` | `crunch-cli model validate "<scenario>"` |

## Execution Pattern

1. **Parse** — Identify action, target, name/identifier, parameters
2. **Resolve profile** — If mentioned, prepend profile flags
3. **Map** — Use phrase mapping table
4. **Execute** — Run command
5. **Format** — Output for requested medium (Slack/Telegram/Discord/plain)

## Output Formatting

Detect medium from user request ("for slack", "telegram format", etc.):

- **Slack:** `*bold*`, `•` bullets, `━` separators
- **Telegram:** `<b>bold</b>`, emoji prefixes
- **Discord:** `## headers`, `**bold**`
- **Plain:** Simple key: value pairs

## Error Handling

If command fails, suggest fixes:
- Wrong network? Add `-u devnet` or `-u mainnet-beta`
- Missing wallet? Add `-w /path/to/wallet.json`
- Not found? List available with `crunches list`

## Reference

For full CLI documentation: [references/cli-reference.md](references/cli-reference.md)
