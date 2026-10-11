#!/usr/bin/env python3
"""Validate synthetic control-plane relationships and derive case state."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "examples" / "synthetic"

ALLOWED_TECHNICAL_STATUSES = {"open", "in_progress", "closed"}
ALLOWED_TICKET_STATUSES = {"open", "in_progress", "closed"}
ALLOWED_GOVERNANCE_STATUSES = {"open", "in_progress", "closed"}
ALLOWED_EVIDENCE_STATUSES = {"required", "submitted", "verified"}


class ValidationError(ValueError):
    """Raised when the control-plane dataset is internally inconsistent."""


def load_json(name: str, data_dir: Path = DATA_DIR) -> list[dict[str, Any]]:
    path = data_dir / name
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValidationError(f"{name}: top-level JSON value must be a list")
    return data


def index_unique(records: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise ValidationError(f"{label}: every record must have a non-empty string id")
        if record_id in indexed:
            raise ValidationError(f"{label}: duplicate id {record_id}")
        indexed[record_id] = record
    return indexed


def require_status(record: dict[str, Any], field: str, allowed: set[str]) -> None:
    value = record.get(field)
    if value not in allowed:
        record_id = record.get("id", "<unknown>")
        allowed_values = ", ".join(sorted(allowed))
        raise ValidationError(
            f"{record_id}: invalid {field}={value!r}; allowed values: {allowed_values}"
        )


def validate_dataset(data_dir: Path = DATA_DIR) -> dict[str, str]:
    incidents = index_unique(load_json("incidents.json", data_dir), "incidents")
    tickets = index_unique(
        load_json("operational-tickets.json", data_dir), "operational tickets"
    )
    actions = index_unique(
        load_json("governance-actions.json", data_dir), "governance actions"
    )
    evidence = index_unique(load_json("evidence.json", data_dir), "evidence")

    all_ids: set[str] = set()
    for label, records in (
        ("incidents", incidents),
        ("operational tickets", tickets),
        ("governance actions", actions),
        ("evidence", evidence),
    ):
        overlap = all_ids.intersection(records)
        if overlap:
            raise ValidationError(
                f"{label}: identifiers must be globally unique; duplicates: {sorted(overlap)}"
            )
        all_ids.update(records)

    for incident in incidents.values():
        require_status(
            incident, "technical_status", ALLOWED_TECHNICAL_STATUSES
        )
    for ticket in tickets.values():
        require_status(ticket, "status", ALLOWED_TICKET_STATUSES)
    for action in actions.values():
        require_status(action, "status", ALLOWED_GOVERNANCE_STATUSES)
    for item in evidence.values():
        require_status(item, "status", ALLOWED_EVIDENCE_STATUSES)

    derived: dict[str, str] = {}

    for incident_id, incident in incidents.items():
        ticket_ids = incident.get("operational_ticket_ids", [])
        action_ids = incident.get("governance_action_ids", [])
        evidence_ids = incident.get("evidence_ids", [])

        for ticket_id in ticket_ids:
            if ticket_id not in tickets:
                raise ValidationError(f"{incident_id}: missing ticket {ticket_id}")
            if tickets[ticket_id].get("incident_id") != incident_id:
                raise ValidationError(
                    f"{incident_id}: ticket {ticket_id} points to another incident"
                )

        for action_id in action_ids:
            if action_id not in actions:
                raise ValidationError(f"{incident_id}: missing governance action {action_id}")
            if actions[action_id].get("incident_id") != incident_id:
                raise ValidationError(
                    f"{incident_id}: governance action {action_id} points to another incident"
                )

        for evidence_id in evidence_ids:
            if evidence_id not in evidence:
                raise ValidationError(f"{incident_id}: missing evidence {evidence_id}")
            if evidence[evidence_id].get("incident_id") != incident_id:
                raise ValidationError(
                    f"{incident_id}: evidence {evidence_id} points to another incident"
                )

        required_evidence_ids: set[str] = set()
        for action_id in action_ids:
            for evidence_id in actions[action_id].get("required_evidence_ids", []):
                if evidence_id not in evidence:
                    raise ValidationError(
                        f"{action_id}: missing required evidence {evidence_id}"
                    )
                if evidence_id not in evidence_ids:
                    raise ValidationError(
                        f"{action_id}: evidence {evidence_id} is not linked by {incident_id}"
                    )
                required_evidence_ids.add(evidence_id)

        incomplete = incident["technical_status"] != "closed"
        incomplete = incomplete or any(
            tickets[ticket_id]["status"] != "closed" for ticket_id in ticket_ids
        )
        incomplete = incomplete or any(
            actions[action_id]["status"] != "closed" for action_id in action_ids
        )
        incomplete = incomplete or any(
            evidence[evidence_id]["status"] != "verified"
            for evidence_id in required_evidence_ids
        )

        derived[incident_id] = "ATTENTION_REQUIRED" if incomplete else "CLOSED"

    return derived


def main() -> int:
    try:
        states = validate_dataset()
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    for incident_id, state in sorted(states.items()):
        print(f"{incident_id}: {state}")
    print("Validation passed: all references and lifecycle rules are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
