# Lifecycle and Exception Rules

## Normal lifecycle

1. An incident is registered.
2. Operational tickets are linked for investigation and remediation.
3. Governance or privacy actions are created when required.
4. Evidence requirements are linked to the accountable actions.
5. Technical work may close independently.
6. The control plane derives the overall case state from every required dependency.
7. An accountable human closes each authoritative record in its own system.

## Exception rule: technical closure is not complete closure

If an incident and its operational tickets are technically closed but at least one governance action is open, the derived state is `ATTENTION_REQUIRED`.

The same rule applies when a governance action requires evidence that is not verified.

## Exception rule: missing relationship

If a record references an identifier that does not exist, validation fails. The model must not silently drop the relationship.

## Exception rule: duplicate identifier

Identifiers must be unique within the complete dataset. Duplicate identifiers fail validation because they make ownership and evidence ambiguous.

## Exception rule: unknown lifecycle value

Unknown status values fail validation. Expanding the lifecycle requires an explicit policy and test change.

## Human-in-the-loop boundary

The validator does not:

- decide whether an incident is legally reportable;
- assess personal-data impact;
- approve a risk exception;
- verify the substance of evidence; or
- authorize closure.

It makes missing relationships and unfinished obligations visible to the person who holds that authority.
