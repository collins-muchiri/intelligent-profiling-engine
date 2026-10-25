"""Enforceable human-in-the-loop gate.

A profile action cannot be created unless a recorded human approval exists. This converts the
README principle into a control that fails closed: if the approval record is missing, malformed or
expired, the gate raises and nothing is emitted.
"""
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


class GateError(RuntimeError):
    pass


@dataclass(frozen=True)
class ApprovalRecord:
    approver_role: str
    approver_id: str
    profile_id: str
    approved_at: str          # ISO 8601 UTC
    scope: str                # the single action approved
    evidence_ref: str         # what the approver looked at

    MAX_AGE_HOURS = 72

    def validate(self):
        if not self.approver_role or not self.approver_id:
            raise GateError("approval must name a role and an identifier")
        if self.scope in ("*", "all", ""):
            raise GateError("blanket approvals are not approvals")
        ts = datetime.fromisoformat(self.approved_at.replace("Z", "+00:00"))
        if datetime.now(timezone.utc) - ts > timedelta(hours=self.MAX_AGE_HOURS):
            raise GateError("approval expired; re-review required")


def emit_profile_action(profile_id: str, action: str, approval: ApprovalRecord | None):
    if approval is None:
        raise GateError(f"refusing {action} on {profile_id}: no human approval recorded")
    if approval.profile_id != profile_id or approval.scope != action:
        raise GateError("approval does not match this profile and action")
    approval.validate()
    return {"profile_id": profile_id, "action": action,
            "approved_by": approval.approver_role, "approval": json.dumps(approval.__dict__)}
