# Coordinator CLI Full Reference

## Package Information
- **Name:** `@crunchdao/coordinator-cli`
- **Binary:** `crunch-coordinator`
- **Version:** 4.3.2+

## Installation

```bash
npm install -g @crunchdao/coordinator-cli
```

## Configuration

### Global Config File
Location: `~/.crunch/config.json`

```json
{
  "network": "devnet",
  "wallet": "./accounts/coordinator.json",
  "loglevel": "info"
}
```

### Config Commands
```bash
crunch-coordinator config set <key> <value>
crunch-coordinator config show
crunch-coordinator config use-profile <profile>
```

## Network Options

| Moniker | Description |
|---------|-------------|
| `mainnet-beta` | Solana Mainnet |
| `devnet` | Solana Devnet |
| `testnet` | Solana Testnet |
| `localhost` | Local validator (127.0.0.1:8899) |

## Complete Command Reference

### Coordinator Management

#### `register <name>`
Register a new coordinator with the protocol.

```bash
crunch-coordinator register "AI Research Lab"
```

**Requirements:**
- Unique coordinator name
- Sufficient SOL for account creation
- Later requires admin approval

---

#### `get [owner]`
Get coordinator details by owner address.

```bash
# Current wallet
crunch-coordinator get

# Specific address
crunch-coordinator get "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
```

**Output Fields:**
- Owner address
- Coordinator name
- Registration status
- Approval status
- Hotkey information

---

#### `get-config`
Get coordinator configuration from the protocol.

```bash
crunch-coordinator get-config
```

**Output Fields:**
- Protocol parameters
- Fee configurations
- Margin percentages

---

#### `reset-hotkey`
Reset/regenerate the SMP hotkey for the coordinator.

```bash
crunch-coordinator reset-hotkey
```

---

#### `set-emission-config <coordinatorPct> <stakerPct> <crunchFundPct>`
Set emission configuration percentages.

```bash
crunch-coordinator set-emission-config 50 40 10
```

**Note:** Percentages must sum to 100.

---

### Competition (Crunch) Management

#### `crunches list [wallet]`
List all crunches for a coordinator.

```bash
# Current wallet
crunch-coordinator crunches list

# Specific coordinator
crunch-coordinator crunches list "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
```

**Output:**
- List of all crunches
- Names, statuses, participant counts

---

#### `crunch create <name> <payoutAmount> [maxModelsPerCruncher]`
Create a new crunch competition.

```bash
crunch-coordinator crunch create "Q4 2024 Trading Challenge" 10000 5
```

**Arguments:**
- `name` - Competition name (unique)
- `payoutAmount` - Prize pool in USDC
- `maxModelsPerCruncher` - Max models per participant (default: 2)

---

#### `crunch get <name>`
Get detailed information about a competition.

```bash
crunch-coordinator crunch get "Synth"
```

**Output Fields:**
- Name and status
- Coordinator info
- Participant count
- Prize pool balance
- Checkpoint information
- Created/started/ended timestamps
- Configuration parameters

---

#### `crunch start <name>`
Start a competition (transitions from Created to Active).

```bash
crunch-coordinator crunch start "Q4 2024 Trading Challenge"
```

**Requirements:**
- Competition must be in Created state
- Must be the creating coordinator

---

#### `crunch end <name>`
End a competition (transitions from Active to Ended).

```bash
crunch-coordinator crunch end "Q4 2024 Trading Challenge"
```

**Requirements:**
- Competition must be in Active state
- Must be the creating coordinator

---

#### `crunch get-cruncher <crunchName> <cruncherWallet>`
Get cruncher details for a specific competition.

```bash
crunch-coordinator crunch get-cruncher "Synth" "5abc..."
```

**Output:**
- Cruncher registration info
- Model submissions
- Rewards claimed
- Performance data

---

### Financial Commands

#### `crunch deposit-reward <crunchName> <amount>`
Deposit USDC rewards to a competition.

```bash
crunch-coordinator crunch deposit-reward "Synth" 5000
```

**Requirements:**
- Sufficient USDC balance in wallet
- Competition must exist

---

#### `crunch margin <crunchName>`
Execute margin payout for a competition.

```bash
crunch-coordinator crunch margin "Synth"
```

---

#### `crunch drain <crunchName>`
Drain remaining USDC from a competition.

```bash
crunch-coordinator crunch drain "Synth"
```

**Use Case:** Recover unspent funds after competition ends

---

### Checkpoint Commands

#### `crunch checkpoint-create <crunchName> <prizeFileName> [--dryrun]`
Create a checkpoint for payout distribution.

```bash
crunch-coordinator crunch checkpoint-create "Synth" "./prizes.json"

# Dry run (no execution)
crunch-coordinator crunch checkpoint-create "Synth" "./prizes.json" --dryrun
```

**Prize File Format (JSON Lines):**
```json
{"timestamp": 1840417288969, "model": "model_1", "prize": 456.78}
{"timestamp": 1840417288969, "model": "model_2", "prize": 412.34}
{"timestamp": 1840417288969, "model": "model_3", "prize": 130.88}
```

---

#### `crunch checkpoint-get-current <crunchName>`
Get the current checkpoint information.

```bash
crunch-coordinator crunch checkpoint-get-current "Synth"
```

**Output:**
- Checkpoint index
- Total payout amount
- Distribution timestamp
- Claim status

---

#### `crunch checkpoint-get <crunchName> <checkpointIndex>`
Get checkpoint by index.

```bash
crunch-coordinator crunch checkpoint-get "Synth" 3
```

---

#### `crunch checkpoint-get-address <crunchName> <checkpointIndex>`
Get the Solana address of a checkpoint account.

```bash
crunch-coordinator crunch checkpoint-get-address "Synth" 3
```

---

### Utility Commands

#### `crunch check-prize-atas <crunchName> <prizeFileName> [-c]`
Check if crunchers have USDC Associated Token Accounts.

```bash
# Check only
crunch-coordinator crunch check-prize-atas "Synth" "./prizes.json"

# Create missing ATAs
crunch-coordinator crunch check-prize-atas "Synth" "./prizes.json" -c
```

---

#### `crunch set-fund-config <crunchName> <cruncherPct> <dataproviderPct> <computeProviderPct>`
Set fund configuration for a crunch.

```bash
crunch-coordinator crunch set-fund-config "Synth" 70 20 10
```

**Note:** Percentages must sum to 100.

---

#### `crunch emission-checkpoint-add <emissionFile>`
Add an emission checkpoint to the coordinator pool.

```bash
crunch-coordinator crunch emission-checkpoint-add "./emissions.json"
```

---

#### `crunch map-cruncher-addresses <crunchAddress> <wallets...>`
Map cruncher wallets into the coordinator pool address index.

```bash
crunch-coordinator crunch map-cruncher-addresses "CrunchAddr..." "Wallet1..." "Wallet2..."
```

---

## Multisig Operations

For production environments, use multisig for critical operations:

```bash
crunch-coordinator --multisig <SQUADS_MULTISIG_ADDR> <command>
```

**Multisig-Compatible Commands:**
- `register`
- `crunch create`
- `crunch start`
- `crunch end`
- `crunch deposit-reward`
- `crunch drain`

**Example:**
```bash
crunch-coordinator --multisig 9WzDX... crunch create "Production Competition" 50000 3
```

This creates a Squads proposal instead of direct execution.

---

## JSON Output Mode

For programmatic parsing, use JSON output:

```bash
crunch-coordinator -o json crunch get "Synth"
```

All commands support `-o json` for structured output.

---

## Typical Competition Workflow

1. **Register:** `crunch-coordinator register "My Coordinator"`
2. **Get Approved:** Wait for admin approval
3. **Create:** `crunch-coordinator crunch create "My Competition" 10000 2`
4. **Fund:** `crunch-coordinator crunch deposit-reward "My Competition" 10000`
5. **Start:** `crunch-coordinator crunch start "My Competition"`
6. **Monitor:** `crunch-coordinator crunch get "My Competition"`
7. **Checkpoint:** `crunch-coordinator crunch checkpoint-create "My Competition" prizes.json`
8. **End:** `crunch-coordinator crunch end "My Competition"`
9. **Drain:** `crunch-coordinator crunch drain "My Competition"`
