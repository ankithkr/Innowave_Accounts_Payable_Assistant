import json

from models import APWorkflowState
from prompts import RECOMMENDER_PROMPT
from llm import model
from google_services import write_audit_log


def recommender_node(state: APWorkflowState):

    print("Running Recommender Agent")

    try:

        invoice_status = state["invoice_status"]
        exceptions = state["exceptions"]
        validation_results = state["validation_results"]

        # Format exceptions and validation for prompt
        exceptions_text = json.dumps(exceptions, indent=2) if exceptions else "No exceptions"
        validation_text = json.dumps(validation_results, indent=2)

        # Build prompt with context
        prompt = RECOMMENDER_PROMPT.format(
            validation_results=validation_text,
            exceptions=exceptions_text,
            invoice_status=invoice_status
        )

        # Call Gemini to generate recommendations
        response = model.generate_content(prompt)

        # Clean response
        response_text = response.text.strip()
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")

        # Parse Gemini response
        gemini_response = json.loads(response_text)

        recommendations = gemini_response.get("action_items", [])
        final_recommendation = gemini_response.get("final_recommendation", "")
        risk_assessment = gemini_response.get("risk_assessment", "")

        # If no action items but invoice needs review, add generic one
        if not recommendations and invoice_status == "NEEDS_REVIEW":
            recommendations.append("Review invoice against exceptions before approval")

        # Audit log: recommender completed
        try:
            write_audit_log(
                invoice_number=state.get("invoice_number", ""),
                agent_name="Recommender Agent",
                step_name="recommender",
                action="recommend",
                status="COMPLETED",
                reason=final_recommendation,
                confidence_score=1.0
            )
        except Exception:
            pass

        return {
            "recommendations": recommendations,
            "final_recommendation": final_recommendation,
            "risk_assessment": risk_assessment,
            "current_step": "WORKFLOW_COMPLETE"
        }

    except Exception as e:

        print(f"Recommender Error: {e}")

        # Fallback to simple logic if Gemini fails
        recommendations = []
        if state["invoice_status"] == "APPROVED":
            final_recommendation = "All validation checks passed. Invoice approved for payment."
            recommendations.append("Invoice can be processed for payment.")
        elif state["invoice_status"] == "REJECTED":
            final_recommendation = "Invoice rejected due to critical validation failures."
            recommendations.append("Reject invoice and notify procurement team.")
        else:
            final_recommendation = "Invoice requires manual review before approval."
            recommendations.append("Review invoice against exceptions")

        # Audit log: recommender fallback
        try:
            write_audit_log(
                invoice_number=state.get("invoice_number", ""),
                agent_name="Recommender Agent",
                step_name="recommender",
                action="recommend_fallback",
                status="FAILED",
                reason=str(e),
                confidence_score=0.0
            )
        except Exception:
            pass

        return {
            "recommendations": recommendations,
            "final_recommendation": final_recommendation,
            "risk_assessment": str(e),
            "current_step": "WORKFLOW_COMPLETE"
        }
