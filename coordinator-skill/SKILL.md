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

The CLI has built-in profile management via `~/.crunch/config.json`:

```bash
crunch-cli config show                    # Show current config
crunch-cli config set <key> <value>       # Set config value
crunch-cli config use-profile <profile>   # Switch profile
```

When user says _"use profile m-jeremy"_ or _"switch to devnet"_:
```bash
crunch-cli config use-profile m-jeremy
```

Global flags can override config per-command:

| Flag | Description |
|------|-------------|
| `-u <url>` | RPC URL or moniker: `mainnet-beta`, `devnet`, `testnet`, `localhost` |
| `-w <path>` | Path to Solana keypair |
| `-m <addr>` | Squads multisig address |

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

## Coordinator Node Setup

To run your own coordinator node (backend infrastructure for competitions):

1. Fork https://github.com/crunchdao/coordinator-node-starter
2. Clone your fork and follow its `SKILL.md` for setup and customization

## Reference

For full CLI documentation: [references/cli-reference.md](references/cli-reference.md)
