---
name: crunch-compete
description: Use when working with Crunch competitions - setting up workspaces, exploring quickstarters, testing solutions locally, or submitting entries.
---

# Cruncher Skill

Guides users through Crunch competition lifecycle: setup, quickstarter discovery, solution development, local testing, and submission.

## Prerequisites
- Python 3.9+ with `venv` module (included in standard Python)
- `pip` for package installation

## Package Installation

This skill installs Python packages from [PyPI](https://pypi.org) into isolated virtual environments:

| Package | Source | Purpose |
|---------|--------|---------|
| `crunch-cli` | [PyPI](https://pypi.org/project/crunch-cli/) | CrunchDAO competition CLI (setup, test, submit) |
| `jupyter` | [PyPI](https://pypi.org/project/jupyter/) | Notebook support (optional) |
| `ipykernel` | [PyPI](https://pypi.org/project/ipykernel/) | Jupyter kernel registration (optional) |
| Competition SDKs (e.g. `crunch-synth`, `birdgame`) | PyPI | Competition-specific libraries (varies) |

**Agent rules for package installation:**
- **Always use a virtual environment** — never install into system Python
- **Only install known packages** listed above or referenced in competition docs (PACKAGES.md)
- **Ask the user before installing** any package not listed here
- **All packages are from PyPI** — no custom URLs, no `--index-url` overrides, no `.whl` files from unknown sources


## Credentials

### Submission Token (required for setup & submit)
- **How to get:** User logs into [CrunchDAO Hub](https://hub.crunchdao.com), navigates to the competition's submit page (`/competitions/<competition>/submit`), and copies their token
- **How it's used:** Passed once via `--token <TOKEN>` during `crunch setup`
- **Persistence:** After setup, the CLI stores the token in the project's `.crunch/` config directory. All subsequent commands (`crunch test`, `crunch push`, `crunch download`) authenticate automatically — no need to pass the token again
- **If token expires:** Run `crunch update-token` inside the project directory to refresh it

**Agent rules for tokens:**
- **Always ask the user** to provide the token — never assume, guess, or reuse tokens from other projects
- **Never write tokens** into source files, scripts, notebooks, or any committed file
- **Never log or echo tokens** in shell output (use `--token <TOKEN>` placeholder in examples shown to user)
- Tokens are user-specific and project-scoped — each `crunch setup` call requires the user to supply one

### GitHub API (optional, unauthenticated)
- Used only for browsing quickstarter listings via `api.github.com` (public repo, no auth needed)
- Rate-limited to 60 requests/hour per IP; sufficient for normal use

## Network Access

| Operation | Requires network | Endpoint |
|-----------|-----------------|----------|
| `crunch setup` | Yes | hub.crunchdao.com |
| `crunch push` | Yes | hub.crunchdao.com |
| `crunch download` | Yes | hub.crunchdao.com |
| `crunch test` | **No** | Local only |
| `crunch list` | Yes | hub.crunchdao.com |
| `pip install` | Yes | pypi.org |
| Quickstarter browsing | Yes | api.github.com |

## Quick Setup

**Each competition needs its own virtual environment** (dependencies can conflict).

```bash
mkdir -p ~/.crunch/workspace/competitions/<competition>
cd ~/.crunch/workspace/competitions/<competition>
python -m venv .venv && source .venv/bin/activate 
pip install crunch-cli jupyter ipykernel --upgrade --quiet --progress-bar=off
python -m ipykernel install --user --name <competition> --display-name "Crunch - <competition>"

# Get token from: https://hub.crunchdao.com/competitions/<competition>/submit
crunch setup <competition> <project-name> --token <TOKEN>
cd <competition>-<project-name>
```

For competition-specific packages and full examples, see [references/competition-setup.md](references/competition-setup.md).

## Session Continuation State (Critical)

Use this **strict source priority** for current status:
1. `<competition>-<project>/results.tsv` (authoritative experiment ledger)
2. git state in `<competition>-<project>/` (branch, HEAD, tag, clean/dirty)
3. `~/.../<competition>/SESSION-SUMMARY.md` (compact carry-over summary + next ideas)

Fallbacks when files are missing:
- If `results.tsv` does not exist yet, treat as fresh run and state "no tracked experiments yet".
- If no `exp-vNNN` tag exists on HEAD, show `tag=none`.
- If `SESSION-SUMMARY.md` is missing, proceed with `results.tsv` + git only.

`history.md` is optional narrative context and can be stale.
Never treat `history.md` as single source of truth for latest best score/version.

**At the START of every session:**
1. Read `results.tsv` + git state first
2. Read `SESSION-SUMMARY.md` for quick context and next ideas
3. Use `history.md` only for long-term background if needed

**At the END of every session (or after significant progress):**
1. Ensure `results.tsv` is up to date
2. Update `SESSION-SUMMARY.md` with best version/score + next 2-3 experiments
3. Optionally append context to `history.md`

### Optional history.md Structure

```markdown
# <competition> — Experiment History

**Project:** <project-name>
**Dashboard:** <hub-url>
**Workspace:** <path>
**Last updated:** <date>

## Competition Summary
<one-paragraph: goal, metric, data format, constraints>

## Current Best
<version, score, whether submitted, what to do next>

## Experiment Log
| Ver | Features | CV AUC | Test AUC | Sub# | Description |
|-----|----------|--------|----------|------|-------------|
| ... | ...      | ...    | ...      | ...  | ...         |

## What Works (Key Learnings)
<numbered list of validated insights from experiments>

## What Hasn't Been Tried Yet
### High Priority
### Medium Priority
### Lower Priority

## Top Solutions Context
<leaderboard scores and approaches from prior competitions if available>

## Architecture (current)
<description of current solution pipeline>
```

This file is **background narrative only**. The authoritative current state is `results.tsv` + git.

### Fast Continuation Response (Required)

For prompts like "continue", "what's the latest", "keep going", first reply with this exact structure:

```text
Latest Snapshot — <competition>
- Best: <vNNN> (<tag>, <commit>) — <score>
- Branch/HEAD: <branch>, <commit> (<clean/dirty>)
- Recent experiments:
  - <vNNN> | <score> | <keep/discard/crash> | <short description>
  - <vNNN> | <score> | <keep/discard/crash> | <short description>
  - <vNNN> | <score> | <keep/discard/crash> | <short description>

Suggested Next Approaches
1) <title>
   - Hypothesis: <1 sentence>
   - Expected upside: <range>
   - Cost/Risk: <runtime + complexity + overfit risk>

2) <title>
   - Hypothesis: <1 sentence>
   - Expected upside: <range>
   - Cost/Risk: <runtime + complexity + overfit risk>

3) <title>
   - Hypothesis: <1 sentence>
   - Expected upside: <range>
   - Cost/Risk: <runtime + complexity + overfit risk>

Choose: 1, 2, 3, or "run all".
```

For this first continuation response:
- use lightweight local reads + git only
- do NOT run `crunch test`
- do NOT make live submission-limit claims unless re-validated now
- if submission-limit status is unknown, explicitly say "unknown (not checked live)"

## Core Workflow

### 1. Discover
```bash
crunch list                    # List competitions
```

### 2. Read Current State
- Read `<competition>-<project>/results.tsv`
- Check git branch/HEAD/tag/status in `<competition>-<project>/`
- Read `../SESSION-SUMMARY.md`
- Optionally read `../history.md` for context only

### 3. Explain
Read the quickstarter code (`main.py` or notebook) and competition's SKILL.md/README.md. Provide walkthrough covering: Goal, Interface, Data flow, Approach, Scoring, Constraints, Limitations, Improvement ideas.

### 4. Propose Improvements
Analyze current approach, cross-reference competition docs (SKILL.md, LITERATURE.md, PACKAGES.md), and recent outcomes from `results.tsv`, then generate concrete code suggestions:
- Model: mixture densities, NGBoost, quantile regression, ensembles
- Features: volatility regimes, cross-asset correlation, seasonality
- Architecture: online learning, Bayesian updating, horizon-specific models

### 5. Test
```bash
crunch test                    # Test solution locally
```

### 6. Update Tracking
After each significant experiment:
- append/update `results.tsv`
- refresh `SESSION-SUMMARY.md`
- optionally update `history.md` for long-form narrative

### 7. Submit
```bash
crunch test                    # Always test first
crunch push -m "Description"   # Submit
```

## Phrase Mapping

| User says | Action |
|-----------|--------|
| `what competitions are available` | `crunch list` |
| `show quickstarters for <name>` | Fetch from GitHub API |
| `set up <competition>` | Full workspace setup |
| `download the data` | `crunch download` |
| `get the <name> quickstarter` | `crunch quickstarter --name` |
| `explain this quickstarter` | Structured code walkthrough |
| `propose improvements` | Analyze and suggest code improvements |
| `continue working on <competition>` / `what's the latest` | Return Fast Continuation Response first |
| `keep going` / `let's continue` | Return Fast Continuation Response first |
| `test my solution` | `crunch test` |
| `compare with baseline` | Run both, side-by-side results |
| `submit my solution` | `crunch push` |

## Important Rules

- Entrypoint must be `main.py` (default for `crunch push`/`crunch test`)
- Model files go in `resources/` directory
- Respect competition interface and constraints (time limits, output format)
- Ask before installing new packages
- **NEVER call `crunch push` during iteration/experiment loops** — only `crunch test` is used for local testing. Each `crunch push` creates a submission on the hub and counts toward the daily submission limit (typically 5/day). Getting blocked means you exceeded this limit.
- `crunch push` requires **explicit human approval** and should only be called ONCE at the very end with the best result

## Reference

- CLI commands: [references/cli-reference.md](references/cli-reference.md)
- Setup examples: [references/competition-setup.md](references/competition-setup.md)
