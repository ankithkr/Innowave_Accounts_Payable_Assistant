class RecommenderAgent:
    """Recommender Agent predicting general ledger allocation settings."""
    def __init__(self):
        pass

    async def get_allocation(self, vendor: str):
        print(f"RecommenderAgent looking up allocations for {vendor}")
        return {"gl_account": "610000", "cost_center": "CC-102"}
