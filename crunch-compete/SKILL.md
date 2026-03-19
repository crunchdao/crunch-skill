---
name: crunch-compete
description: Use when working with Crunch competitions - setting up workspaces, exploring quickstarters, developing solutions, running autonomous experiments, or submitting entries. Also use when asked to "run experiments", "improve my model", "start the loop", or "show results".
---

# Cruncher Skill

Guides agents through the full Crunch competition lifecycle: setup, competition briefing, autonomous experimentation, and human-approved submission.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/) for Python environment management:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Credentials

### Submission Token (required for setup & submit)
- Obtained from: `https://hub.crunchdao.com/competitions/<competition>/submit`
- User must be logged in to CrunchDAO Hub
- Passed via `--token <TOKEN>` during `crunch setup`
- After setup, stored in `.crunchdao/` — subsequent commands use it automatically
- **Never hardcode tokens in code or commit them to git**
- If expired: `crunch update-token`

### GitHub API (optional, unauthenticated)
- For browsing quickstarters via `api.github.com` (public repo, 60 req/hr)

## Phase 1: Setup

**Each competition needs its own virtual environment.**

```bash
mkdir -p ~/.crunch/workspace/competitions/<competition>
cd ~/.crunch/workspace/competitions/<competition>
uv venv && source .venv/bin/activate
uv pip install crunch-cli --upgrade --quiet --progress-bar off

# Ask user for token from: https://hub.crunchdao.com/competitions/<competition>/submit
crunch setup <competition> <project-name> --token <TOKEN>
cd <competition>-<project-name>

# Initialize git for experiment tracking
git init && git add -A && git commit -m "initial quickstarter"
git checkout -b experiments/<competition>
```

For competition-specific packages, see [references/competition-setup.md](references/competition-setup.md).

## Phase 2: Competition Briefing

Before any experimentation, assemble a complete `program.md` briefing document. This is the agent's persistent reference for the competition.

### Step 1: Fetch competition context

Pull from three sources. See [references/hub-api-reference.md](references/hub-api-reference.md) for full endpoint details.

**Hub API** (no auth, use curl):
```bash
NAME="<competition>"

# Metadata: format, status, prizes, participant count
curl -s "https://api.hub.crunchdao.com/v1/competitions/$NAME" | python3 -m json.tool

# Targets: what to predict, rank direction
curl -s "https://api.hub.crunchdao.com/v1/competitions/$NAME/targets" | python3 -m json.tool

# Metrics: scoring method (e.g. ROC-AUC, Spearman)
curl -s "https://api.hub.crunchdao.com/v1/competitions/$NAME/metrics" | python3 -m json.tool

# Rounds: deadlines, max submissions/day
curl -s "https://api.hub.crunchdao.com/v1/competitions/$NAME/rounds" | python3 -m json.tool

# Leaderboard: top scores for calibration
curl -s "https://api.hub.crunchdao.com/v2/competitions/$NAME/leaderboards/@default" | python3 -m json.tool
```

**GitHub** (scoring function + runner contract):
```bash
# Scoring function — what you're optimizing
curl -s "https://raw.githubusercontent.com/crunchdao/competitions/master/competitions/$NAME/scoring/scoring.py"

# Runner — how train/infer are called, output contract
curl -s "https://raw.githubusercontent.com/crunchdao/competitions/master/competitions/$NAME/scoring/runner.py"

# List quickstarters
curl -s "https://api.github.com/repos/crunchdao/competitions/contents/competitions/$NAME/quickstarters"
```

**Local data** (after `crunch download`):
```python
import pandas as pd

# Inspect what's in data/
import os
for f in os.listdir("data"):
    print(f)

# Load and summarize — adapt file names per competition
X_train = pd.read_parquet("data/X_train.parquet")
print(f"X_train: {X_train.shape}")
print(X_train.dtypes)
print(X_train.describe())
print(f"NaN: {X_train.isna().sum()[X_train.isna().sum() > 0]}")
print(f"Index: {X_train.index.names}")
```

### Step 2: Generate program.md

Fill in the template from [references/program-template.md](references/program-template.md) with all gathered context. Write it to the workspace root as `program.md`.

Key sections:
- **Goal** — one-sentence objective + metric + direction
- **Format & Interface** — train/infer signatures from runner.py
- **Scoring Function** — full scoring.py inlined
- **Validation Checks** — from scoring.py check() function
- **Data Summary** — from local EDA
- **Leaderboard Context** — top-10 scores for calibration
- **Constraints** — max submissions/day, whitelisted libraries only

### Step 3: Establish baseline

Run the quickstarter as-is and record experiment #0:

```bash
crunch test > run.log 2>&1
```

Parse the output for the local score. Initialize `results.tsv`:

```
commit	score	status	description
a1b2c3d	0.7850	keep	baseline - quickstarter as-is
```

## Phase 3: Autonomous Experimentation

### The Loop

```
LOOP:
  1. Read program.md (interface, scoring, constraints)
  2. Read results.tsv (what's been tried)
  3. Pick experiment idea (informed by scoring function, data, literature, past results)
  4. Modify code (main.py + helpers, requirements.txt if needed)
  5. git commit -m "experiment: <description>"
  6. crunch test > run.log 2>&1
  7. Parse run.log for score — OR detect crash
  8. If crash → tail -n 50 run.log → attempt fix (max 2 retries) → log as crash
  9. Log to results.tsv
  10. If score improved → keep commit (branch advances)
  11. If score worsened → git reset --hard <last-good-commit>
  12. Check stopping condition → if met, pause and present results
  13. → back to 1
```

### Experiment Strategy

Follow this progression, not random search:

1. **Baseline** — run quickstarter as-is (experiment #0)
2. **Quick wins** — hyperparameter tuning, simple model swaps
3. **Feature engineering** — informed by EDA and domain knowledge
4. **Model architecture** — ensembles, stacking, different algorithms
5. **Advanced techniques** — from literature, leaderboard-calibrated ideas
6. **Refinement** — combine best ideas from previous experiments

Each experiment builds on the current best, not from scratch.

### What the Agent Can Modify

**Fair game:**
- `main.py` — model logic, features, hyperparameters
- Helper modules — new `.py` files for utilities, pipelines
- `requirements.txt` — add whitelisted packages only
- `resources/` — saved models, preprocessed data

**Do NOT modify:**
- `train()` / `infer()` function signatures (the runner calls these)
- Output format (file names, dtypes, index — defined in program.md)
- `.crunchdao/` directory (project config, token)

### Scoring Extraction

Primary: parse `crunch test` stdout for the score.

Fallback: run the scoring function directly against output:
```python
# Example for ROC-AUC competitions
import pandas as pd
import sklearn.metrics

prediction = pd.read_parquet("prediction/prediction.parquet")
y_test = pd.read_parquet("data/y_test.reduced.parquet")["<target_column>"]
score = sklearn.metrics.roc_auc_score(y_test, prediction)
```

The exact scoring function is inlined in `program.md`.

### results.tsv Format

Tab-separated, NOT comma-separated. Header + one row per experiment:

```
commit	score	status	description
```

| Column | Type | Description |
|--------|------|-------------|
| commit | string | Git commit hash (7 chars) |
| score | float | Primary metric value. 0.0000 for crashes |
| status | enum | `keep`, `discard`, or `crash` |
| description | string | Short text — what this experiment tried |

**Do not commit results.tsv to git** — it stays untracked as a local log.

### Stopping Conditions

Pause and present results when ANY of:
- **10 experiments completed** (configurable — user can say "do 20 more")
- **3 consecutive experiments with no improvement** (plateau)
- **Human interrupts**

### Results Presentation

When paused, present a summary:

```
Experiment Results: <competition>
  Baseline:  78.50%  (experiment #0)
  Best:      89.20%  (experiment #7)
  Top LB:    92.01%  (rank 1 on leaderboard)

  #   Score    Status   Description
  0   78.50%   keep     baseline
  1   82.30%   keep     gradient boosting
  2   81.90%   discard  random forest (worse)
  ...
  7   89.20%   keep     ensemble: LightGBM + XGBoost

  Current best: experiment #7 (commit abc1234)

  Options:
  1. Submit best → crunch push -m "description"
  2. Keep experimenting (another 10 rounds)
  3. Try a specific idea
```

### Submission (Human Approval Required)

**Never submit without asking the user.** When they approve:

```bash
crunch test          # Always re-test before submitting
crunch push -m "Description of the approach"
```

## Phrase Mapping

| User says | Action |
|-----------|--------|
| `what competitions are available` | `crunch list` |
| `set up <competition>` | Phase 1: Full workspace setup |
| `brief me on <competition>` | Phase 2: Generate program.md |
| `start experiments` / `run the loop` | Phase 3: Begin experiment loop |
| `show results` | Present results.tsv summary |
| `keep going` / `do 10 more` | Continue experiment loop |
| `submit the best` / `submit #N` | `crunch push` (after confirmation) |
| `test my solution` | `crunch test` |
| `explain the scoring` | Read scoring function from program.md |
| `what's the leaderboard look like` | Fetch leaderboard from Hub API |

## Important Rules

- Entrypoint must be `main.py`
- Model files go in `resources/`
- Respect the interface contract (train/infer signatures from runner.py)
- Only install whitelisted packages
- Ask before submitting — `crunch push` always requires human approval
- Never commit tokens or results.tsv to git

## Reference

- CLI commands: [references/cli-reference.md](references/cli-reference.md)
- Setup examples: [references/competition-setup.md](references/competition-setup.md)
- Hub API endpoints: [references/hub-api-reference.md](references/hub-api-reference.md)
- Program.md template: [references/program-template.md](references/program-template.md)
