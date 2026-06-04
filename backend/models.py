from typing import TypedDict, Optional


class APWorkflowState(TypedDict):
    # Input
    file_path: str
    file_name: str

    # Extractor
    extracted_data: dict
    extraction_status: str

    # Validator
    validation_results: dict
    validation_status: str
    po_data: dict

    # Exception
    exceptions: list
    severity: str
    invoice_status: str
    risk_score: int

    # Approval
    approval_status: str
    recommended_approver: str
    approval_reasoning: str

    # Recommender
    recommendations: list
    final_recommendation: str

    # Meta
    invoice_id: str
    invoice_number: str
    error_message: str
    current_step: str