import json

from models import APWorkflowState
from tools import extract_pdf_text
from prompts import EXTRACTION_PROMPT
from llm import model
from google_services import write_audit_log


def extractor_node(state: APWorkflowState):

    print("Running Extractor Agent")

    try:

        # Extract text from PDF
        invoice_text = extract_pdf_text(
            state["file_path"]
        )

        # Build prompt
        prompt = EXTRACTION_PROMPT.format(
            invoice_text=invoice_text
        )

        # Gemini call
        response = model.generate_content(
            prompt
        )

        # Clean Gemini response
        response_text = response.text.strip()

        response_text = response_text.replace(
            "```json", ""
        )

        response_text = response_text.replace(
            "```", ""
        )

        # Convert JSON string -> Python dict
        extracted_data = json.loads(
            response_text
        )

        # Audit log entry
        try:
            write_audit_log(
                invoice_number=extracted_data.get("invoice_number", ""),
                agent_name="Extractor Agent",
                step_name="extractor",
                action="extracted",
                status="SUCCESS",
                reason="",
                confidence_score=1.0
            )
        except Exception:
            pass

        return {
            "extracted_data": extracted_data,
            "invoice_number": extracted_data.get(
                "invoice_number", ""
            ),
            "extraction_status": "SUCCESS",
            "current_step": "EXTRACTOR_COMPLETE"
        }

    except Exception as e:

        print(f"Extractor Error: {e}")

        # Audit log for failure
        try:
            write_audit_log(
                invoice_number=state.get("invoice_number", ""),
                agent_name="Extractor Agent",
                step_name="extractor",
                action="extraction_failed",
                status="FAILED",
                reason=str(e),
                confidence_score=0.0
            )
        except Exception:
            pass

        return {
            "extraction_status": "FAILED",
            "error_message": str(e),
            "current_step": "EXTRACTOR_FAILED"
        }