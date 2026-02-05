# Proposal: Quickstarter Skill Extension

## What this is about

Each CrunchDAO competition (crunch) has **quickstarters** — ready-to-run notebooks and code that show participants how to get started. Today a human has to find the right repo, clone it, read through the code, understand the scoring, and figure out how to improve. All of this can be guided by an AI skill.

This proposal describes how to extend the crunch-skill so the AI can:

1. **Download** quickstarters for any competition
2. **Explain** what a quickstarter does (code walkthrough)
3. **Propose** new solution approaches
4. **Backtest** solutions locally before submitting
5. **Submit** solutions to competitions

---

## How the ecosystem is structured

### Competitions registry

The [`crunchdao/competitions`](https://github.com/crunchdao/competitions) repo is the central registry:

```
competitions/
├── synth/
│   ├── assets/
│   └── quickstarters/
│       └── example-tracker/
│           └── quickstarter.json          ← points to entrypoint
├── datacrunch/
│   ├── README.md                          ← competition description
│   ├── quickstarters/
│   │   └── quickstarter/
│   │       └── quickstarter.json
│   └── scoring/
├── falcon/
│   ├── README.md
│   └── quickstarters/
│       ├── ngboost/
│       ├── ewma-variance/
│       ├── quantile-linear-regression/
│       └── wealth-distribution/
└── ...
```

### quickstarter.json schema

Each quickstarter is described by a `quickstarter.json`:

```json
{
  "title": "NGBoost",
  "authors": [{ "name": "Alexis GASSMANN", "link": "https://github.com/Tarandro" }],
  "language": "PYTHON",           // PYTHON or R
  "usage": "SUBMISSION",          // SUBMISSION or EXPLORATION
  "notebook": true,               // true = .ipynb, false = .py with "files" array
  "entrypoint": "https://github.com/microprediction/birdgame/blob/main/birdgame/examples/quickstarters/ngboost.ipynb"
}
```

Key: the `entrypoint` can be a **local file** (relative path within the competitions repo) or a **URL** pointing to an external repo.

### Competition-specific repos

Some competitions have dedicated repos with full frameworks:

| Competition | Repo | Package |
|---|---|---|
| Synth | [`crunchdao/crunch-synth`](https://github.com/crunchdao/crunch-synth) | `pip install crunch-synth` |
| Falcon | [`microprediction/birdgame`](https://github.com/microprediction/birdgame) | (external) |
| DataCrunch | quickstarter in competitions repo | `pip install crunch-cli` (the Python SDK, not the Solana CLI) |

These repos contain:
- The SDK / framework (e.g. `TrackerBase` for Synth)
- Example trackers / models
- Local evaluation tools (e.g. `TrackerEvaluator`)
- `SKILL.md` or `README.md` explaining how to participate

### Competition-specific SKILL.md files

Each competition repo can include a `SKILL.md` that teaches the AI how to participate in *that* competition. For example, `crunch-synth` could have a SKILL.md that explains:
- What a tracker is
- The `predict()` interface
- How scoring works (CRPS)
- How to evaluate locally with `TrackerEvaluator`
- How to submit

This means the quickstarter skill becomes a **skill compositor** — it pulls in the competition-specific skill and combines it with the quickstarter code to give contextual guidance.

---

## Proposed workflow

### 1. Discover & download

```
User: "show me quickstarters for Synth"
```

The skill should:

1. Fetch the competitions registry (GitHub API or local clone of `crunchdao/competitions`)
2. List quickstarters for the requested competition
3. For each, show title, authors, language, and usage type
4. On request, download/clone the entrypoint code into a working directory

**Implementation:**
- Clone or sparse-checkout `crunchdao/competitions` once into a local cache
- Parse `quickstarter.json` files to build the listing
- For external entrypoints (URLs), clone the target repo
- For notebook entrypoints, convert `.ipynb` → `.py` for easier analysis

### 2. Explain

```
User: "explain the example tracker for Synth"
```

The skill should:

1. Read the downloaded quickstarter code
2. Read the competition's SKILL.md / README.md for context (scoring, interface, constraints)
3. Produce a structured walkthrough:
   - **Goal** — what the competition asks for
   - **Approach** — what strategy this quickstarter uses
   - **Data flow** — how data comes in (e.g. `tick()` → `PriceStore`) and predictions go out
   - **Model** — what statistical / ML model is used
   - **Limitations** — where this quickstarter is naive or could be improved
   - **Scoring** — how the output maps to the scoring function (e.g. CRPS)

### 3. Propose new solutions

```
User: "propose improvements to the Synth example tracker"
```

The skill should:

1. Analyze the current quickstarter's approach
2. Cross-reference the competition's SKILL.md for scoring details and constraints
3. Read any `LITERATURE.md` or `PACKAGES.md` provided in the competition repo
4. Suggest concrete improvements with code, e.g.:
   - Better distributional models (mixture densities, copulas)
   - Feature engineering (volatility regimes, cross-asset correlation)
   - Ensemble approaches
   - Alternative ML frameworks (NGBoost, DeepAR, Normalizing Flows)
5. Generate a new tracker/model file with the proposed changes

### 4. Backtest / evaluate locally

```
User: "backtest my tracker on SOL for the last 7 days"
```

The skill should:

1. Identify the local evaluation tool for the competition:
   - Synth → `TrackerEvaluator` from `crunch-synth`
   - DataCrunch → `crunch test` from the Python `crunch-cli` SDK
2. Run the evaluation and report results:
   - CRPS scores (overall, per asset, per horizon)
   - Comparison against the quickstarter baseline
   - Score trajectory over time
3. If the competition repo has a `scoring/` directory, use those scoring functions

### 5. Submit

```
User: "submit my tracker to the Synth competition"
```

The skill should:

1. Validate the solution meets competition requirements (correct interface, runs within time limits)
2. Use the competition's submission mechanism:
   - Synth → deploy tracker via the Synth platform
   - DataCrunch → `crunch push` via the Python SDK
3. Confirm submission and provide a link to the leaderboard

---

## What needs to happen

### In this repo (crunch-skill)

Add a new section to `SKILL.md` (or a separate `SKILL-quickstarters.md`) that teaches the AI:

- How to navigate the competitions registry
- How to download and read quickstarters  
- The mapping from competition name → repo → SDK → evaluation tool
- How to read a competition's SKILL.md for context
- The propose/evaluate/submit loop

### In competition repos (e.g. crunch-synth)

Each competition repo should add a `SKILL.md` that explains:

- The competition format and rules
- The code interface participants must implement
- How scoring works
- How to evaluate locally
- How to submit
- Common pitfalls and tips

The `crunch-synth` README already contains all of this — it just needs to be moved/copied to `SKILL.md` following a consistent format.

### Competition registry mapping

The skill needs a mapping from crunch names to their repos/resources. This could live in a `competitions.json` file:

```json
{
  "competitions": {
    "synth": {
      "registry": "crunchdao/competitions",
      "repo": "crunchdao/crunch-synth",
      "package": "crunch-synth",
      "hub": "https://hub.crunchdao.com/competitions/synth",
      "evaluator": "crunch_synth.tracker_evaluator.TrackerEvaluator"
    },
    "datacrunch": {
      "registry": "crunchdao/competitions",
      "repo": null,
      "package": "crunch-cli",
      "hub": "https://hub.crunchdao.com/competitions/datacrunch",
      "evaluator": "crunch test"
    },
    "falcon": {
      "registry": "crunchdao/competitions",
      "repo": "microprediction/birdgame",
      "package": "birdgame",
      "hub": "https://hub.crunchdao.com/competitions/falcon",
      "evaluator": null
    }
  }
}
```

---

## Open questions

1. **Where should quickstarter code be cloned to?** A `~/.crunch/quickstarters/` cache? A workspace directory the user specifies?

2. **Should the AI auto-install Python packages?** Running `pip install crunch-synth` in user environments has risk. Maybe suggest it and wait for confirmation.

3. **Notebook handling** — Most quickstarters are `.ipynb`. Should the skill convert to `.py` for analysis, or work with the notebook format directly?

4. **Competition-specific SKILL.md adoption** — How many competition repos already have (or will add) a SKILL.md? The `crunch-synth` README is essentially a SKILL.md already. Should we formalize a standard?

5. **Submission credentials** — Submitting to competitions likely requires authentication. How should the skill handle API keys / tokens?

6. **Live data for backtesting** — Some evaluators (like `TrackerEvaluator`) need real-time price data. Should the skill handle data fetching, or assume the user has it?
