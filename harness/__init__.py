"""Two-loop evaluation harness.

Two independently-gated loops around the existing `agent.run()` contract:

  - eval-learning loop:  supervisor feedback -> rubric proposal -> approval
  - agent-update loop:   supervisor feedback -> prompt candidate -> A/B -> promotion

Everything here is file-backed under evals/ (see harness.storage.EVALS_DIR).
No parallel subagents, no Postgres, no ground-truth answer pairs required.
"""
