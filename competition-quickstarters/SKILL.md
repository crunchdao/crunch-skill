---
name: competition-quickstarters
description: Helps participants discover, understand, improve, backtest, and submit solutions for CrunchDAO competitions. Uses the crunch CLI (pip install crunch-cli) for workspace setup, data download, local testing, notebook conversion, and submission. Guides users through quickstarter code, proposes improvements, and runs evaluations.
---

# Competition Quickstarter Skill

This skill guides users through the full CrunchDAO competition lifecycle: setting up a workspace, discovering and understanding quickstarters, building better solutions, testing locally, and submitting.

## Setup

### uv (package manager)

This skill uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python environment management. Each competition gets its own isolated virtual environment.

Install uv if not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Per-competition environment

**Every competition must have its own virtual environment.** Competitions can have conflicting dependencies, and isolation prevents breakage.

When setting up a competition workspace:

```bash
mkdir -p ~/.crunch/workspace/competitions/<competition>
cd ~/.crunch/workspace/competitions/<competition>
uv venv
source .venv/bin/activate
```

### Clone tokens

**Each competition has its own unique clone token.** Tokens are per-user, per-competition. When a user asks to set up a competition, direct them to the submit page to get their token:

```
https://hub.crunchdao.com/competitions/<competition>/submit
```

Store tokens in `~/.crunch/.tokens` for reuse:

```bash
# ~/.crunch/.tokens
SYNTH_TOKEN=VqbyFbiETucdJjsV0CHKpj4d
FALCON_TOKEN=wihApI77M4S6xHFZi0UFieoH
DATACRUNCH_TOKEN=...
```

When the user provides a token, store it in this file for future use.

### Full setup flow

The complete setup for any competition follows this pattern:

```bash
# 1. Create workspace and venv
mkdir -p ~/.crunch/workspace/competitions/<competition>
cd ~/.crunch/workspace/competitions/<competition>
uv venv
source .venv/bin/activate

# 2. Install crunch CLI and Jupyter
uv pip install crunch-cli jupyter ipykernel --upgrade --quiet --progress-bar off

# 3. Register Jupyter kernel for this competition
python -m ipykernel install --user --name <competition> --display-name "CrunchDAO - <competition>"

# 4. Set up the competition project (token from hub submit page)
crunch setup <competition> <project-name> --token <TOKEN>

# 5. Enter the project directory
cd <competition>-<project-name>
```

After step 4, the `crunch setup` command will:
- Create a directory `<competition>-<project-name>/`
- Prompt the user to select a quickstarter (interactive)
- Download the competition data
- Set up the workspace with `main.py` as the entrypoint

### Competition-specific packages

Some competitions have their own SDK. Install into the competition's venv as needed (in step 2):

```bash
uv pip install crunch-synth --upgrade --quiet --progress-bar off   # Synth competition
uv pip install birdgame --upgrade --quiet --progress-bar off       # Falcon competition
```

Look up required packages for the competition in its repo's `README.md` or `SKILL.md`.

### Example: full setup for Synth

```bash
mkdir -p ~/.crunch/workspace/competitions/synth
cd ~/.crunch/workspace/competitions/synth
uv venv
source .venv/bin/activate
uv pip install crunch-cli crunch-synth jupyter ipykernel --upgrade --quiet --progress-bar off
python -m ipykernel install --user --name synth --display-name "CrunchDAO - Synth"
# Get token from: https://hub.crunchdao.com/competitions/synth/submit
crunch setup synth my-project --token <TOKEN>
cd synth-my-project
```

### Example: full setup for Falcon

```bash
mkdir -p ~/.crunch/workspace/competitions/falcon
cd ~/.crunch/workspace/competitions/falcon
uv venv
source .venv/bin/activate
uv pip install crunch-cli birdgame jupyter ipykernel --upgrade --quiet --progress-bar off
python -m ipykernel install --user --name falcon --display-name "CrunchDAO - Falcon"
# Get token from: https://hub.crunchdao.com/competitions/falcon/submit
crunch setup falcon my-project --token <TOKEN>
cd falcon-my-project
```

## Overview

Each CrunchDAO competition has **quickstarters** — ready-to-run notebooks and code showing how to participate. The `crunch` CLI handles workspace setup, data download, quickstarter selection, local testing, and submission.

## Step 1: Discover Competitions & Quickstarters

### Phrase mapping

| User says | Action |
|---|---|
| `what competitions are available` | Run `crunch list` |
| `list competitions` | Run `crunch list` |
| `show quickstarters for <competition>` | List available quickstarters |
| `quickstarters for synth` | List quickstarters for Synth |

### How to list competitions

Use the `crunch list` command to get all available competitions from the CrunchDAO platform:

```bash
crunch list
```

Example output:
```
  adialab (TIMESERIES)
  datacrunch (TIMESERIES)
  synth (TIMESERIES)
  falcon (DAG)
```

The competition hub page is always at `https://hub.crunchdao.com/competitions/<name>`.

### How to list quickstarters

Fetch from the competitions registry via GitHub API:

```bash
# List quickstarter directories
curl -s "https://api.github.com/repos/crunchdao/competitions/contents/competitions/<name>/quickstarters"

# Get details for each
curl -s "https://api.github.com/repos/crunchdao/competitions/contents/competitions/<name>/quickstarters/<qs>/quickstarter.json"
```

The `quickstarter.json` contains:
- `title` — display name
- `authors` — list of `{name, link}`
- `language` — `PYTHON` or `R`
- `usage` — `SUBMISSION` (can be submitted) or `EXPLORATION` (for learning)
- `notebook` — `true` if `.ipynb`
- `entrypoint` — file path or URL to the code

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
```

## Step 2: Set Up Workspace

### Phrase mapping

| User says | Action |
|---|---|
| `set up <competition>` | Full workspace setup with crunch CLI |
| `set up datacrunch` | Set up DataCrunch workspace |
| `set up synth notebook` | Set up Synth in notebook mode |
| `download the data for <competition>` | Download competition data |
| `get the <name> quickstarter` | Deploy a specific quickstarter |

### How to set up — using `crunch setup`

First, ensure the competition's venv exists and is active (see Setup section above).

The user needs a **clone token**. Each competition has its own token. If not provided, direct them to:
```
https://hub.crunchdao.com/competitions/<competition>/submit
```

**Standard setup:**

```bash
cd ~/.crunch/workspace/competitions/<competition>
source .venv/bin/activate
crunch setup <competition> <project-name> --token <TOKEN>
cd <competition>-<project-name>
```

**Pre-select a quickstarter:**

```bash
crunch setup <competition> <project-name> --token <TOKEN> --quickstarter-name "NGBoost"
```

**Notebook setup** (for Jupyter workflows):

```bash
crunch setup <competition> <project-name> --token <TOKEN> --notebook
```

In notebook mode:
- Workspace is set up in the current directory (`.`)
- No quickstarter selection (notebooks use `crunch.load_notebook()`)
- Force mode is implicit

**Skip data download** (faster setup):

```bash
crunch setup <competition> <project-name> --token <TOKEN> --no-data
```

### Download data separately

```bash
cd <workspace-directory>
crunch download
crunch download --force              # re-download
crunch download --size-variant small  # smaller dataset
```

### Deploy a quickstarter into an existing workspace

```bash
cd <workspace-directory>
crunch quickstarter                           # interactive selection
crunch quickstarter --name "NGBoost"          # specific quickstarter
crunch quickstarter --show-notebook           # include notebook quickstarters
crunch quickstarter --overwrite               # overwrite existing files
```

### Convert notebook to Python script

If working with a notebook quickstarter and need a `.py` file:

```bash
crunch convert notebook.ipynb main.py
crunch convert notebook.ipynb main.py --override       # overwrite existing
crunch convert notebook.ipynb main.py --requirements    # also export requirements.txt
crunch convert notebook.ipynb main.py --embedded-files  # also export embedded files
```

### For competitions with dedicated repos (e.g. Synth)

Some competitions have their own SDK repo (e.g. `crunch-synth` for Synth):

```bash
# Clone the competition repo into the workspace
git clone https://github.com/crunchdao/crunch-synth.git
cd crunch-synth

# Install the SDK into the competition's venv
uv pip install crunch-synth --upgrade
```

### Also fetch reference material

After setup, check the competition repo for these files and read them if present:
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
| `how does scoring work for <competition>` | Explain the competition's scoring |
| `what's the interface I need to implement` | Explain the required code structure |

### How to explain

Read the quickstarter code (the `main.py` or notebook in the workspace) and the competition's SKILL.md/README.md, then produce a structured walkthrough:

1. **Goal** — What the competition asks you to predict / build.
2. **Interface** — What class/function you must implement, its inputs and outputs.
3. **Data flow** — How data comes in and predictions go out.
4. **Approach** — What strategy this specific quickstarter uses.
5. **Scoring** — How predictions are evaluated.
6. **Constraints** — Time limits, model count limits, required output format.
7. **Limitations** — Where this quickstarter is naive or overly simple.
8. **Ideas** — Quick pointers to what could be improved (expanded in Step 4).

### Notebook usage pattern

For competitions using the `crunch` SDK in notebooks:

```python
import crunch
crunch = crunch.load_notebook()

# Load competition data
X_train, y_train, X_test = crunch.load_data()

# ... build and train model ...

# Test locally
crunch.test()
```

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
  Simple Gaussian model — computes mean/std of 5-min returns,
  scales by √(step/300) for different time horizons.

📏 Scoring
  CRPS (Continuous Ranked Probability Score) — lower is better.
  7-day rolling average, ranked against all participants.

⏱️ Constraints
  All forecasts for a round must complete within 40 seconds.
  Max 2 models per participant.

⚠️ Limitations
  - Assumes normal distribution (fat tails ignored)
  - No regime detection
  - No cross-asset correlation
  - Single-component density
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

1. **Analyze the current approach** — Read the `main.py` or notebook in the workspace and identify its assumptions and weaknesses.
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

5. When the user picks an approach, generate the full solution file in the workspace directory as `main.py` (the default entrypoint the `crunch` CLI expects).

### Important rules for proposing solutions

- Always respect the competition's interface.
- Always respect constraints (time limits, output format).
- Keep the quickstarter's structure as a starting point — modify, don't rewrite from scratch (unless asked).
- The entrypoint must be `main.py` (default for `crunch push` and `crunch test`).
- Model files go in the `resources/` directory (default model directory for `crunch`).
- If using a new package, note it and ask before installing.

## Step 5: Test Locally

### Phrase mapping

| User says | Action |
|---|---|
| `test my solution` | Run `crunch test` |
| `test my tracker` | Run the local evaluator |
| `backtest on SOL` | Evaluate on a specific asset |
| `compare with the baseline` | Run both and compare scores |
| `how does my model score` | Run evaluation and report results |
| `run crunch test` | Run `crunch test` directly |

### How to test — using `crunch test`

The primary way to test locally for most competitions:

```bash
cd <workspace-directory>
crunch test
```

**`crunch test` options:**

```bash
crunch test --main-file main.py            # specify entrypoint (default: main.py)
crunch test --model-directory resources     # model dir (default: resources)
crunch test --round-number @current        # which round's data to use
crunch test --gpu                          # enable GPU flag
crunch test --no-checks                    # skip prediction validation
crunch test --no-determinism-check         # skip determinism check
crunch test --train-frequency 1            # train interval
crunch test --no-force-first-train         # don't force train on first loop
```

### For Synth (Python evaluator)

Synth has its own evaluator in addition to `crunch test`:

```python
from crunch_synth.tracker_evaluator import TrackerEvaluator
from my_tracker import MyTracker

evaluator = TrackerEvaluator(MyTracker())
evaluator.tick({"SOL": [(ts, price)]})
predictions = evaluator.predict("SOL", horizon=86400, steps=[300, 3600, 21600, 86400])
print(f"CRPS: {evaluator.overall_score('SOL'):.4f}")
```

### For notebooks

In a Jupyter notebook using the crunch SDK:

```python
import crunch
crunch_tools = crunch.load_notebook()

X_train, y_train, X_test = crunch_tools.load_data()
# ... your model code ...
crunch_tools.test()
```

### Comparison mode

When comparing approaches:
1. Run `crunch test` with the baseline quickstarter, record output.
2. Swap in the user's modified `main.py`, run `crunch test` again.
3. Present a side-by-side comparison.

### Example output

```
📊 Evaluation Results: MyImprovedTracker vs Baseline
════════════════════════════════════════════════════════════

                     Baseline      Yours        Δ
  BTC (24h CRPS)     0.4231       0.3812      -9.9% ✅
  ETH (24h CRPS)     0.3987       0.3654      -8.3% ✅
  SOL (24h CRPS)     0.5102       0.4890      -4.2% ✅
  ────────────────────────────────────────────────
  Overall             0.3856       0.3586      -7.0% ✅
```

## Step 6: Submit

### Phrase mapping

| User says | Action |
|---|---|
| `submit my solution` | Run `crunch push` |
| `push my code` | Run `crunch push` |
| `deploy my tracker` | Submit to the platform |

### How to submit — using `crunch push`

```bash
cd <workspace-directory>
crunch push -m "Description of changes"
```

**`crunch push` options:**

```bash
crunch push -m "Added mixture density model"           # with message
crunch push --main-file main.py                        # specify entrypoint
crunch push --model-directory resources                 # model dir
crunch push --dry                                      # dry run (prepare but don't submit)
crunch push --no-pip-freeze                            # skip pip freeze
```

The `crunch push` command:
1. Packages your `main.py` and `resources/` directory
2. Converts `.ipynb` to `.py` automatically if `main.py` is missing but a notebook exists
3. Uploads to the CrunchDAO platform
4. Creates a new submission entry

### For platform-only competitions (e.g. Synth)

Some competitions submit through the platform directly:
- Direct the user to `https://hub.crunchdao.com/competitions/<name>`
- Explain what files need to be uploaded
- Provide the leaderboard link

### Before submitting, always:

1. Run `crunch test` to verify the solution works locally.
2. Check that `main.py` exists (or a notebook that can be converted).
3. Check that the `resources/` directory contains any required model files.
4. Ask the user for confirmation: _"Ready to submit?"_

## Detecting the environment

The crunch SDK lets you detect whether code is running locally or in the competition runner:

```python
import crunch

if crunch.is_inside_runner:
    print("running inside the runner")
else:
    print("running locally")
    # enable debug logging, etc.
```

This is useful for adding debug output or loading local-only dependencies.

## `crunch` CLI Command Reference

| Command | Description |
|---|---|
| `crunch setup <competition> <project> --token <TOKEN>` | Set up workspace with quickstarter |
| `crunch setup <competition> <project> --token <TOKEN> --notebook` | Set up notebook workspace |
| `crunch setup-notebook <competition> <TOKEN>` | Alternative notebook setup |
| `crunch quickstarter` | Deploy a quickstarter into existing workspace |
| `crunch quickstarter --name "Name"` | Deploy a specific quickstarter |
| `crunch download` | Download competition data |
| `crunch download --force` | Re-download data |
| `crunch download --size-variant small` | Download smaller dataset |
| `crunch test` | Test solution locally |
| `crunch test --gpu` | Test with GPU flag |
| `crunch push -m "message"` | Submit solution |
| `crunch push --dry` | Dry run (no actual submission) |
| `crunch convert notebook.ipynb main.py` | Convert notebook to Python |
| `crunch update-token` | Update the project clone token |
| `crunch list` | List all available competitions |
| `crunch ping` | Check if the CrunchDAO server is online |

## Quickstarter Phrase Mapping (Complete)

| User Phrase Pattern | Action |
|---|---|
| `what competitions are available` | Run `crunch list` |
| `show quickstarters for <name>` | Fetch and list quickstarters from registry |
| `set up <competition>` | Run `crunch setup` with token + quickstarter |
| `set up <competition> notebook` | Run `crunch setup --notebook` |
| `download the data` | Run `crunch download` |
| `get the <name> quickstarter` | Run `crunch quickstarter --name` |
| `explain this quickstarter` | Structured code walkthrough |
| `how does <competition> work` | Explain competition rules and scoring |
| `propose improvements` | Analyze and suggest concrete code improvements |
| `try <technique>` | Rewrite using a specific approach |
| `test my solution` | Run `crunch test` |
| `backtest on <asset>` | Run evaluator on specific asset |
| `compare with baseline` | Side-by-side evaluation |
| `submit my solution` | Run `crunch push` |
| `push my code` | Run `crunch push` |
