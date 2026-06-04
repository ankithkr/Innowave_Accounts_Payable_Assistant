from models import APWorkflowState


def approval_router(state: APWorkflowState):
    """
    Decide whether approval agent is needed.
    """

    invoice_status = state.get("invoice_status")

    if invoice_status == "NEEDS_REVIEW":
        return "approval"

    return "recommender"


def extraction_router(state: APWorkflowState):
    """
    Stop workflow if extraction fails.
    """

    if state.get("extraction_status") == "FAILED":
        return "end"

    return "validator"