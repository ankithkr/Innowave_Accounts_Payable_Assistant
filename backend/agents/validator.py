from models import APWorkflowState
from google_services import fetch_po, write_audit_log


def validator_node(state: APWorkflowState):

    print("Running Validator Agent")

    invoice = state["extracted_data"]

    po_number = invoice.get("po_number")

    po = fetch_po(po_number)

    if not po:

        validation_results = {
            "po_exists": False,
            "vendor_match": False,
            "amount_match": False,
            "quantity_match": False,
            "currency_match": False
        }

        # Audit log: PO not found
        try:
            write_audit_log(
                invoice_number=state.get("invoice_number", ""),
                agent_name="Validator Agent",
                step_name="validator",
                action="validate",
                status="FAIL",
                reason="PO not found",
                confidence_score=1.0
            )
        except Exception:
            pass

        return {
            "validation_results": validation_results,
            "validation_status": "FAIL",
            "current_step": "VALIDATOR_COMPLETE"
        }

    validation_results = {
        "po_exists": True,

        "vendor_match":
            invoice.get("vendor_name", "").strip().lower()
            ==
            po.get("vendor_name", "").strip().lower(),

        "amount_match":
            float(invoice.get("amount", 0))
            ==
            float(po.get("approved_amount", 0)),

        "quantity_match":
            float(invoice.get("quantity", 0))
            ==
            float(po.get("approved_quantity", 0)),

        "currency_match":
            invoice.get("currency", "INR")
            ==
            po.get("currency", "INR")
    }

    validation_status = (
        "PASS"
        if all(validation_results.values())
        else "FAIL"
    )

    # Audit log: validator completed
    try:
        write_audit_log(
            invoice_number=state.get("invoice_number", ""),
            agent_name="Validator Agent",
            step_name="validator",
            action="validate",
            status=validation_status,
            reason="",
            confidence_score=1.0
        )
    except Exception:
        pass

    return {
        "validation_results": validation_results,
        "validation_status": validation_status,
        "po_data": po,
        "current_step": "VALIDATOR_COMPLETE"
    }