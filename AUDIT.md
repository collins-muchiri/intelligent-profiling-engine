# AUDIT.md - Phase 0 Forensic Audit

Repo: intelligent-profiling-engine
Audit date: 2026-10-24 (UTC, execution-environment clock)
Auditor: autonomous agent session (principal-engineer mission), account collins-muchiri
Status: Phase 0 complete for this repo. No production code changed during the audit (transient `profiles.json` from the CLI smoke removed).

## 1. Method

Clean clone at `/home/user/audit_ws/intelligent-profiling-engine` (main @ c735ca3). Raw outputs committed verbatim under `docs/evidence/audit-phase0/`:

| Evidence file | Command | Result |
|---|---|---|
| `2026-10-24-install.log` | `uv venv --python 3.12`; `uv pip install -r requirements-dev.txt --torch-backend=cpu`; `spacy download en_core_web_sm` | SUCCESS (~30s) |
| `2026-10-24-tests.log` | `python -m pytest tests -v --cov=src/profile_system` | 64 passed / 0 failed in 21.6s; coverage 75% of profile_system |
| `2026-10-24-lint-type-security.log` | `ruff check src tests`; `mypy src`; `bandit -r src -q`; `python run.py -c stats` | ruff: 157 errors; mypy: config error (python_version 3.9 unsupported by mypy>=1.8 - typecheck does not run at all); bandit: 1 Low/High-confidence (B311 in generator seed); CLI: PASS |
| `2026-10-24-app-run.log` | `streamlit run app.py --server.headless true` + GET /healthz,/ | 200/200 |

CI state at audit time (`gh run view 40114937243`): main is RED. Root causes captured: (a) py3.9 matrix job fails at dependency install (modern wheels require >=3.10); (b) `pip-audit` step fails (dependency vulnerabilities); (c) ruff step fails (matches the 157 local errors). Six dependabot PRs have been open since 2026-09-13.

Environment limits disclosed: no Docker daemon (Dockerfile/docker-compose not built locally), no macOS runner.

## 2. Inventory

- Python 4,149 LOC. Two source trees: `src/profile_system/` (721 stmts measured: cli 397, profile 157, nlp 79, logging_viz 39, unsupervised 28, hitl 15) and `src/generator/` (synthetic-data orchestrator, spark/streaming/parquet bridges, terminal UI) - NOT measured by the coverage config.
- Top-level `src/hitl_gate.py` (fail-closed human-approval gate), `app.py` (Streamlit dashboard), `gui_app.py`, `run.py` (CLI entrypoint), `examples/`.
- Tests: 64 across 9 files (8 unit + 1 integration), pytest configured in pyproject with coverage addopts.
- Makefile: help/install/dev/lint/type/test/test-cov/security/docker/docker-run/docs - a real Makefile, but NOT the mission contract (no bootstrap/data/train/evaluate/demo/bench/test-integration/test-e2e).
- CI: 1 workflow (matrix incl. py3.9 which cannot install), dependabot active (6 open PRs).
- Docs: ARCHITECTURE.md, CHANGELOG.md, SECURITY.md, CONTRIBUTING, CODE_OF_CONDUCT, docs/{DPIA.md, DECISION_AND_AUTHORITY.md, EVAL_PLAN.md, architecture.md, quickstart.md, index.md}, mkdocs.yml. Licence: LICENSE present. Tag: v0.3.0.
- Authorship: 10 x collins-muchiri noreply, 7 x `z@container` (AI-tooling session identity), 3 x bucky-ops noreply (former account name).

## 3. Run results

### 3.1 Install - PASS
Full dev stack installs cleanly on Python 3.12.15 via uv with CPU torch backend, including the spaCy model download. Note: `make install` uses bare `pip` and downloads the spaCy model at install time (network dependency; acceptable but not zero-network).

### 3.2 Tests - PASS (64/64), coverage 75% with an exclusion problem
All tests pass on 3.12. Coverage of `src/profile_system` is 75% (cli 78%, profile 83%, unsupervised 93%, hitl 100%, nlp 41%, logging_viz 54%). However `--cov` is scoped to `src/profile_system` only: `src/generator/` (~1,900 LOC incl. orchestrator, spark_generation, streaming) is excluded from measurement. Mission rule 0.3 explicitly forbids coverage configs that exclude real source dirs. The integration test does exercise the orchestrator, but its coverage is invisible.

### 3.3 Lint/type/security - FAIL / BROKEN / PASS-with-note
- ruff: 157 errors (21 safely fixable). The CI lint step fails identically.
- mypy: does not run - pyproject sets `python_version = 3.9`, rejected by mypy>=1.8 ("must be 3.10 or higher"). The type gate has been vacuously "passing" or failing silently; either way there is no typechecking today.
- bandit: one Low-severity B311 (random seed in synthetic generator - acceptable use, document suppression with reason).
- pip-audit: fails in CI (dependency vulnerabilities) - not re-run locally in Phase 0; P1 must resolve pins.

### 3.4 CLI and app - PASS
`python run.py -c "stats"` renders the engine statistics panel (exit 0). Streamlit dashboard serves `/healthz` and `/` with 200. Side effect noted: the CLI writes `profiles.json` into the repo cwd (removed after the run; should be configurable/ignored).

## 4. Gap matrix vs Definition of Done

| DoD | State | Evidence | Fix cost |
|---|---|---|---|
| D1 clean-clone ubuntu+macos | PARTIAL | local install+tests+app PASS on linux/py3.12; CI py3.9 job cannot install; macOS never run | S-M |
| D2 CI green + gates | FAIL | main red: py3.9 install, pip-audit, ruff (run 40114937243); no model-eval/data-contract/evidence-link/reproducibility/clean-clone gates | L |
| D3 coverage 85/75 | PARTIAL | 75% on profile_system; generator tree excluded from measurement (rule 0.3 issue) | M |
| D4 mypy strict + ruff clean | FAIL | mypy misconfigured (doesn't run); ruff 157 errors | M |
| D5 claims -> evidence | PARTIAL | README coverage badge says "37%" (stale/wrong vs measured 75%); docs/evidence seeded by this audit | S |
| D6 docs set | PARTIAL | strong: ARCHITECTURE, CHANGELOG, SECURITY, DPIA, DECISION_AND_AUTHORITY, EVAL_PLAN, quickstart; missing DATA.md, MODEL_CARD.md, THREAT_MODEL.md, RUNBOOK.md, DEPLOYMENT.md, PRIVACY.md (DPIA partially covers), ADR dir, SUPPORT.md | M |
| D7 adversarial QA | ABSENT | no docs/qa/; mission 3.4 demands alias-perturbation, blocking-cascade, drift tests | L |
| D8 self-review | PARTIAL | prior audit drove CHANGELOG 0.2.0 remediation; mission-grade hostile review pending | M |
| D9 release/GHCR/SBOM | PARTIAL | v0.3.0 tag; Dockerfile exists but no image build/SBOM in CI | M |
| D10 metadata/dependabot/protection | PARTIAL | dependabot active (6 stale open PRs); topics/branch protection to verify P1 | S |
| D11 live demo | ABSENT | no deployed instance; Streamlit local only | M |
| D12 STATUS/lie detector | PARTIAL | this audit | S |
| D13 15-min evaluator path | PARTIAL | docs/quickstart.md exists; needs the 4-command/3-screen format + verified run | S |
| D14 no theatre | PARTIAL | honest CHANGELOG and remediation history; misleading coverage badge; generator tree hidden from coverage | S-M |

Mission spec 3.4 delta: `PermittedUsePolicy` runtime enforcement and schema-level natural-person blocking are specified in docs/DPIA.md but NOT implemented in code (grep finds no enforcement module). Entity resolution (Fellegi-Sunter/SPLINK), graph features, UMAP/HDBSCAN, convergence-curve publication, React review console, FastAPI/Postgres/pgvector/Redis stack: absent. Current engine = rule-based profiler + clustering/anomaly basics + synthetic generator + HITL gates.

## 5. Risk register

| ID | Risk | Class | Sev | Remediation |
|---|---|---|---|---|
| R1 | mypy gate non-functional (config rejected) - type claims vacuous | integrity/correctness | P0 | P1: set python_version=3.12, run mypy, fix or baseline with reasons |
| R2 | CI red on main (py3.9 install, pip-audit, ruff) | correctness | P0 | P1: drop 3.9 from matrix (declare 3.11/3.12 floor), fix pins, ruff --fix + manual remainder |
| R3 | Coverage config excludes src/generator (~1,900 LOC) | integrity (0.3) | P0 | P1: measure both trees; justified exclusions only |
| R4 | Permitted-use charter documented but not enforced in code | legal/privacy (mission 3.4, Kenya DPA/GDPR) | P1 | P3: PermittedUsePolicy module + schema guard + tests proving blocks hold |
| R5 | README coverage badge "37%" matches nothing measurable | integrity (0.1) | P1 | P1: replace with evidence-linked number or remove badge |
| R6 | profiles.json written into repo cwd by CLI | hygiene/privacy | P2 | P1: configurable path + .gitignore |
| R7 | 6 stale dependabot PRs since 2026-09-13 | supply chain | P2 | P1: triage/merge after pins fixed |
| R8 | B311 bandit finding (synthetic seed) | security (low) | P3 | Document suppression with reason string |

## 6. Lie detector

| CLAIM | EVIDENCE | VERDICT |
|---|---|---|
| README badge "coverage 37% tests" | measured 75% of profile_system this session (tests.log); 37% matches nothing current | STALE/FALSE - fix badge |
| CHANGELOG 0.2.0 "runnable end-to-end, ships with tests, CI and Docker" | tests PASS locally; CI is RED; Dockerfile present but image never built in CI | PARTIAL |
| docs/DPIA.md / DECISION_AND_AUTHORITY.md human-gate claims | src/hitl_gate.py + tests/unit/test_hitl.py pass (fail-closed behaviour tested) | SUPPORTED for the gate; NOT enforced platform-wide (R4) |
| README "hybrid profiling: unsupervised + NLP + HITL" | unsupervised.py/nlp.py/hitl.py exist; nlp.py 41% covered; no embedding models wired (sentence-transformers declared, unused in profile_system per coverage misses) | PARTIAL |
| docs/EVAL_PLAN.md | plan only; no results artefacts committed | PLAN, NOT EVIDENCE - P5 must produce results or mark unproven |

## 7. Sequenced work plan

1. P1 Foundations (M): fix mypy config + ruff errors; CI matrix 3.11+3.12 x ubuntu+macos; resolve pip-audit pins; coverage over both src trees; badge truth-fix; Makefile -> full mission contract; uv migration + lockfile; profiles.json path/ignore; dependabot triage. PR.
2. P2 Data layer (M): DATA.md data cards for OpenSanctions samples/registers used by examples; synthetic generator labelled SYNTHETIC in filenames+schema+outputs (rule 0.5); pandera contracts on generator output; committed offline fixtures. PR.
3. P3 Core engine (L): PermittedUsePolicy + schema-level natural-person guard + audit log that cannot be disabled + tests proving blocks; probabilistic entity resolution (Fellegi-Sunter) with P/R curve output; graph features; embeddings wired or dependency dropped. PR.
4. P4 Service/API + UI (L): FastAPI service (healthz/readyz/livez, OpenAPI export), review console (start from Streamlit HITL queue, migrate to React only if budget), batch + streaming interfaces. PR.
5. P5 Evaluation (L): execute EVAL_PLAN.md: benchmark suite + committed baseline + regression gate; convergence curve (accuracy vs human reviews) + marginal value per review - the headline claim: prove or retract; metrics JSON to docs/evidence/metrics/. PR.
6. P6 Hardening (M): adversarial alias perturbation, blocking-cascade, embedding drift tests; false-positive cost model; THREAT_MODEL (STRIDE); semgrep/trivy/SBOM. PR.
7. P7 Presentation (M): 15-min path, market pack, demo deploy or recorded walkthrough, release/GHCR/SBOM, repo metadata. PR.
8. P8 Self-review (S-M): hostile pass, docs/review/REVIEW.md. Final PR.
