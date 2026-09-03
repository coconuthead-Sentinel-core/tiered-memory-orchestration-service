# Phase Gates

## Owner
- Approval owner: Shannon Brian Kelley
- Documentation prep date: 2026-04-22

## Gate 1: Discovery And Definition
- Entry criteria: mission, target users, and scope drafted
- Required artifacts: `PRD.md`, `SYSTEM_DESIGN.md`, `BACKLOG.md`
- Owners: project owner assigned
- Risks: recorded in `RISK_REGISTER.md`
- Exit criteria: scope, architecture direction, and validation approach documented
- Approval path: owner sign-off

## Gate 2: Build And Integration
- Entry criteria: prioritized backlog and baseline architecture present
- Required artifacts: API contracts, implementation, tests, engineering-build suite
- Owners: owner plus implementation support
- Risks: cloud dependencies, stale docs, and legacy artifact drift tracked
- Exit criteria: code and paperwork align, local validation passes
- Approval path: owner accepts validation evidence

## Gate 3: Release Readiness
- Entry criteria: tests and smoke checks pass
- Required artifacts: `QA_RELEASE_READINESS.md`, `DELIVERY_HANDOFF.md`, relevant compliance packet
- Owners: owner and release approver are the same for this repo
- Risks: exclusions explicitly recorded
- Exit criteria: release packet complete and mirrored to GitHub
- Approval path: owner accepts the release packet
