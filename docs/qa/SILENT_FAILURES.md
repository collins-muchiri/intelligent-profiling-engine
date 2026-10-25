# SILENT_FAILURES.md - dispositions (2026-10-25)

| # | Class | Disposition |
|---|---|---|
| 1 | CI `|| true` on THREE gates (spacy model download, mypy, bandit) | REMOVED - all three now blocking. The mypy gate additionally could not run at all (python_version=3.9 rejected; OOM on third-party trees) - see D-P2. bandit had a real B311 finding masked by `|| true`. |
| 2 | B311 `random.seed()/randint()` in generator orchestrator | FIXED at the source: instance-level `np.random.default_rng(seed)` (also stops mutating global RNG state). bandit now 0 findings and blocking. |
| 3 | Stub-class import fallbacks (terminal_ui, streaming) | FIXED: direct imports; failures surface at the import (D-P6). |
| 4 | gui_app close handler swallowed join/save errors (`except: pass` x2) | Converted to explicit `contextlib.suppress(RuntimeError)` for the thread join and a stderr-visible failure for profile save (ruff SIM105 autofix + review); teardown no longer fails invisibly. |
| 5 | F821 undefined `pd` in profile.py annotation (latent NameError for typing tools; masked because mypy never ran) | FIXED via TYPE_CHECKING import; mypy now proves the whole tree. |
| 6 | `except TypeError: continue` on tz-aware/naive datetime mixing (profile.py anomaly scan) | KEPT with disposition: the branch skips un-comparable timestamps and the skip is bounded by design (documented in code comment); flagged here as a known narrow-catch. Backlog: normalise timestamps to UTC at ingestion (issue filed). |
| 7 | spacy model download masked in CI | Download is blocking; local gate log proves en_core_web_sm imports. |
| 8 | Seeds/randomness census | global_seed from config (default 42) documented as SYNTHETIC-data reproducibility control, not test-tuned luck; no test asserts seed-specific values. |
