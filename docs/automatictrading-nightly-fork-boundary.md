# AutomaticTrading NautilusTrader fork — Nightly merge trust boundary

**Status:** DRAFT PR source-only mitigation. **No change in default develop until authorized merge.**

## Root cause supported by source

At `AutomaticTrading/nautilus_trader` develop SHA `2568f2abd67c000c1d8b1422178149b07692268f`:

1. `.github/workflows/nightly-merge.yml` can run daily or manually with a secret named `NIGHTLY_TOKEN`, and calls `scripts/ci/plan-nightly-merge.bash`.
2. `plan-nightly-merge.bash` hardcodes the GitHub Actions REST URL for **`nautechsystems/nautilus_trader`**, using a candidate SHA's upstream build status as a criterion for an acceptable nightly branch merge.
3. `scripts/ci/merge-nightly.bash` performs `git merge --ff-only` and `git push origin nightly`.

On an organization fork, this risks using **a different repository's CI status to authorize updates of the fork's nightly branch**. The specific behavior depends on actual branch history/Actions/credentials, which were not observed. This is a source-level cross-repository trust-confusion risk, not proof that an unauthorized merge occurred.

## Proposed conservative change

In the nightly merge workflow, require `github.repository == 'nautechsystems/nautilus_trader'` for both the planning and merge jobs.

This makes the imported upstream nightly workflow **inert in the AutomaticTrading fork** even if manually triggered or scheduled. It does not change `develop`, `master`, release, Docker, source modules or any runtime service.

To enable a **fork-specific** nightly merge later, create a separate independently reviewed design that:
- Queries successful CI checks in the actual `github.repository` with exact SHA and expected trusted workflow ID/ref.
- Verifies fork branch history, fast-forward and provenance.
- Requires scoped authorization before any nightly branch push.
- Uses an environment with effective owner-required approvals, and strictly limited GitHub App token permissions.
- Adds synthetic workflow tests and failure-path checks before enabling the job.

## Source verification/acceptance

- Both jobs carry explicit upstream-only repository guard.
- Hard-coded upstream URL and merge scripts **remain unchanged**, but are not scheduled to execute in this fork under the proposed guard.
- No installation, CI workflow dispatch, nightly branch update or source-code execution was performed.
- Exact-head PR checks/review/merge and active repository settings: **UNVERIFIED**.

## Boundaries

No live trading, production changes, branch merge, images pushed, service restart, broker credentials, dataset migrations, PostgreSQL, LightRAG, legacy Chroma RAG or snapshots. This does not authorize editing CI runner settings or tokens.

Related conflicts: INT-025 (fork publication governance), INT-028 (cross-repo CI provenance), GOV-02 and GOV-04.
