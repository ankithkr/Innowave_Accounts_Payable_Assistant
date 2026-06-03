class ExceptionAgent:
    """Exception Agent for analyzing errors or mismatches."""
    def __init__(self):
        pass

    async def log_exception(self, reason: str):
        print(f"ExceptionAgent processing error: {reason}")
        return {"action": "flag_for_review"}
