---
name: competition-quickstarters
description: Helps participants discover, understand, improve, backtest, and submit solutions for CrunchDAO competitions. Downloads quickstarters, explains the code and scoring, proposes improvements, runs local evaluators, and handles submission.
---

# Competition Quickstarter Skill

This skill guides users through the full CrunchDAO competition lifecycle: discovering quickstarters, understanding them, building better solutions, evaluating locally, and submitting.

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
