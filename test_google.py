import os
import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

prompt = """
Extract invoice information.

Return JSON only.

Invoice:
Invoice Number: INV-001
Vendor: ABC Supplies
Amount: 50000
PO Number: PO-1001
"""

response = llm.invoke(prompt)

print(response.content)