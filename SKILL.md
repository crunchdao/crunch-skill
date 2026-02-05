---
name: crunch-protocol-skill
description: Natural language interface for CrunchDAO. Manages coordinators and competitions via the crunch-cli, and helps participants discover, understand, improve, backtest, and submit quickstarter solutions for CrunchDAO competitions.
---

# Crunch Protocol CLI Skill

This skill translates natural language queries into `crunch-cli` CLI commands and formats outputs for various mediums.

## Setup

Ensure the CLI is installed globally:
```bash
npm install -g @crunchdao/crunch-cli
```

Verify installation:
```bash
crunch-cli --version
```

## Profiles

Profiles are stored in `profiles.json` (next to this file). Each profile maps a short name to a set of CLI flags so users can say things like _"list crunches for m-jeremy"_ instead of typing full addresses every time.

### Profile file format

```json
{
  "profiles": {
    "m-jeremy": {
      "url": "https://mainnet.helius-rpc.com/?api-key=...",
      "wallet": "/path/to/keypair.json",
      "multisigAddress": "9WzDXwBbmkg8...",
      "coordinatorWallet": "5abc..."
    },
    "devnet": {
      "url": "devnet",
      "wallet": "/path/to/dev-keypair.json",
      "coordinatorWallet": ""
    }
  }
}
```

### Profile fields → CLI flags

| Profile field | CLI flag | Notes |
|---|---|---|
| `url` | `-u <value>` | RPC URL or moniker: `mainnet-beta`, `devnet`, `testnet`, `localhost` |
| `wallet` | `-w <value>` | Path to Solana keypair. Only used in multisig mode when the wallet is a proposer. |
| `multisigAddress` | `-m <value>` | Squads multisig address (not the vault). |
| `coordinatorWallet` | appended to `coordinator get` | The coordinator owner address. When set, default to this coordinator's context (e.g. listing its crunches). |

### How to resolve a profile

When a user references a profile name:

1. Read `profiles.json` from the skill directory.
2. Look up the profile by name (case-insensitive match).
3. Map each non-empty field to its CLI flag (see table above).
4. Prepend the flags to whatever command is being built.

**Example:** User says _"list crunches for m-jeremy"_

1. Load profile `mainnet-proposer` → `{ url: "https://mainnet...", wallet: "/path/...", multisigAddress: "9WzDX..." }`
2. Build: `crunch-cli -u "https://mainnet..." -w "/path/..." -m "9WzDX..." crunches list`

**Example:** User says _"show coordinator for devnet"_

1. Load profile `devnet` → `{ url: "devnet" }`
2. Build: `crunch-cli -u devnet coordinator get`

### Managing profiles

- Users can ask to **add**, **update**, or **remove** profiles. When they do, read the current `profiles.json`, apply the change, and write it back.
- If `profiles.json` doesn't exist yet, create it with the structure above.
- When a user says _"set profile to m-jeremy"_ or _"use profile m-jeremy"_, remember it for the rest of the conversation and apply those flags to all subsequent commands automatically.

## Command Mapping Rules

### IMPORTANT: Direct Phrase Mapping

For speed and consistency, map these phrases **directly** to CLI commands without LLM interpretation:

| User Phrase Pattern | CLI Command |
|---------------------|-------------|
| `get info about crunch <name>` | `crunch-cli crunch get "<name>"` |
| `get crunch <name>` | `crunch-cli crunch get "<name>"` |
| `show crunch <name>` | `crunch-cli crunch get "<name>"` |
| `crunch details <name>` | `crunch-cli crunch get "<name>"` |
| `get coordinator <address>` | `crunch-cli coordinator get "<address>"` |
| `show coordinator` | `crunch-cli coordinator get` |
| `my coordinator` | `crunch-cli coordinator get` |
| `list crunches` | `crunch-cli crunches list` |
| `list my crunches` | `crunch-cli crunches list` |
| `show all crunches` | `crunch-cli crunches list` |
| `get config` | `crunch-cli coordinator get-config` |
| `coordinator config` | `crunch-cli coordinator get-config` |
| `checkpoint for <name>` | `crunch-cli crunch checkpoint-get-current "<name>"` |
| `current checkpoint <name>` | `crunch-cli crunch checkpoint-get-current "<name>"` |
| `set certificate` | `crunch-cli coordinator cert set` |
| `set cert` | `crunch-cli coordinator cert set` |
| `update certificate` | `crunch-cli coordinator cert set` |
| `get certificate` | `crunch-cli coordinator cert get` |
| `get cert` | `crunch-cli coordinator cert get` |
| `show certificate` | `crunch-cli coordinator cert get` |
| `my certificate` | `crunch-cli coordinator cert get` |
| `sweep tokens <name>` | `crunch-cli crunch sweep-token-accounts "<name>"` |
| `sweep token accounts <name>` | `crunch-cli crunch sweep-token-accounts "<name>"` |
| `check prize accounts <name>` | `crunch-cli crunch check-prize-atas "<name>"` |
| `check atas <name>` | `crunch-cli crunch check-prize-atas "<name>"` |
| `map cruncher addresses` | `crunch-cli crunch map-cruncher-addresses` |
| `emission checkpoint add` | `crunch-cli crunch emission-checkpoint-add` |

### Name Extraction Rules

- When a crunch name is provided, wrap it in quotes in the CLI command
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
   crunch-cli [options] <command> [arguments]
   ```

4. **Format** The output of the CLI should be kept as close as possible, except if the user told you to post process the data. But map the output for the specified medium (see Output Formatting below as reference to use)

## Available Commands Reference

### Coordinator Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `coordinator get [owner]` | Get coordinator details | `crunch-cli coordinator get [address]` |
| `coordinator get-config` | Get coordinator configuration | `crunch-cli coordinator get-config` |
| `coordinator register <name>` | Register new coordinator | `crunch-cli coordinator register "Name"` |
| `coordinator reset-hotkey` | Reset SMP hotkey | `crunch-cli coordinator reset-hotkey` |
| `coordinator set-emission-config` | Set emission percentages | `crunch-cli coordinator set-emission-config <coord%> <staker%> <fund%>` |

### Certificate Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `coordinator cert set <pubkey> [--slot N]` | Set certificate hash | `crunch-cli coordinator cert set "MIIBIjAN..." [--slot 0\|1]` |
| `coordinator cert get [owner]` | Get certificate info | `crunch-cli coordinator cert get [address]` |

### Crunch Commands (Competition Management)
| Command | Description | Usage |
|---------|-------------|-------|
| `crunch get <name>` | Get crunch details | `crunch-cli crunch get "Synth"` |
| `crunches list [wallet]` | List all crunches | `crunch-cli crunches list` |
| `crunch create` | Create new crunch | `crunch-cli crunch create "Name" <payoutUSDC> [maxModels]` |
| `crunch start <name>` | Start competition | `crunch-cli crunch start "Name"` |
| `crunch end <name>` | End competition | `crunch-cli crunch end "Name"` |
| `crunch deposit-reward` | Deposit USDC | `crunch-cli crunch deposit-reward "Name" <amount>` |
| `crunch margin <name>` | Execute margin payout | `crunch-cli crunch margin "Name"` |
| `crunch drain <name>` | Drain remaining USDC | `crunch-cli crunch drain "Name"` |
| `crunch get-cruncher` | Get cruncher details | `crunch-cli crunch get-cruncher "CrunchName" <wallet>` |
| `crunch sweep-token-accounts` | Sweep tokens to vault | `crunch-cli crunch sweep-token-accounts "Name"` |
| `crunch check-prize-atas` | Check USDC accounts | `crunch-cli crunch check-prize-atas "Name"` |
| `crunch map-cruncher-addresses` | Map cruncher addresses | `crunch-cli crunch map-cruncher-addresses "CoordName"` |
| `crunch emission-checkpoint-add` | Add emission checkpoint | `crunch-cli crunch emission-checkpoint-add "CoordName" <amount>` |

### Checkpoint Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `crunch checkpoint-create` | Create checkpoint | `crunch-cli crunch checkpoint-create "Name" prizes.json [--dryrun]` |
| `crunch checkpoint-get-current` | Current checkpoint | `crunch-cli crunch checkpoint-get-current "Name"` |
| `crunch checkpoint-get` | Get checkpoint by index | `crunch-cli crunch checkpoint-get "Name" <index>` |

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
crunch-cli crunch get "Synth"
```

### "Show my coordinator on mainnet"
```bash
crunch-cli -u mainnet-beta coordinator get
```

### "List all crunches for slack"
```bash
crunch-cli crunches list
```
Then format output for Slack.

### "What's the current checkpoint for the Chaos competition?"
```bash
crunch-cli crunch checkpoint-get-current "Chaos"
```

## Reference Documentation

For full CLI documentation, see [references/cli-reference.md](references/cli-reference.md).

---

# Competition Quickstarter Skill

This section enables guiding users through the full competition lifecycle: discovering quickstarters, understanding them, building better solutions, evaluating locally, and submitting.

## Overview

Each CrunchDAO competition has **quickstarters** — ready-to-run notebooks and code showing how to participate. The competitions registry is at [`crunchdao/competitions`](https://github.com/crunchdao/competitions) on GitHub. Some competitions also have dedicated repos with full SDKs and evaluators.

The mapping from competition names to repos, packages, and tools lives in [`competitions.json`](competitions.json) next to this file.

## Workspace

All quickstarter work happens in a local workspace directory. Default: `~/.crunch/workspace/<competition>/`.

When starting work on a competition:
1. Create the workspace directory if it doesn't exist.
2. Clone/download the quickstarter code there.
3. All subsequent work (editing, backtesting, submitting) happens from that directory.

If the user specifies a different directory (e.g. _"set up synth in ~/projects/synth"_), use that instead and remember it for the session.

## Step 1: Discover Quickstarters

### Phrase mapping

| User says | Action |
|---|---|
| `show quickstarters for <competition>` | List available quickstarters |
| `what competitions are available` | List all competitions from competitions.json |
| `quickstarters for synth` | List quickstarters for Synth |

### How to list quickstarters

1. Read `competitions.json` to find the registry repo (default: `crunchdao/competitions`).
2. Fetch the quickstarters directory for the competition via GitHub API:
   ```bash
   curl -s "https://api.github.com/repos/crunchdao/competitions/contents/competitions/<name>/quickstarters"
   ```
3. For each subdirectory, fetch its `quickstarter.json`:
   ```bash
   curl -s "https://api.github.com/repos/crunchdao/competitions/contents/competitions/<name>/quickstarters/<qs>/quickstarter.json"
   ```
4. Parse and present to the user:
   - Title
   - Authors
   - Language (Python / R)
   - Usage (Submission / Exploration)
   - Whether it's a notebook

### Example output

```
📚 Quickstarters for Falcon
════════════════════════════════════════
  1. NGBoost              Python  Submission   📓 notebook
     by Alexis GASSMANN
  2. EWMA Variance        Python  Submission   📓 notebook
     by Alexis GASSMANN
  3. Quantile Lin. Reg.   Python  Submission   📓 notebook
     by Alexis GASSMANN
  4. Wealth Distribution  Python  Submission   📓 notebook
     by Alexis GASSMANN
```

## Step 2: Download & Set Up

### Phrase mapping

| User says | Action |
|---|---|
| `download the <title> quickstarter for <competition>` | Download specific quickstarter |
| `set up synth` | Clone the Synth competition repo + quickstarter |
| `get the example tracker` | Download the quickstarter (infer competition from context) |

### How to download

1. Look up the competition in `competitions.json`.
2. Create the workspace directory:
   ```bash
   mkdir -p ~/.crunch/workspace/<competition>
   cd ~/.crunch/workspace/<competition>
   ```
3. If the competition has a dedicated `repo` in `competitions.json`, clone it:
   ```bash
   git clone https://github.com/<repo>.git .
   ```
4. Fetch the `quickstarter.json` for the requested quickstarter to find its `entrypoint`.
5. Download the entrypoint:
   - **If the entrypoint is a URL** (starts with `http`): download or clone the target repo.
   - **If the entrypoint is a relative path**: it's inside the cloned repo already.
6. If the entrypoint is a `.ipynb` notebook, convert it to `.py` for easier reading:
   ```bash
   jupyter nbconvert --to script <notebook>.ipynb
   ```
   Keep both files — the notebook for running, the `.py` for analysis.
7. Install the competition's Python package:
   ```bash
   pip install <package>
   ```
   **Always ask the user for confirmation before installing packages.**
8. If the competition repo has a `SKILL.md`, read it — it contains competition-specific instructions. If it only has a `README.md`, read that instead. This context is critical for all subsequent steps.

### Also fetch reference material

After downloading, check the competition repo for these files and read them if present:
- `SKILL.md` or `README.md` — competition rules, interface, scoring
- `LITERATURE.md` — relevant academic papers and approaches
- `PACKAGES.md` — useful Python packages for the competition
- `scoring/` directory — scoring functions used for evaluation

## Step 3: Explain

### Phrase mapping

| User says | Action |
|---|---|
| `explain this quickstarter` | Walkthrough of the downloaded code |
| `what does the example tracker do` | Explain the quickstarter approach |
| `how does scoring work for synth` | Explain the competition's scoring |
| `what's the interface I need to implement` | Explain the required code structure |

### How to explain

Read the quickstarter code and the competition's SKILL.md/README.md, then produce a structured walkthrough:

1. **Goal** — What the competition asks you to predict / build.
2. **Interface** — What class/function you must implement, its inputs and outputs.
3. **Data flow** — How data comes in and predictions go out (e.g. `tick()` → `PriceStore` → `predict()`).
4. **Approach** — What strategy this specific quickstarter uses (e.g. Gaussian returns model).
5. **Scoring** — How predictions are evaluated (e.g. CRPS, ranked relative to other participants).
6. **Constraints** — Time limits, model count limits, required output format.
7. **Limitations** — Where this quickstarter is naive or overly simple.
8. **Ideas** — Quick pointers to what could be improved (expanded in Step 4).

### Example output

```
📖 Quickstarter Walkthrough: Example Tracker (Synth)
════════════════════════════════════════════════════════════

🎯 Goal
  Predict probability distributions of future crypto price changes
  across multiple assets (BTC, ETH, SOL, ...) and time horizons.

🔌 Interface
  Extend `TrackerBase` and implement one method:
    predict(asset: str, horizon: int, step: int) → list[distribution]

📊 Data Flow
  Framework calls tick(data) → updates self.prices (PriceStore)
  Framework calls predict(asset, horizon, step) → you return densities
  Multi-resolution handled automatically by predict_all()

🧠 Approach
  This quickstarter uses a simple Gaussian model:
  - Computes mean and std of 5-minute historical returns
  - Scales by √(step/300) for different time horizons
  - Returns a single-component Gaussian mixture

📏 Scoring
  CRPS (Continuous Ranked Probability Score) — lower is better.
  7-day rolling average, ranked against all participants.
  Best score = 1.0, worst 5% = 0.0.

⏱️ Constraints
  - All forecasts for a round must complete within 40 seconds
  - Max 2 models per participant

⚠️ Limitations
  - Assumes returns are normally distributed (fat tails ignored)
  - No regime detection (treats volatile and calm periods the same)
  - No cross-asset correlation
  - Single-component density (can't capture bimodal scenarios)
```

## Step 4: Propose New Solutions

### Phrase mapping

| User says | Action |
|---|---|
| `propose improvements` | Suggest concrete improvements to the current approach |
| `what could I do better` | Analyze weaknesses and suggest alternatives |
| `try a different approach` | Generate a new solution from scratch |
| `use NGBoost instead` | Rewrite using a specific technique |
| `add volatility regime detection` | Add a specific feature to the current code |

### How to propose

1. **Analyze the current approach** — Read the active quickstarter code and identify its assumptions and weaknesses.
2. **Cross-reference competition context** — Read the SKILL.md/README.md for scoring details, the LITERATURE.md for research directions, and PACKAGES.md for available tools.
3. **Generate concrete suggestions** with code. Always propose changes as runnable code, not just ideas. Categories of improvement:

   **Model improvements:**
   - Better distributions (mixture densities, Student-t, skew-normal)
   - ML-based approaches (NGBoost, LightGBM quantile regression, DeepAR)
   - Ensemble methods (combine multiple models)
   - Normalizing flows for flexible density estimation

   **Feature engineering:**
   - Volatility regime detection (GARCH, realized volatility)
   - Cross-asset correlation / contagion signals
   - Order book features, volume profiles
   - Time-of-day / day-of-week seasonality

   **Architecture:**
   - Online learning (adapt parameters as new data arrives)
   - Bayesian updating
   - Separate models for different horizons

4. **Present each suggestion** with:
   - What it changes and why
   - Expected impact on scoring
   - Complexity / effort estimate
   - The actual code

5. When the user picks an approach, generate the full solution file in the workspace directory.

### Important rules for proposing solutions

- Always respect the competition's interface (e.g. must extend `TrackerBase` for Synth).
- Always respect constraints (time limits, output format).
- Keep the quickstarter's structure as a starting point — modify, don't rewrite from scratch (unless asked).
- If using a new package, note it and ask before installing.

## Step 5: Backtest / Evaluate Locally

### Phrase mapping

| User says | Action |
|---|---|
| `test my tracker` | Run the local evaluator |
| `backtest on SOL` | Evaluate on a specific asset |
| `compare with the baseline` | Run both and compare scores |
| `how does my model score` | Run evaluation and report results |
| `run crunch test` | Run the CLI-based test |

### How to evaluate

1. Look up the competition in `competitions.json` to find the evaluator.

2. **Python evaluator** (e.g. Synth):
   - The evaluator class and usage pattern are in `competitions.json`.
   - Write a small evaluation script in the workspace:
     ```python
     from crunch_synth.tracker_evaluator import TrackerEvaluator
     from my_tracker import MyTracker

     evaluator = TrackerEvaluator(MyTracker())
     # Feed data, run predictions, report scores
     ```
   - Run it: `python evaluate.py`
   - Report CRPS scores per asset and horizon.

3. **CLI evaluator** (e.g. DataCrunch):
   ```bash
   cd ~/.crunch/workspace/datacrunch
   crunch test
   ```

4. **No evaluator available** — Tell the user there's no local evaluator for this competition and suggest submitting to the platform to see results.

5. **Comparison mode** — When comparing approaches:
   - Run the baseline quickstarter first, record scores.
   - Run the user's modified version, record scores.
   - Present a side-by-side comparison.

### Example output

```
📊 Evaluation Results: MyImprovedTracker vs Baseline
════════════════════════════════════════════════════════════

                     Baseline      Yours        Δ
  BTC (24h CRPS)     0.4231       0.3812      -9.9% ✅
  ETH (24h CRPS)     0.3987       0.3654      -8.3% ✅
  SOL (24h CRPS)     0.5102       0.4890      -4.2% ✅
  BTC (1h CRPS)      0.2103       0.1987      -5.5% ✅
  ────────────────────────────────────────────────
  Overall             0.3856       0.3586      -7.0% ✅

  Your model outperforms the baseline on all assets.
  Biggest improvement: BTC 24h (-9.9%)
```

## Step 6: Submit

### Phrase mapping

| User says | Action |
|---|---|
| `submit my solution` | Submit to the competition |
| `push to datacrunch` | Submit via CLI |
| `deploy my tracker` | Submit to the platform |

### How to submit

1. Look up the competition in `competitions.json` to find the submission method.

2. **CLI submission** (DataCrunch and similar):
   ```bash
   cd ~/.crunch/workspace/<competition>
   crunch push "Submission message"
   ```

3. **Platform submission** (Synth and similar):
   - Direct the user to the platform URL from `competitions.json`.
   - Explain what files need to be uploaded.
   - Provide the link to track results on the leaderboard.

4. **Before submitting, always validate:**
   - The solution implements the required interface.
   - All imports resolve (no missing packages).
   - The solution runs within time constraints (if testable locally).
   - Ask the user for confirmation: _"Ready to submit to <competition>?"_

## Quickstarter Phrase Mapping (Complete)

| User Phrase Pattern | Action |
|---|---|
| `what competitions are available` | List all competitions from competitions.json |
| `show quickstarters for <name>` | Fetch and list quickstarters from registry |
| `download <quickstarter> for <name>` | Download quickstarter to workspace |
| `set up <competition>` | Clone repo, install package, download quickstarter |
| `explain this quickstarter` | Structured code walkthrough |
| `how does <competition> work` | Explain competition rules and scoring |
| `propose improvements` | Analyze and suggest concrete code improvements |
| `try <technique>` | Rewrite using a specific approach |
| `test my solution` | Run local evaluator |
| `backtest on <asset>` | Evaluate on specific asset |
| `compare with baseline` | Side-by-side evaluation |
| `submit my solution` | Push to competition platform |
