# PROVENANCE

## Origin

- Not a fork (`gh repo view --json isFork,parent` -> false/none, checked 2026-10-24).
- Owned by `collins-muchiri` (formerly `bucky-ops`; same GitHub user id 83084745).

## Authorship census (main @ c735ca3, 20 commits)

| Email | Commits | Interpretation |
|---|---|---|
| `83084745+collins-muchiri@users.noreply.github.com` | 10 | Owner, current account name |
| `z@container` | 7 | Commits authored inside an AI-tooling container session; not a personal mailbox |
| `83084745+bucky-ops@users.noreply.github.com` | 3 | Owner, former account name |

Disclosure: part of the history was produced by AI-assisted tooling under the owner's direction, including container-identity commits. CHANGELOG.md documents a v0.1 -> v0.2.0 audit-remediation cycle (real bug fixes: SyntaxError in terminal_ui.py, CLI argparse rework), which this Phase 0 audit independently re-verified by execution (64/64 tests pass).

## Licence

- LICENSE present (see file header; MIT-style). Compatible with planned data sources: OpenSanctions sample sets (OpenSanctions Licence NC - noncommercial; flagged for P2 DATA.md review before bundling), GLEIF LEI (CC0), Companies House-style open data, Faker-generated synthetic data (MIT). A licences policy gate is scheduled for P1 CI.

## Third-party code

- No vendored upstream trees. Declared deps: scikit-learn, pandas, numpy, matplotlib, spacy (+en_core_web_sm model downloaded at install), textblob, sentence-transformers, PyYAML, Faker, streamlit; dev: pytest/cov/benchmark, ruff, black, mypy, pip-audit, bandit, pre-commit. `requirements.txt` header documents that an earlier revision contained fictional future pins (torch 2.10.0 etc.) and was regenerated from a real audit - disclosed here as part of the repo's honesty record.

## Data

- No real entity/personal data committed. `src/generator/` produces synthetic organisational data via Faker; examples/ use generated records. Per rule 0.5, P2 will enforce SYNTHETIC labelling in filenames, schemas, and outputs. OpenSanctions sample sets are not yet vendored; when added they will carry licence + retrieval metadata in DATA.md.

## Automation artefacts

- Six dependabot branches/PRs open since 2026-09-13 (actions/checkout, actions/setup-python, faker, pyarrow, pyspark, sentence-transformers). Left open per rule 0.8 (no branch deletion); triage scheduled P1.
