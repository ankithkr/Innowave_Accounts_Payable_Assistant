import json
import google.generativeai as genai

from models import APWorkflowState
from prompts import EXCEPTION_MESSAGE_PROMPT
from google_services import write_audit_log


def exception_node(state: APWorkflowState):

    print("Running Exception Agent")

    validation = state["validation_results"]

    exceptions = []

    if not validation.get("po_exists", False):
        exceptions.append({
            "type": "PO_NOT_FOUND",
            "severity": "CRITICAL",
            "message": "Purchase Order does not exist"
        })

    if not validation.get("vendor_match", False):
        exceptions.append({
            "type": "VENDOR_MISMATCH",
            "severity": "HIGH",
            "message": "Vendor does not match PO"
        })

    if not validation.get("amount_match", False):
        exceptions.append({
        "type": "AMOUNT_MISMATCH",
        "severity": "HIGH",
        "description": "Invoice amount differs from approved PO amount",
        "expected_value":
            state.get("po_data", {}).get(
                "approved_amount", ""
            ),
        "actual_value":
            state.get("extracted_data", {}).get(
                "amount", ""
            ),
        "recommended_action":
            "Verify invoice amount with vendor"
        })

    if not validation.get("quantity_match", False):
        exceptions.append({
            "type": "QUANTITY_MISMATCH",
            "severity": "MEDIUM",
            "message": "Invoice quantity differs from approved quantity"
        })

    if not validation.get("currency_match", False):
        exceptions.append({
            "type": "CURRENCY_MISMATCH",
            "severity": "HIGH",
            "message": "Invoice currency differs from PO currency"
        })

    if not exceptions:
        return {
            "exceptions": [],
            "severity": "LOW",
            "risk_score": 0,
            "invoice_status": "APPROVED",
            "current_step": "EXCEPTION_COMPLETE"
        }

    # Use a lightweight Gemini model to craft concise exception messages
    try:
        model_lite = genai.GenerativeModel("gemini-2.5-flash-lite")
    except Exception:
        model_lite = None

    # Enrich exceptions with LLM-generated concise messages (5-12 words)
    for exc in exceptions:
        # Build prompt context
        prompt = EXCEPTION_MESSAGE_PROMPT.format(
            validation_results=json.dumps(validation, indent=2),
            po_data=json.dumps(state.get("po_data", {}), indent=2),
            extracted_data=json.dumps(state.get("extracted_data", {}), indent=2),
            exception_type=exc.get("type", ""),
            severity=exc.get("severity", ""),
            context=json.dumps(exc, indent=2)
        )

        generated_message = None

        if model_lite is not None:
            try:
                resp = model_lite.generate_content(prompt)
                text = getattr(resp, "text", "").strip()
                text = text.replace("```", "").strip()

                # Normalize to a single sentence and limit length (fallback trimming)
                # Keep as-is if it already looks concise
                words = text.split()
                if 5 <= len(words) <= 12:
                    generated_message = text
                else:
                    # Truncate/trim to 12 words if too long
                    if len(words) > 12:
                        generated_message = " ".join(words[:12]).rstrip(" ,.")
                    else:
                        # If too short or empty, leave None to fallback
                        generated_message = text

            except Exception:
                generated_message = None

        # Fallbacks: prefer existing message fields if LLM failed or produced empty
        if generated_message:
            exc["message"] = generated_message
        else:
            # Ensure a message key exists
            if "message" not in exc:
                exc["message"] = exc.get("description", "Exception detected")

    # Audit log: exception agent run
    try:
        write_audit_log(
            invoice_number=state.get("invoice_number", ""),
            agent_name="Exception Agent",
            step_name="exception",
            action="detect_exceptions",
            status="COMPLETED",
            reason=f"{len(exceptions)} exceptions",
            confidence_score=1.0
        )
    except Exception:
        pass

    severities = [e["severity"] for e in exceptions]

    if "CRITICAL" in severities:
        severity = "CRITICAL"
        risk_score = 95
        invoice_status = "REJECTED"

    elif "HIGH" in severities:
        severity = "HIGH"
        risk_score = 75
        invoice_status = "NEEDS_REVIEW"

    else:
        severity = "MEDIUM"
        risk_score = 50
        invoice_status = "NEEDS_REVIEW"

    return {
        "exceptions": exceptions,
        "severity": severity,
        "risk_score": risk_score,
        "invoice_status": invoice_status,
        "current_step": "EXCEPTION_COMPLETE"
    }