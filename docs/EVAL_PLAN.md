# Evaluation plan: measuring whether the profiles are any good

Unmeasured profiling is anecdote with a user interface. This plan produces the first published
numbers.

1. Labelled sample. Two hundred entity records labelled by two independent reviewers against the
   profile schema. Record inter-rater agreement; below 0.7 kappa the schema is ambiguous and must be
   revised before any metric is trusted.
2. Cluster stability. Re-run clustering on bootstrap resamples; report the distribution of adjusted
   Rand index against the full-data partition. Stability below 0.6 means the clusters are noise.
3. Extraction quality. Precision and recall of NLP-extracted attributes against the labelled sample,
   reported per attribute type, not as a single average.
4. Drift. Population stability index on feature distributions monthly; above 0.25 triggers review.
5. Sensitive-attribute proxy audit. Test whether any cluster or extracted attribute acts as a proxy
   for a protected characteristic; publish the result including negatives.
6. HITL effectiveness. Of profiles rejected or corrected at human review, report the rate and the
   reason taxonomy. A gate that never rejects anything is not a gate.

Publish all six in EVALUATION.md with dates and sample sizes. A metric without its sample size is
advertising.
