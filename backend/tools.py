# Common Tools for Agents and Workflow Execution

def calculate_sums(items: list) -> float:
    """Helper tool for validating line item sum math."""
    return sum(item.get("total_price", 0.0) for item in items)

def query_historic_codings(vendor: str) -> dict:
    """Simulates historic coding pattern lookups for GL assignment."""
    if "google" in vendor.lower():
        return {"gl_account": "610000 - IT Subscriptions", "cost_center": "CC-102 - Engineering"}
    return {"gl_account": "620000 - General Office Expenses", "cost_center": "CC-101 - Admin"}
