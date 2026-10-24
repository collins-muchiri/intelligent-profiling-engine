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
