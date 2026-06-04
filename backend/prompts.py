# Prompt templates consolidated

EXTRACTION_PROMPT = """
You are an Accounts Payable Invoice Extraction Agent.

Extract invoice information from the invoice text below.

Return ONLY valid JSON.

Required format:

{{
  "invoice_number": "",
  "invoice_date": "",
  "po_number": "",
  "vendor_name": "",
  "buyer_name": "",
  "gstin": "",
  "quantity": 0,
  "amount": 0.0,
  "currency": "INR"
}}

Invoice Text:

{invoice_text}
"""


EXCEPTION_MESSAGE_PROMPT = """
You are an AP auditor. Given the validation results, PO data, extracted invoice data, and an exception type, produce a concise one-sentence description of the exception.

Constraints:
- Output exactly one sentence.
- Sentence length should be between 5 and 12 words (inclusive).
- Return ONLY the sentence (no JSON, no lists, no extra text).

Validation Results:
{validation_results}

PO Data:
{po_data}

Extracted Data:
{extracted_data}

Exception Type: {exception_type}
Severity: {severity}
Context: {context}

Return a single sentence (5-12 words) describing the issue.
"""


RECOMMENDER_PROMPT = """
You are an expert Accounts Payable recommendations agent. Your job is to provide clear, actionable recommendations based on invoice validation results and exceptions.

Validation Results:
{validation_results}

Exceptions Found:
{exceptions}

Invoice Status: {invoice_status}

Based on the validation results and exceptions, provide:
1. A detailed final recommendation
2. Specific action items if needed
3. Any risks or concerns

Respond with ONLY a JSON object in this format:
{{
  "final_recommendation": "Clear, specific recommendation text",
  "action_items": ["item 1", "item 2"],
  "risk_assessment": "Assessment of risks if any"
}}
"""
