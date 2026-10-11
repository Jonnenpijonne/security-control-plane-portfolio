# Architecture

## Architectural decision

The portfolio uses a read-only derived control plane rather than introducing another operational master database.

The control plane:

- reads or receives approved record references;
- validates relationship integrity;
- derives a cross-system case state;
- exposes unresolved ownership and evidence requirements; and
- retains a clear distinction between source status and derived status.

## Source boundaries

| Information | Authoritative source | Control-plane responsibility |
|---|---|---|
| Security incident | Incident register | Reference, relationship validation and derived completion state |
| Technical work | ITSM or operational ticketing | Reference and technical-status interpretation |
| Governance action | Governance/privacy workflow | Reference, owner and completion dependency |
| Evidence | Approved evidence store | Reference and verification-status interpretation |

## Trust boundaries

The demo assumes that source records may be incomplete or inconsistent. Referential integrity is therefore checked independently.

The validator can establish that:

- a referenced record exists;
- a relationship is internally consistent;
- required fields are present; and
- lifecycle rules produce the expected derived state.

It cannot establish that:

- a source statement is factually true;
- an approver had organizational authority;
- uploaded evidence is substantively sufficient; or
- an incident was investigated correctly.

Those remain accountable human and organizational responsibilities.

## Failure behavior

The model fails visibly:

- unresolved references fail validation;
- duplicate identifiers fail validation;
- unknown status values fail validation; and
- technically closed but organizationally unfinished cases are marked `ATTENTION_REQUIRED`, not silently closed.

## Integration with related portfolio projects

This repository uses concepts demonstrated elsewhere without copying their implementations:

- [Operations as a Service Blueprint](https://github.com/Jonnenpijonne/operations-as-a-service-blueprint) supplies the operational ownership and escalation context.
- [Infrastructure Change Quality Gate](https://github.com/Jonnenpijonne/infrastructure-change-quality-gate) demonstrates deterministic policy validation and audit evidence.
- [Governed Knowledge Base](https://github.com/Jonnenpijonne/governed-knowledge-base-portfolio) demonstrates Source of Truth, AI and publication boundaries.
- [RBAC-Lite](https://github.com/Jonnenpijonne/RBAC-Lite) provides an example access-governance domain.
