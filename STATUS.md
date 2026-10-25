# STATUS.md

Last updated: 2026-10-24 (UTC) by Phase 0 audit session.

## Where this repo stands

- Phase 0 (forensic audit): COMPLETE. See `AUDIT.md`, `docs/PROVENANCE.md`, verbatim evidence in `docs/evidence/audit-phase0/`.
- Phases P1-P8: NOT STARTED.
- Honest completion vs Definition of Done: ~45%. This is the strongest of the five repos: the full test suite passes (64/64) on Python 3.12, the CLI and Streamlit dashboard run, docs are substantive. What blocks "done": CI is red on main (py3.9 install, pip-audit, ruff), mypy does not actually run (config rejected), coverage excludes src/generator, the permitted-use charter is documented but not enforced in code, and the evaluation plan has no results.

## What actually runs right now (verified this session)

| Command | Result |
|---|---|
| `uv venv --python 3.12` + `uv pip install -r requirements-dev.txt --torch-backend=cpu` + spacy model | PASS (~30s) |
| `pytest tests -v --cov=src/profile_system` | 64 PASSED, 0 failed, 21.6s; coverage 75% (profile_system only; generator excluded) |
| `ruff check src tests` | FAIL: 157 errors |
| `mypy src` | BROKEN: pyproject python_version=3.9 rejected by mypy>=1.8 |
| `bandit -r src -q` | 1 Low (B311, synthetic-data seed) |
| `python run.py -c "stats"` | PASS (writes profiles.json into cwd - removed after run) |
| `streamlit run app.py --server.headless true` + GET /healthz,/ | 200/200 |
| GitHub Actions main (run 40114937243) | RED: py3.9 install fails, pip-audit fails, ruff fails |

## Known-broken / not real

1. CI red on main (three independent causes above).
2. mypy gate vacuous (misconfigured python_version).
3. Coverage blind spot: src/generator (~1,900 LOC) unmeasured - rule 0.3 issue.
4. README coverage badge claims 37%; measured reality is 75% of profile_system - badge matches nothing.
5. PermittedUsePolicy / natural-person schema block: documented in docs/DPIA.md, absent from code.
6. EVAL_PLAN.md has no committed results; convergence-curve headline claim unproven.

## Exact next commands for the next operator

```bash
git clone https://github.com/collins-muchiri/intelligent-profiling-engine
cd intelligent-profiling-engine
uv venv --python 3.12
uv pip install -r requirements-dev.txt --torch-backend=cpu
uv run python -m spacy download en_core_web_sm
uv run pytest tests            # expect 64 passed
uv run ruff check src tests    # expect 157 errors (P1 target)
# then start P1 per AUDIT.md section 7
```

## Checkpoint log

- 2026-10-24 Phase 0: install/tests/lint/type/security/CLI/app executed, outputs captured verbatim; AUDIT.md + PROVENANCE.md + STATUS.md + DECISIONS.md committed on `audit/phase-0`; PR opened. CI on main red for pre-existing reasons; merge waits for green per rule 0.8.
