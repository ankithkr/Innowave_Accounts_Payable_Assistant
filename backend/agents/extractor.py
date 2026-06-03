class ExtractorAgent:
    """Extractor Agent for extracting invoice structured values using OCR/LLM."""
    def __init__(self):
        pass

    async def extract_details(self, file_path: str):
        print(f"Extractor processing file: {file_path}")
        return {"invoice_number": "MOCK-1", "amount": 100.0}
