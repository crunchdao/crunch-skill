# CrunchDAO Hub API Reference

Base URL: `https://api.hub.crunchdao.com`

No authentication required for all endpoints below.

## Competition Metadata (v1)

### Get competition

```
GET /v1/competitions/{name}
```

Returns: format, status, description, prize pool, participant stats, dates.

Key fields:
- `format`: `TIMESERIES` | `UNSTRUCTURED` | `DAG` | `STREAM` | `SPATIAL`
- `status`: `OPEN` | `CLOSED`
- `statistics.participants`, `statistics.submissions`
- `prizePoolText`, `start`, `end`

### List competitions

```
GET /v1/competitions
```

Returns array of all competitions.

### Get targets

```
GET /v1/competitions/{name}/targets
```

Returns scoring targets. Key fields:
- `name`: target identifier (e.g. `prediction`)
- `rankOrder`: `ASCENDING` (lower=better) or `DESCENDING` (higher=better)
- `primary`: whether this is the main target

### Get metrics

```
GET /v1/competitions/{name}/metrics
```

Returns metric definitions. Key fields:
- `metricDefinition.name`: e.g. `roc-auc`, `spearman`
- `target`: which target this metric scores
- `multiplier`: display scaling (e.g. 100.0 for percentage display)
- `unit.suffix`: e.g. `%`

### Get rounds

```
GET /v1/competitions/{name}/rounds
```

Returns round info. Key fields:
- `number`: round number
- `start`, `end`: round dates
- `maxSubmissionsPerDay`: submission rate limit

## Leaderboard (v2)

### Get default leaderboard

```
GET /v2/competitions/{name}/leaderboards/@default
```

Returns full leaderboard with positions. Navigate the response:

```python
data = response.json()
for target in data["targets"]:
    for position in target["positions"]:
        rank = position["rank"]
        user = position["user"]["login"]
        mean = position["mean"]
        best = position["best"]
```

Key position fields: `rank`, `mean`, `best`, `user.login`, `project.name`

## Libraries (v2)

### List whitelisted libraries

```
GET /v2/libraries?size=1000
```

Returns paginated list of all whitelisted packages. Key fields:
- `name`: package name
- `language`: `PYTHON` | `R`
- `aliases`: import names
- `gpuRequirement`: `OPTIONAL` | `RECOMMENDED` | `REQUIRED`

## Competition Source Files (GitHub API)

Base: `https://raw.githubusercontent.com/crunchdao/competitions/master/competitions/{name}/`

| File | Purpose |
|------|---------|
| `scoring/scoring.py` | Scoring function |
| `scoring/runner.py` | How train/infer are called, output contract |
| `quickstarters/{qs}/main.py` | Baseline code (if Python file) |
| `quickstarters/{qs}/*.ipynb` | Baseline notebook |
| `README.md` | Competition description and links |

List quickstarters:
```
GET https://api.github.com/repos/crunchdao/competitions/contents/competitions/{name}/quickstarters
```

## Example: Full Briefing Fetch

```bash
NAME="structural-break-open-benchmark"

# Metadata
curl -s "https://api.hub.crunchdao.com/v1/competitions/$NAME"

# Targets + Metrics
curl -s "https://api.hub.crunchdao.com/v1/competitions/$NAME/targets"
curl -s "https://api.hub.crunchdao.com/v1/competitions/$NAME/metrics"

# Round info
curl -s "https://api.hub.crunchdao.com/v1/competitions/$NAME/rounds"

# Leaderboard top scores
curl -s "https://api.hub.crunchdao.com/v2/competitions/$NAME/leaderboards/@default"

# Scoring function source
curl -s "https://raw.githubusercontent.com/crunchdao/competitions/master/competitions/$NAME/scoring/scoring.py"

# Runner (train/infer contract)
curl -s "https://raw.githubusercontent.com/crunchdao/competitions/master/competitions/$NAME/scoring/runner.py"
```
