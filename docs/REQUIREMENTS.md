# Requirements and Acceptance Criteria

## R1 — Preserve Source of Truth ownership

The control plane must not become the authoritative source for incidents, tickets, governance decisions or evidence.

Acceptance criteria:

- Every record identifies its source system.
- Cross-system records are connected by stable identifiers.
- Derived state is distinguishable from source status.
- The demo does not write back to any source system.

## R2 — Expose cross-system relationships

An analyst must be able to identify all operational tickets, governance actions and evidence records connected to an incident.

Acceptance criteria:

- Every referenced identifier resolves to exactly one synthetic record.
- Missing and duplicate references fail validation.
- Reverse ownership can be reconstructed from the dataset.

## R3 — Prevent false closure

A technically closed incident must not be reported as organizationally complete while a required governance action or evidence item remains unfinished.

Acceptance criteria:

- Closed technical work with an open governance action derives `ATTENTION_REQUIRED`.
- Closed technical work with required but unverified evidence derives `ATTENTION_REQUIRED`.
- A case derives `CLOSED` only when the incident, related tickets, required governance actions and required evidence are complete.

## R4 — Keep decisions human-owned

Automation may validate structure and derive a status, but it must not approve evidence or close an accountable action.

Acceptance criteria:

- Approval and verification states exist as source data.
- The validator reports states but does not modify records.
- AI is described as an analysis and proposal layer only.

## R5 — Be safe to publish

The portfolio must demonstrate the model without exposing a real organization.

Acceptance criteria:

- All names and records are fictional.
- No credentials, internal URLs, production identifiers or customer data exist.
- Claims clearly distinguish a reference implementation from a production deployment.

## User stories

### Security owner

As a security owner, I want to see unresolved obligations connected to a technically closed incident so that organizational follow-up is not lost.

### Privacy owner

As a privacy owner, I want privacy assessments to remain independently visible so that a service ticket cannot implicitly close my decision.

### Service manager

As a service manager, I want an evidence-backed case status so that I can distinguish technical resolution from complete closure.

### Auditor or reviewer

As a reviewer, I want stable identifiers and deterministic validation so that I can trace why a case was reported in a particular state.
