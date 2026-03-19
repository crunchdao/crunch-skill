# Competition: {displayName}

Generated: {timestamp}
Competition: {name}

## Goal

{shortDescription from API}

- **Metric:** {metric name} — {DESCENDING = higher is better, ASCENDING = lower is better}
- **Prize:** {prizePoolText}
- **Status:** {status}
- **Deadline:** {round end date}
- **Max submissions/day:** {maxSubmissionsPerDay}

## Format & Interface

**Format:** {TIMESERIES | UNSTRUCTURED | DAG | STREAM}

### train() signature

```python
# Extracted from runner.py — what arguments train receives
def train(
    # ... arguments ...
    model_directory_path: str,
):
    # Must save model to model_directory_path
```

### infer() signature

```python
# Extracted from runner.py — what arguments infer receives, what it returns
def infer(
    # ... arguments ...
    model_directory_path: str,
):
    # Must return predictions in the expected format
```

### Output Contract

{From scoring.py check() function:}
- Output file(s): {e.g. prediction.parquet}
- Required columns: {e.g. prediction}
- Column dtypes: {e.g. float}
- Index: {e.g. integer id}
- Additional outputs: {e.g. prediction.noisy.parquet for anti-plagiarism}

## Scoring Function

```python
{Full scoring.py score() function inlined}
```

## Validation Checks

{From scoring.py check() function — list each check:}
- {e.g. Column must be named "prediction" and dtype float}
- {e.g. No NaN or infinite values}
- {e.g. IDs must match y_test exactly, no duplicates}
- {e.g. Anti-plagiarism: Spearman correlation with top-10 must be < 0.9}

## Data Summary

{From local EDA after crunch download:}
- **X_train:** {rows} × {cols}, index: {structure}
- **X_test:** {rows} × {cols}, index: {structure}
- **Target:** {column name}, dtype: {dtype}
  - Distribution: {for classification: class counts/balance; for regression: mean, std, min, max}
- **Features:** {list with dtypes, or summary if many}
- **NaN:** {columns with >0% NaN, or "none"}
- **Key observations:** {anything notable from EDA}

## Leaderboard Context

{From leaderboard API — top 10 for calibration:}

| Rank | User | Mean Score | Best Score |
|------|------|------------|------------|
| 1 | {login} | {mean} | {best} |
| ... | ... | ... | ... |

## Baseline Approach

{Description of quickstarter:}
- **Method:** {what the baseline does}
- **Baseline score:** {from experiment #0}
- **Why it's simple:** {what's left on the table}

## Literature & Packages

{From LITERATURE.md if exists, otherwise "None available in competition repo."}
{From PACKAGES.md if exists}

## Experiment Log

See `results.tsv` for all experiments and outcomes.
