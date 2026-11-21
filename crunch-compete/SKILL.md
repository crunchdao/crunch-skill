---
name: crunch-compete
description: Use when working with Crunch competitions on hub.crunchdao.com - setting up a workspace, exploring quickstarters, building an offline validation, testing solutions locally, pushing submissions, and running/monitoring them in the cloud.
---

# Crunch Compete

Helps a user compete end-to-end in a Crunch competition: setup, understanding
the task, a trustworthy offline validation, local iteration, then push + cloud
run -- in a loop, until the user says stop.

**Never idle while something runs.** A cloud run takes minutes to hours, a
local experiment can too. Start the wait in the background (see step 9), then
immediately work on the next hypothesis: a new feature, another model, a
deeper search. Waiting is never a step of its own, and "waiting for the run"
is never a reason to end your turn.

This file is competition-agnostic. Data format, function signatures, metric,
injected parameters, extra packages and constraints vary per competition:
always defer to the competition's own overview page and quickstarter. For
scale, compare:

- Some competitions stream: `infer()` is a generator yielding one score per
  observation.
- Others are batch: `train(X_train, y_train, model_directory_path, ...)` /
  `infer(X_test, ...)` over whole dataframes.

Same platform, same CLI, almost nothing else in common.

- Docs: https://docs.crunchdao.com/
- Glossary (Submission, Run, Crunch, phases): https://docs.crunchdao.com/other/glossary

**Prerequisites:** Python 3.9+, `pip install crunch-cli --upgrade`, and a
setup token from the competition's page on the Hub -- always ask the user.

## Do this first: the setup token expires in 3 minutes

The `--token` for `crunch setup` is **single-use and expires ~3 minutes after
being issued**. **Run `crunch setup` immediately**, before reading docs or
planning. If it has expired, ask the user for a fresh one -- never work around
it, never guess or reuse one.

## What kind of competition is this? (type, not name)

The display name is marketing; the *type* decides the workflow. "Real-time" in
a *name* does **not** imply the Real-Time type: a streaming code interface can
still be scored offline by ordinary cloud runs. Check the overview page:

- **Offline**: code runs in the cloud against a dataset and gets scored.
  `crunch-cli` covers the whole loop. Most of this file.
- **Live-deployed**, called **Real-Time**: code runs continuously against a live feed, via a
  dedicated package (sometimes without `crunch-cli`). Where `crunch-cli` is
  used, it **stops at `push`**: deployment needs a human. Get to a validated,
  pushed submission, then hand off. `run create` returns an error.

Some competitions require extra packages (listed in their docs). Check the
**deadlines** against today's date before investing hours.

## Commands

The commands of the usual flow. This file can be outdated: when a command
rejects a flag or behaves differently from what is written here, trust
`crunch <command> --help`, and read the tips printed after most commands.

```
# workspace
crunch setup <competition> <project> [directory] --token <token>   # once, right away (token expires)
crunch status                                    # competition metadata, dates, docs links
crunch quota                                     # submissions, compute, whether a run is active
crunch download [--force]                        # (re)download the data

# starter code and libraries
crunch quickstarter list | show <name> | apply <name> [--overwrite]
crunch convert <notebook>.ipynb [main.py] --requirements [--overwrite]
crunch whitelist search <query>                  # is a library allowed in the cloud?
crunch whitelist validate [requirements.txt]

# local loop
crunch test [--main-file <file>] [--model-directory <directory>] [--no-force-first-train] [--no-determinism-check]

# submissions
crunch push -m "<message>" [--main-file <file>] [--model-directory <directory>] [--no-pip-freeze] [--dry]
crunch submission list [--limit N] [--all] [--original]
crunch submission show <number>
crunch submission update <number> --note "<text>"   # shown instead of the message
crunch submission checkout <number> [files...]

# cloud runs
crunch runtime list --submission <number>
crunch run create --submission <number> --runtime <runtime> [--force-first-train true] [--train-frequency N]
crunch run wait <run-id> [--timeout <seconds>]   # exit code: 0 succeeded, 3 failed, 4 timed out, 5 terminated, 1 error
crunch run show <run-id>                         # status, error, score
crunch run logs <run-id> [--tail N] [--follow] [--debug]
crunch run traces <run-id>                       # time, cpu and ram of each step, against the run's limits
crunch run list [--limit N] [--all]              # with the score of each run
crunch run terminate <run-id>

# standing and selection
crunch leaderboard
crunch run select <run-id>
```

## Mental model

- **setup** ~ `git clone`: restores your latest pushed code (or nothing).
- **submission** ~ git commit: an immutable snapshot of code + model artifact,
  message included.
- **run** ~ a CI pipeline run: executes one submission in the cloud, in a
  restricted environment, producing a prediction and (once scored) a metric.

A submission can sit unrun; one submission can be run several times.

## Workflow

Steps 5-9 are a **loop**. Once the user has asked you to compete, run it on
your own -- build, validate, push, run, check, iterate -- reporting progress
periodically. Don't ask permission for each push or run; stop only for a
genuine block (see "When something looks broken"). Selection (step 10) is the
user's call.

### 1. Set up the workspace

Run the user's ready-made command as-is:

```
crunch setup <competition-slug> <project-name> [directory] --token <token>
```

(`crunch list` resolves a slug from a display name if needed.)

- Data lands in `data/`. The **latest pushed submission is restored** -- it may
  be an old experiment; check `crunch submission list` before building on it.
- A brand-new project has no code (only `data/`, `resources/`, `.crunchdao/`).
  Check before assuming any file exists.

```
crunch status   # competition metadata, dates, docs links
crunch quota    # submission + compute budget + whether a run is active
```

### 2. Read the competition overview

`https://docs.crunchdao.com/competitions/competitions/<slug>` -- read it
**before** the quickstarter. It links to the problem, data, code interface,
metric, rules, required packages, deadlines and prizes.

### 3. Get starter code: quickstarters

```bash
crunch quickstarter list
crunch quickstarter apply <name>                      # --overwrite if files collide
crunch convert <notebook>.ipynb main.py --requirements
```

`convert` is silent -- check the output files exist. `--requirements` writes a
frozen `requirements.txt` and the original `requirements.original.txt`; fall
back to the latter if the frozen one fails to install in the cloud.

**Read every markdown cell of the quickstarter before writing code**: it is
the most authoritative spec (shapes, signatures, metric, constraints, often
"ideas for stronger solutions"). But it is a demo of the interface -- don't
feel bound by its approach or libraries; diverging is where the score comes
from.

You may move files that play no part in your solution out of the submission
tree (e.g. `scratch/`), but **every script or notebook used to generate a file
the submission relies on MUST be pushed**, even if left untouched afterwards.

### 4. Understand the code interface

- **Interface & dynamic parameters:**
  https://docs.crunchdao.com/competitions/participate/code-interface --
  signatures differ per competition. Parameters are injected **by name**
  (unknown name -> `None` or its default); type hints aren't enforced.
- **Notebook processing:**
  https://docs.crunchdao.com/competitions/participate/notebook-processor --
  only imports/functions/classes are kept; everything else is commented out.
  `# @crunch/keep:on` / `# @crunch/keep:off` preserve a section. First thing
  to check if a notebook behaves differently from a converted file.
- **Library whitelist:**
  https://docs.crunchdao.com/competitions/participate/whitelisted-libraries --
  validates `requirements.txt` (`crunch whitelist search <name>` and
  `crunch whitelist validate` check it from the command line). Requesting an
  addition (Resources section: PyPI name, import alias, GPU need) is normal. GitHub-only packages **must
  be vendored** into the submission: copy only the source you need (don't
  just `git clone`; strip tests, docs, examples...) and merge the package's
  own requirements into your `requirements.txt`.

**Data access rule:** never dump the full data into your context. Aggregates
(shape, `describe()`, group summaries) and a single example record are fine,
as are local scripts that process everything and print only aggregates.

### 5. Build an offline validation before building a model

This decides whether your iterations mean anything.

- **`crunch test` is not a real benchmark.** It checks your code runs
  end-to-end (interface, output, determinism). Its local test set is usually
  small: its score is noisy and can rank close models in the wrong order.
- **Build your own validation from the training data**, with the
  competition's metric (quickstarter or open-source scoring code). Make the
  holdout differ from training the way the competition's test set does.
- **Know your noise**: how much the score moves when only chance changes
  (another holdout draw, another seed). Smaller differences mean nothing.
- **Compare variants paired** -- same holdout, same seeds.
- **Screen on a subset, confirm on the full set.**
- **Single source of truth**: validation imports the exact code the
  competition's entrypoints use (the docs say which -- not every competition
  has `train()`/`infer()`); never a re-implementation. Cross-check once that
  an independently recomputed prediction matches `crunch test`'s output.
- **Calibrate against the cloud early**: push a first variant and note how far
  offline is from the cloud score.

### 6. Iterate locally (where you should spend your time)

```
crunch test                                                    # full local run, as the cloud does it
crunch test --no-force-first-train                             # if there is a training step: reuse the model
crunch test --main-file <file> --model-directory <directory>   # a variant, without touching the main one
```

- **Local is free; cloud is not** (weekly compute budget, daily submissions).
- **`crunch test` is not a perfect mirror.** Notably the cloud **blocks
  internet access**; code that downloads something passes locally and fails
  there. https://docs.crunchdao.com/competitions/participate/resources-limit#runs
- **Use the machine**: run independent experiments in parallel, each with
  capped threads, leaving a few cores to the user. Share large arrays across
  processes via memory-mapped files instead of loading copies.
- **Thread hygiene**: LightGBM, XGBoost, CatBoost, PyTorch and the BLAS
  behind numpy take every core by default. Two such jobs side by side fight
  over the cores and can both run several times slower than one alone, and a
  `crunch test` running next to an experiment slows down the same way. Give
  each process an explicit share (`n_jobs`/`num_threads`/`thread_count`,
  `torch.set_num_threads`, `OMP_NUM_THREADS`) so that the processes times
  their threads stay within `nproc`.
- **Variants side by side**: `--main-file` / `--model-directory` (on `test`
  and `push`) let variants coexist in one workspace -- no re-setup.
- **Sub-agents**, if available, suit independent hypotheses: own folder,
  entrypoint and model directory, core and time budget, and the exact baseline
  to beat on the same holdout. Re-verify their wins yourself.
- **Push what your validation picked.** Explore in parallel, and push each
  variant your validation backs with a message saying what it is -- pushing
  untested variants makes it hard to remember what was actually run, and
  submissions per day are limited (`crunch quota`): don't spend them on ideas
  your validation hasn't backed.

**Constraints of *some* competitions** (check the docs for which apply):

- **Determinism**: a re-run on part of the data must match within a tiny
  tolerance, or the submission is ineligible for prizes. Seed everything.
- **One-pass data**: iterables readable only once in the cloud (re-readable
  locally); step *t* must be answered before *t+1* arrives.
- **Time budget**: per-call overhead kills. ~300µs per call is fine on 10k
  calls, fatal on 10M; single-row library `predict` can be far slower than
  batch throughput suggests. Benchmark the inference path, not just the fit.
- **Memory budget**: cloud training runs within the chosen runtime's RAM.
  Estimate peak memory first -- Python lists of floats cost ~8x a float32
  array.

**Scratch files** (dumps, caches, harness, benchmarks) go in e.g. `scratch/`,
listed in `.gitignore` (`crunch push` respects it). So do the logs some
libraries write into the working directory, or they get pushed as code:
CatBoost's `catboost_info/` (`allow_writing_files=False`, or `train_dir=`),
Lightning's `lightning_logs/`, MLflow's `mlruns/`. **Reproducibility is
separate**: with the model directory left **empty**, the training step alone
must refill it completely -- prize eligibility requires this even when you
push a filled model directory.

**Keep a log** (e.g. `NOTES.md` at the workspace root -- **not** in
`scratch/`: push it with every submission) of everything: what you tried and
why, data findings, rejected ideas and their evidence, bugs, and one line per
pushed variant (submission, run id, description, offline score and noise,
cloud score). It's your memory and you need it for selection: `run list`
shows scores but not what each variant was.

### 7. Push a submission

```
crunch push -m "<message>"   # --main-file, --model-directory, --no-pip-freeze, --dry
```

`--no-pip-freeze` helps when locally pinned versions can't be installed in the
cloud. Write what changed and the offline score into the message: it is
immutable. Once a run of it is scored, record the outcome with a **note**,
which `crunch submission list` then shows instead of the message (marked `*`,
`--original` shows the messages again):

```
crunch submission update 12 --note "run 126301: 57.59% (offline 57.9%), AR(30) CUSUM"
```

**Clean the tree before pushing.** Everything under the workspace that is not
ignored is uploaded: downloaded datasets, cloned repositories, the resources of
another project or competition, caches, checkpoints of abandoned experiments.
Move them out of the workspace or list them in `.gitignore`; keep only what
the submission needs to run and to be reproduced. The submission and its
resources directory have size limits (`crunch quota`), and `push --dry` shows
what would be sent.

For a **live-deployed** competition, this is the last CLI step.

**Push all code needed to reproduce the submission**, including what didn't
make the final cut if it produced an artifact. Artifacts without the code that
made them, files of unknown origin, and long strings decoded at runtime make a
submission ineligible. Local training is allowed
(https://docs.crunchdao.com/competitions/faqs#can-i-train-a-model-locally);
omitting its code is what's not. A model that needs no training: mark "No
training" at run creation. Training you don't want run in the cloud: keep it
behind an early `return` in the training function, or as a documented script.

Rules vary per competition (`https://api.hub.crunchdao.com/v1/competitions/<slug>/rules`);
recurring themes: code under a **permissive, non-copyleft, OSI-approved
license allowing commercial use**, and broad rights granted to the sponsor.

### 8. Pick a runtime

```
crunch runtime list --submission <number>
crunch runtime request <runtime-name> --submission <number> --justification "<why>"
```

Availability can depend on the submission (a CUDA-mandatory package can grant
a GPU automatically). **Don't ask for a GPU the code doesn't need.** Requests
are **reviewed by a human** (answer by email), weigh your run history, and once
granted are permanent for the competition. Ground the justification in
something observed (a run that saturated CPU/RAM, as `crunch run traces`
shows); never request
speculatively. Keep running on CPU meanwhile.

### 9. Run it in the cloud -- and keep working while it runs

```
crunch run create --submission <number> --runtime <runtime-name>
crunch run wait <run-id> > run-<run-id>.log 2>&1 &   # in the background, then keep working
crunch run show <run-id>
crunch run logs <run-id> [--tail N] [--follow] [--debug]
crunch run traces <run-id>
crunch run list [--limit N] [--all]
crunch run terminate <run-id>
```

- **Wait in the background, never in the foreground.** `run wait` checks the
  run every 10 seconds and returns when it ends (exit code 0 succeeded,
  3 failed, 4 timed out, 5 terminated; 1 means `run wait` itself hit an
  error, the run may still be going). Agent harnesses kill a foreground
  command after a couple of minutes, so a foreground `run wait` gets cut off,
  and polling with `sleep` wastes the time. If your harness can run a command
  in the background and tell you when it ends, use that; otherwise start it
  as above, go back to your next experiment, and look at the log (or
  `crunch run show`) between two steps of that work.
- **One run at a time** (`crunch quota` shows whether one is running). Get
  the next variant ready meanwhile, so it can start as soon as the run ends.
- `--runtime` is required; `--submission` defaults to the latest.
- `--train-frequency` / `--force-first-train` are **not accepted by every
  competition** (check `run create --help` and the docs; unsupported ones
  error out). Where supported they **default to not training** -- pass them
  to retrain. Training is forced anyway if the model directory is empty.
- Where there is a training step, once per promising line of work run with
  `--force-first-train true`: it proves the model reproduces in the cloud
  (RAM, time, versions). The score should match the locally-trained run.
- Develop the next variant in a separate entrypoint file, never one that a
  running local test or a pending push is using.
- **The score can lag completion** (prediction status `checking`): re-read
  `run show` a minute later. Don't poll harder than the default.
- Once scored, put the score in the submission's note
  (`crunch submission update <number> --note "..."`) and in your log.
- `logs --debug` shows pip install failures (hidden by default).
- **`run traces` shows where a run spent its time and resources**: each step
  (train, infer, ...) with its duration, average cpu and peak ram against the
  runtime's limit, then the usage over the whole run. Use it, also while the
  run is going, to find the slow step, to check how close ram got to the
  limit before scaling the model up, and to ground a runtime request.
- **Failed runs still cost quota**: ~5% of duration for timeouts and
  terminations, ~30% for crashes; setup time is free; a run's timeout is your
  remaining quota + ~30 min.
- **Scoring code is open-source** (`competitions/<slug>/scoring/` in
  https://github.com/crunchdao/competitions; interface:
  `documentation/organizer/test.md`). Read the **actual source**, not a
  web-fetch summary -- summaries drop the details conclusions depend on.

### 10. Check standing, then select

```
crunch leaderboard
crunch quota
crunch run select <run-id>
```

`quota`: size caps, submissions per day (**reset at midnight UTC**), compute
hours, and whether a run is active (**only one at a time**). The leaderboard
lags and may be unavailable; `run show` is the reliable way to read a score.

**The leaderboard ranks your best run, not your selected one.** During the
competition it shows the best score among your runs; your selection is what
gets scored out of sample at the end. So the leaderboard can show a run you
did not select.

**Selection decides the user's result -- it is their call.** Don't leave it to
the automatic fallback: when nothing is selected, the *latest* successful run
is used, not the best. `run list` and `run show` mark it `selected (last, by
default)`, which only means that nobody chose: make the choice explicit with
`crunch run select <run-id>`, after which it shows as `selected`. A grace
window after the end is common but not guaranteed. The public score measures
fit to the public set: weigh how much tuning targeted it, the local/public
gap, model complexity, and whether a margin exceeds your noise. Present the
trade-off: "#42 is higher but heavily tuned; #38 is ~1pt lower and much
plainer -- stronger bet or safer bet?"

## When something looks broken

1. **Your own mistake** (bad assumption, slow code, memory blow-up) -- fix it.
2. **A documented constraint** (whitelist rejection, unsupported parameter,
   determinism failure, no internet, live deployment) -- read the docs, work
   within it.
3. **The platform or CLI misbehaving** (internal error, status contradicting
   logs, scored run without a score, backend rejecting a request) -- **stop and
   report with evidence**: exact command, error, stack frames, whether anything
   was created. Don't build a workaround or edit CLI internals.

API errors that mean **stop and report** (don't retry in a loop, don't work
around them; they print after a `---` line):

- `An internal error occured` -- a server error.
- `Crunch not found.`, `Current phase not found.`, `Round not found.` --
  the competition is over or misconfigured on the server.
- `Your token seems to have expired or is invalid.`, `Project not found.` --
  the workspace needs a new setup command from the user.
- `You do not have permission to access this resource` -- wrong credentials
  or environment.
- `You cannot participate in the competition yet` -- an account issue
  (verification, restriction, rules or terms not accepted, country): only the
  user can fix it.
- `This action cannot be done during the ... phase.` -- the phase does not
  allow it.

Errors to fix yourself: `Forbidden packages` (change or request the library),
`Submission is too big` / `The resources directory is too big` (clean the
tree), `Competition specific checks did not pass` (read the reason),
`The main file ... is missing` / `is invalid`, and `Daily submission limit
exceeded` (wait for midnight UTC, keep working locally).

**State your confidence**: when reporting a bug, leak, exploit or a too-good
score, say what you verified, what you inferred, and from which source. Report
a suspected leak or exploit; never use it.

## Known CLI gaps / quirks

- No `--format json` / `--non-interactive`; text output is inconsistent --
  don't parse it strictly. Use the exit code of `run wait` for scripts.
- `setup --token` has no non-interactive or environment-variable fallback --
  always get an explicit, fresh token from the user.

## Modeling pitfalls (competition-agnostic)

- **Understand the metric first.** If it compares entities at the same
  step/group, a feature that only trends with position carries no ranking
  information, yet looks predictive offline and crowds out real signal.
- **Per-entity constant features invite memorization**: given labels that are
  structured per entity, a tree model learns *which* entity rather than the
  pattern. Prefer features *normalized by* an entity's characteristics over
  features *describing* it.
- **An unbeaten baseline is information**: if varied approaches all land near
  it, change what you measure, not the model.
- **Capacity vs. features**: if bigger models, more rows or other
  regularization stay within noise, the information isn't in the features.
- **Ablate and believe it**: removing a feature group sometimes helps. Run
  paired leave-one-group-out checks after each significant addition.
- **Match library to workload**: a fast *fit* doesn't mean a fast *single-row
  predict*. Benchmark per-call inference; compiling a fitted tree ensemble into
  plain code (generated at load time from training code you submit) is a
  legitimate fix.
- **Benchmark before scaling up**: a timing script on synthetic data of the
  right shape takes seconds and can save a wasted run.
