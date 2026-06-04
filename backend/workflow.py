from langgraph.graph import StateGraph, END
import uuid
from google_services import (
    write_invoice_result,
    write_exception
)

from models import APWorkflowState

from agents.extractor import extractor_node
from agents.validator import validator_node
from agents.exception import exception_node
from agents.approval import approval_node
from agents.recommender import recommender_node

from agents.orchestrator import (
    extraction_router,
    approval_router
)

# Create graph
workflow = StateGraph(APWorkflowState)

# Register nodes
workflow.add_node("extractor", extractor_node)
workflow.add_node("validator", validator_node)
workflow.add_node("exception", exception_node)
workflow.add_node("approval", approval_node)
workflow.add_node("recommender", recommender_node)

# Entry point
workflow.set_entry_point("extractor")

# Extractor routing
workflow.add_conditional_edges(
    "extractor",
    extraction_router,
    {
        "validator": "validator",
        "end": END,
    }
)

# Validator -> Exception
workflow.add_edge(
    "validator",
    "exception"
)

# Exception routing
workflow.add_conditional_edges(
    "exception",
    approval_router,
    {
        "approval": "approval",
        "recommender": "recommender"
    }
)

# Approval -> Recommender
workflow.add_edge(
    "approval",
    "recommender"
)

# End
workflow.add_edge(
    "recommender",
    END
)

# Compile graph
app_workflow = workflow.compile()


def run_workflow(file_path: str, file_name: str):

    state = {
        "file_path": file_path,
        "file_name": file_name,

        "extracted_data": {},
        "extraction_status": "",

        "validation_results": {},
        "validation_status": "",

        "exceptions": [],
        "severity": "",
        "invoice_status": "",
        "risk_score": 0,

        "approval_status": "NOT_REQUIRED",
        "recommended_approver": "AUTO",
        "approval_reasoning": "No approval required",

        "recommendations": [],
        "final_recommendation": "",

        "invoice_id": str(uuid.uuid4()),
        "invoice_number": "",

        "error_message": "",
        "current_step": "START"
    }

    final_state = app_workflow.invoke(state)

# Write final invoice result
    write_invoice_result(final_state)

# Write exceptions
    for exception in final_state["exceptions"]:

        write_exception(
            invoice_number=final_state["invoice_number"],
            po_number=final_state["extracted_data"].get(
                "po_number", ""
            ),
            exception_data=exception
        )

    return final_state