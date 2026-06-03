class ApprovalAgent:
    """Approval Agent handling workflow gates and email routes."""
    def __init__(self):
        pass

    async def get_path(self, amount: float):
        print(f"ApprovalAgent calculating gates for ${amount}")
        return ["Manager"]
