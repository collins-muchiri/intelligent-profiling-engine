# Data protection impact assessment

## Processing
Automated profiling of entities using unsupervised clustering and NLP over ingested records, with a
human-in-the-loop review step before any profile is actioned.

## First question, answered before anything else
Does the engine profile natural persons, or only organisations and other legal entities? The answer
determines the entire legal regime. Record it here explicitly. If any input record can resolve to an
identifiable natural person, the processing is personal data under the Kenya Data Protection Act 2019
and GDPR, and the following controls are mandatory rather than advisory.

## Lawful basis
TO BE RECORDED by the data controller before further development: consent, contract, legal
obligation, vital interests, public task or legitimate interests, with a legitimate-interests
assessment if that basis is chosen. A profiling system with no recorded lawful basis must not ingest
further data.

## Data subject and entity rights
Access, rectification, objection and erasure procedures, with the owner of each procedure named.
For profiling specifically, the right to object to automated processing and to obtain human review
of any significant decision.

## Retention and deletion
Profile retention period, decay rule for stale signals, and a deletion path that removes a subject
from clusters and from derived aggregates, not merely from the input table.

## Risks and mitigations
| Risk | Mitigation |
|---|---|
| Wrong profile drives a wrong decision about an entity | HITL gate enforced in code, see src/hitl_gate.py; decision authority named in docs/DECISION_AND_AUTHORITY.md |
| Clustering infers sensitive attributes | Sensitive-attribute proxy audit in EVAL_PLAN.md; suppress clusters whose dominant signal is a protected characteristic |
| Scope creep into surveillance use | Purpose limitation statement in README; licence does not grant surveillance use |
| Unbounded ingestion | Source allowlist and retention schedule enforced at ingest |
