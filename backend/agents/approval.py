from models import APWorkflowState
from google_services import write_audit_log


def approval_node(state: APWorkflowState):

    print("Running Approval Agent")

    severity = state["severity"]
    risk_score = state["risk_score"]

    # LOW RISK
    if severity == "LOW" and risk_score <= 25:

        approval_status = "APPROVED"
        recommended_approver = "AUTO"
        approval_reasoning = (
            "All validations passed successfully."
        )

    # MEDIUM RISK
    elif severity == "MEDIUM":

        approval_status = "NEEDS_REVIEW"
        recommended_approver = "AP Manager"
        approval_reasoning = (
            "Medium-risk discrepancy detected. "
            "Manual review required."
        )

    # HIGH RISK
    elif severity == "HIGH":

        approval_status = "NEEDS_REVIEW"
        recommended_approver = "Finance Manager"
        approval_reasoning = (
            "High-risk financial discrepancy detected."
        )

    # CRITICAL
    elif severity == "CRITICAL":

        approval_status = "REJECTED"
        recommended_approver = "CFO"
        approval_reasoning = (
            "Critical validation failure detected."
        )

    else:

        approval_status = "NEEDS_REVIEW"
        recommended_approver = "AP Manager"
        approval_reasoning = (
            "Unable to determine risk category."
        )

    # Audit log: approval decision
    try:
        write_audit_log(
            invoice_number=state.get("invoice_number", ""),
            agent_name="Approval Agent",
            step_name="approval",
            action="decide",
            status=approval_status,
            reason=approval_reasoning,
            confidence_score=1.0
        )
    except Exception:
        pass

    return {
        "approval_status": approval_status,
        "recommended_approver": recommended_approver,
        "approval_reasoning": approval_reasoning,
        "current_step": "APPROVAL_COMPLETE"
    }
    