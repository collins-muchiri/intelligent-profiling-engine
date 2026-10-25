# DECISIONS.md

Zero-Red Mandate decisions (mission rule 11.6).

## D-P1 (2026-10-25) Python 3.9 dropped (matrix, requires-python, classifiers)

CPython 3.9 EOL 2025-10-31. The 3.9 CI leg was the standing install red.
Matrix now 3.10/3.11/3.12; requires-python >=3.10; ruff/black/mypy targets
aligned. No failure hidden: the 3.9 leg failed at install, and 3.10-3.12 run
the identical full gate set.

## D-P2 (2026-10-25) mypy made BLOCKING with third-party parse scoping

mypy previously ran as `mypy src || true` (a gate that cannot fail) with
python_version=3.9 (rejected by mypy>=1.8) and, when those were fixed locally,
OOM-killed parsing torch/transformers trees in a 2GB environment. Fix:
per-module `follow_imports="skip"` overrides for the heavy untyped third-party
trees ONLY (torch, transformers, sentence_transformers, spacy, streamlit,
sklearn, textblob, faker, numpy, pandas, matplotlib, yaml, scipy, plotly).
First-party src/ is fully checked: `Success: no issues found in 23 source
files`, blocking in CI, no `|| true` anywhere.

## D-P3 (2026-10-25) Coverage measured over ALL of src; badge corrected

The old gate measured only src/profile_system (75%) while src/generator
(~1,900 LOC) went unmeasured, and the README badge claimed "37%". Measuring
the whole src tree gives 66.67% against the pre-existing floor of 60 - the
floor was NOT lowered (it is unchanged at 60); the measurement scope was
WIDENED and still passes. Badge updated to the measured number with date.

## D-P4 (2026-10-25) sentence-transformers >=5.6,<6 (with transformers 5.x)

pip-audit --strict: sentence-transformers 3.4.1 carries PYSEC-2026-4164
(fixed 5.6.0) and pinned transformers 4.57.6 carried 9 advisories (fixes up
to 5.10.0). The old `<4` manifest constraint BLOCKED the only fixed versions.
Bumped both manifests (requirements.txt + pyproject), suite green on
st 5.7.0 / transformers 5.20.2 (no direct transformers imports exist in src).

## D-P5 (2026-10-25) Entry scripts require the installed package

app.py / gui_app.py used sys.path.insert hacks + E402 noqas. The package is
installable (pip install -e . / make install); the hacks and suppressions are
removed. Running the Streamlit app from an uninstalled checkout now fails
loudly with ModuleNotFoundError instead of silently depending on CWD tricks.

## D-P6 (2026-10-25) Silent-stub import fallbacks removed

terminal_ui.py replaced the real orchestrator with an empty stub CLASS on any
import error; streaming.py aliased it to `object` (and never used it). Both
converted to direct imports (packaging is fixed) / dead import removed:
import failures now surface at the broken import, not as phantom behaviour.

---

# Phase-0 audit decisions (2026-10-24, preserved verbatim)

# DECISIONS.md

Stop-and-log register (mission rule 0.11).

## D-001 Installed with `--torch-backend=cpu`

- Assumption: sentence-transformers pulls torch; CUDA wheels are ~2GB+ and useless in this sandbox and in CI.
- Rationale: zero-cost constraint (0.10); CPU wheels install in ~30s and all 64 tests pass on them. Documented so reproducers on GPU machines know the choice was deliberate.
- Reversibility: full (drop the flag).

## D-002 pip-audit failure taken from CI, not re-run locally

- Assumption: CI run 40114937243 already captured the pip-audit failure verbatim; re-running locally adds no information for Phase 0.
- Rationale: budget discipline (0.12); P1 resolves pins and the CI log remains the evidence of the pre-fix state.
- Reversibility: full.

## D-003 Python 3.9 dropped from the supported floor (proposed, not yet executed)

- Assumption: py3.9 cannot install the declared modern dependency set (CI evidence: build-dependency install error); ruff config already targets py39 syntax but mypy>=1.8 refuses python_version=3.9.
- Rationale: mission stack default is 3.12 with 3.11 floor in CI matrices. Recorded here as the decision P1 will implement; reversible until the CI change merges.
- Reversibility: full.

## D-004 `profiles.json` side effect removed, not committed

- Assumption: CLI smoke created runtime state in the repo root.
- Rationale: audit commits must contain only audit artefacts; the side effect is documented as R6 instead.
- Reversibility: full.

## D-005 Audit PR not merged while CI is red

- Assumption: rule 0.8 - merge only on green.
- Rationale: audit PR is docs/evidence-only and cannot turn the pre-existing red build green; P1 fixes CI, then the audit PR merges (or P1 supersedes it).
- Reversibility: full.
