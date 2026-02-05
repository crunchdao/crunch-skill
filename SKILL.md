---
name: coordinator-cli
description: Natural language interface for Crunch Protocol coordinator-cli. Maps user requests to CLI commands for managing coordinators, competitions (crunches), rewards, and checkpoints. Supports output formatting for Slack, Telegram, Discord, or plain text.
---

# Crunch Protocol Coordinator CLI Skill

This skill translates natural language queries into `crunch-coordinator` CLI commands and formats outputs for various mediums.

## Setup

Ensure the CLI is installed globally:
```bash
npm install -g @crunchdao/coordinator-cli
```

Verify installation:
```bash
crunch-coordinator --version
```

Ask the user if they want to store different profiles. Profiles can be added in conversations and include following information: 

name: Name of the environment for quick reference
environment or rpc: 
   Can be devnet | mainnet  or an RPC URL
   use this to fill -u, --url <URL_OR_MONIKER>  URL for Solana's JSON RPC or moniker (or their first
                              letter): [mainnet-beta, testnet, devnet, localhost]
multisig: 
  Is the address of the Multisig (not the Vault of the multisig)
  -m, --multisig <address>    Squads multisig address for coordinator operations

wallet: 
  Only supported in multisig mode and if the wallet is a proposer only. Sets the Wallet and the solana wallet should be created locally.
  -w, --wallet <wallet>       Path to wallet keypair

coordinator: 
  The coordinator address to use. If this is set default to looking for this coordinators crunch for example. 

Store these profiles locally for lookup. When a user says; Get all the crunches of profile m-jeremy it would look for the profile and insert the values in the CLI. 

It is also possible to set the profile, eg: user coordinator profile m-jeremy

## Command Mapping Rules

### IMPORTANT: Direct Phrase Mapping

For speed and consistency, map these phrases **directly** to CLI commands without LLM interpretation:

| User Phrase Pattern | CLI Command |
|---------------------|-------------|
| `get info about crunch <name>` | `crunch-coordinator crunch get "<name>"` |
| `get crunch <name>` | `crunch-coordinator crunch get "<name>"` |
| `show crunch <name>` | `crunch-coordinator crunch get "<name>"` |
| `crunch details <name>` | `crunch-coordinator crunch get "<name>"` |
| `get coordinator <address>` | `crunch-coordinator get "<address>"` |
| `show coordinator` | `crunch-coordinator get` |
| `my coordinator` | `crunch-coordinator get` |
| `list crunches` | `crunch-coordinator crunches list` |
| `list my crunches` | `crunch-coordinator crunches list` |
| `show all crunches` | `crunch-coordinator crunches list` |
| `get config` | `crunch-coordinator get-config` |
| `coordinator config` | `crunch-coordinator get-config` |
| `checkpoint for <name>` | `crunch-coordinator crunch checkpoint-get-current "<name>"` |
| `current checkpoint <name>` | `crunch-coordinator crunch checkpoint-get-current "<name>"` |
| `set certificate` | `crunch-coordinator cert set` |
| `set cert` | `crunch-coordinator cert set` |
| `update certificate` | `crunch-coordinator cert set` |
| `get certificate` | `crunch-coordinator cert get` |
| `get cert` | `crunch-coordinator cert get` |
| `show certificate` | `crunch-coordinator cert get` |
| `my certificate` | `crunch-coordinator cert get` |
| `sweep tokens <name>` | `crunch-coordinator crunch sweep-token-accounts "<name>"` |
| `sweep token accounts <name>` | `crunch-coordinator crunch sweep-token-accounts "<name>"` |
| `check prize accounts <name>` | `crunch-coordinator crunch check-prize-atas "<name>"` |
| `check atas <name>` | `crunch-coordinator crunch check-prize-atas "<name>"` |
| `map cruncher addresses` | `crunch-coordinator crunch map-cruncher-addresses` |
| `emission checkpoint add` | `crunch-coordinator crunch emission-checkpoint-add` |

### Name Extraction Rules

- Crunch names often contain spaces: "Synth", "Q4 2024 Challenge", "AI Trading Competition"
- When a name is provided, wrap it in quotes in the CLI command
- Common competition names: Crunch, Competition, Tournament, Challenge

## Execution Pattern

1. **Parse** the user request to identify:
   - The action (get, create, start, end, list, etc.)
   - The target (crunch, coordinator, checkpoint, etc.)
   - The name/identifier if applicable
   - Any additional parameters

2. **Map** to CLI command using the direct mapping table above

3. **Execute** the command:
   ```bash
   crunch-coordinator [options] <command> [arguments]
   ```

4. **Format** output for the specified medium (see Output Formatting below)

## Available Commands Reference

### Coordinator Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `get [owner]` | Get coordinator details | `crunch-coordinator get [address]` |
| `get-config` | Get coordinator configuration | `crunch-coordinator get-config` |
| `register <name>` | Register new coordinator | `crunch-coordinator register "Name"` |
| `reset-hotkey` | Reset SMP hotkey | `crunch-coordinator reset-hotkey` |
| `set-emission-config` | Set emission percentages | `crunch-coordinator set-emission-config <coord%> <staker%> <fund%>` |

### Certificate Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `cert set <pubkey> [--slot N]` | Set certificate hash | `crunch-coordinator cert set "MIIBIjAN..." [--slot 0\|1]` |
| `cert get [owner]` | Get certificate info | `crunch-coordinator cert get [address]` |

### Crunch Commands (Competition Management)
| Command | Description | Usage |
|---------|-------------|-------|
| `crunch get <name>` | Get crunch details | `crunch-coordinator crunch get "Synth"` |
| `crunches list [wallet]` | List all crunches | `crunch-coordinator crunches list` |
| `crunch create` | Create new crunch | `crunch-coordinator crunch create "Name" <payoutUSDC> [maxModels]` |
| `crunch start <name>` | Start competition | `crunch-coordinator crunch start "Name"` |
| `crunch end <name>` | End competition | `crunch-coordinator crunch end "Name"` |
| `crunch deposit-reward` | Deposit USDC | `crunch-coordinator crunch deposit-reward "Name" <amount>` |
| `crunch margin <name>` | Execute margin payout | `crunch-coordinator crunch margin "Name"` |
| `crunch drain <name>` | Drain remaining USDC | `crunch-coordinator crunch drain "Name"` |
| `crunch get-cruncher` | Get cruncher details | `crunch-coordinator crunch get-cruncher "CrunchName" <wallet>` |
| `crunch sweep-token-accounts` | Sweep tokens to vault | `crunch-coordinator crunch sweep-token-accounts "Name"` |
| `crunch check-prize-atas` | Check USDC accounts | `crunch-coordinator crunch check-prize-atas "Name"` |
| `crunch map-cruncher-addresses` | Map cruncher addresses | `crunch-coordinator crunch map-cruncher-addresses "CoordName"` |
| `crunch emission-checkpoint-add` | Add emission checkpoint | `crunch-coordinator crunch emission-checkpoint-add "CoordName" <amount>` |

### Checkpoint Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `crunch checkpoint-create` | Create checkpoint | `crunch-coordinator crunch checkpoint-create "Name" prizes.json [--dryrun]` |
| `crunch checkpoint-get-current` | Current checkpoint | `crunch-coordinator crunch checkpoint-get-current "Name"` |
| `crunch checkpoint-get` | Get checkpoint by index | `crunch-coordinator crunch checkpoint-get "Name" <index>` |

### Global Options
- `-u, --url <network>` - Network: mainnet-beta, devnet, localhost (default: from config)
- `-w, --wallet <path>` - Wallet keypair file path
- `-o, --output json` - Output as JSON (useful for parsing)
- `-m, --multisig <addr>` - Create multisig proposal instead of direct execution

## Output Formatting

### Medium Detection
Detect output medium from user request:
- "for slack" / "slack format" → Slack
- "for telegram" / "telegram format" → Telegram  
- "for discord" / "discord format" → Discord
- Default → Plain text / Markdown

### Slack Format
```
*🏆 Crunch: Synth*
━━━━━━━━━━━━━━━━━
• *Status:* Active
• *Participants:* 142
• *Prize Pool:* 10,000 USDC
• *Checkpoint:* 5
* *Funds:* 3000USDC
```

### Telegram Format
```
🏆 <b>Crunch: Synth</b>

📊 Status: Active
👥 Participants: 142  
💰 Prize Pool: 10,000 USDC
📍 Checkpoint: 5
💰 Funds: 3000USDC
```

### Discord Format
```
## 🏆 Crunch: Synth
**Status:** Active
**Participants:** 142
**Prize Pool:** 10,000 USDC
**Checkpoint:** 5
```

### Plain Text / Default
```
Crunch: Synth
Status: Active
Participants: 142
Prize Pool: 10,000 USDC
Checkpoint: 5
Funds: 3000USDC
```

## Error Handling

If a command fails:
1. Show user-friendly error message
2. Suggest possible fixes:
   - Wrong network? Add `-u devnet` or `-u mainnet-beta`
   - Missing wallet? Add `-w /path/to/wallet.json`
   - Crunch not found? List available crunches with `crunches list`

## Example Workflows

### "Get me info about crunch Synth"
```bash
crunch-coordinator crunch get "Synth"
```

### "Show my coordinator on mainnet"
```bash
crunch-coordinator -u mainnet-beta get
```

### "List all crunches for slack"
```bash
crunch-coordinator crunches list
```
Then format output for Slack.

### "What's the current checkpoint for the Chaos competition?"
```bash
crunch-coordinator crunch checkpoint-get-current "Chaos"
```

## Reference Documentation

For full CLI documentation, see [references/cli-reference.md](references/cli-reference.md).
