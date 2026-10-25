# Hostile review: zero-red PR (rule 11.2) - 2026-10-25

1. Suppressions: auditor reports 0/0 after ELIMINATING all 6 pre-existing
   suppressions (2x E402 path-hack noqas -> hacks removed; F401/E402 readline
   -> explicit parse_and_bind use with documented ImportError degrade;
   F811 pandas -> TYPE_CHECKING naming fix; spark type:ignores -> unused,
   removed; test-only coverage omit -> auditor whitelists test-path omits
   with in-code rationale, source omits still flagged).
2. `|| true` count in CI after fix: ZERO (grep-verified). The three former
   false-green gates (spacy download, mypy, bandit) are blocking and each
   passed for real in this session (IPE-003.gates.green.log).
3. Tests: 64 -> 64 (none deleted); two `assert False` anti-patterns upgraded
   to pytest.raises(match=...) - strengthened. Coverage scope WIDENED
   (profile_system-only -> all src) with floor UNCHANGED at 60 (measured
   66.67). No tolerance widened, no seed tuned, no time frozen.
4. Dependency bumps move FORWARD to fixed versions (st>=5.6, transformers 5.x
   via resolution) - not dodge-pins. pandas/numpy untouched.
5. mypy third-party `follow_imports=skip` list: scoped to untyped heavy trees
   only; every first-party module is checked (23 files, Success). This is the
   documented D-P2 decision, not a silent narrowing - first-party strictness
   is unchanged from intent and now actually enforced.
6. Behaviour changes (RNG swap, stub removal, path-hack removal) each have a
   decision entry and green suite; the RNG change preserves per-orchestrator
   determinism (seeded default_rng) and no test asserts RNG-specific values.

## Verdict
MERGEABLE once CI green.
