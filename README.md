# Innowave Accounts Payable Assistant

An automated solution for managing accounts payable workflows. It accepts invoice uploads, extracts invoice fields with Gemini, validates against PO master data, classifies exceptions, routes approval, and records results plus audit trail entries.

## Local Setup

### 1. Create and activate a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create or update `.env` with at least these values:

```ini
GEMINI_API_KEY=<your Gemini API key>
GOOGLE_SHEET_ID=<your Google Sheet ID>
GOOGLE_SERVICE_ACCOUNT_FILE=backend/service_account.json
```

> The project currently uses `service_account.json` for Google Sheets access in `backend/google_services.py`.

### 4. Ensure Google service account access

- Place the Google service account JSON in `backend/service_account.json`.
- Grant that service account access to the target spreadsheet.

### 5. Start the backend server

```bash
uvicorn backend.main:app --reload --port 8000
```

### 6. Run the frontend

You can open `frontend/index.html` directly, or serve it with a simple HTTP server:

```bash
cd frontend
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080` in your browser.

### 7. Upload invoices

- Drag and drop or select a PDF/invoice file in the frontend.
- The frontend sends it to `http://127.0.0.1:8000/upload`.
- Results are displayed in the browser and written to Google Sheets.

## Project Structure

```
Innowave_Accounts_Payable_Assistant/
├── backend/
│   ├── agents/
│   │   ├── orchestrator.py   # workflow routing logic between agents
│   │   ├── extractor.py      # invoice extraction via Gemini LLM
│   │   ├── validator.py      # compare extracted invoice with PO data
│   │   ├── exception.py      # detect validation exceptions and classify severity
│   │   ├── approval.py       # decide approval status based on risk
│   │   └── recommender.py    # final recommendation generation with Gemini
│   ├── main.py               # FastAPI upload endpoint
│   ├── workflow.py           # langgraph workflow definition and invocation
│   ├── tools.py              # PDF text extraction helpers
│   ├── models.py             # typed workflow state definition
│   ├── google_services.py    # Google Sheets read/write helpers
│   ├── prompts.py            # prompt templates for LLM agents
│   ├── config.py             # environment variable loading
│   └── service_account.json  # Google Sheets service account credentials
├── frontend/
│   ├── index.html            # upload UI markup
│   ├── styles.css            # UI styling
│   └── app.js                # frontend upload and result rendering logic
├── .env                      # local environment configuration
├── .gitignore                # ignored files
├── requirements.txt          # Python dependency list
└── README.md                 # project documentation
```

## File Descriptions

- `backend/main.py` — starts the FastAPI app and defines `/upload` endpoint.
- `backend/workflow.py` — builds and runs the LangGraph state machine for the invoice workflow.
- `backend/agents/orchestrator.py` — decides whether to route to approval or recommender, and whether to stop after extraction failure.
- `backend/agents/extractor.py` — extracts invoice fields from the uploaded document using Gemini.
- `backend/agents/validator.py` — validates invoice data against PO master sheet values.
- `backend/agents/exception.py` — converts validation failures into structured exception records.
- `backend/agents/approval.py` — determines approval path and stakeholder recommendation.
- `backend/agents/recommender.py` — generates the final recommendation text using Gemini.
- `backend/tools.py` — provides PDF text extraction utilities.
- `backend/google_services.py` — reads PO data, writes invoice results, exceptions, and audit trail records to Google Sheets.
- `backend/models.py` — defines the workflow state data structure.
- `backend/prompts.py` — stores prompt templates for the LLM agents.
- `backend/config.py` — loads `.env` values.
- `frontend/index.html` — UI for file upload and result display.
- `frontend/styles.css` — styling for the frontend.
- `frontend/app.js` — handles drag-and-drop uploads, backend requests, and result rendering.

## Notes

- Frontend calls backend at `http://127.0.0.1:8000/upload`.
- The backend writes audit logs, invoice results, and exceptions to Google Sheets.
- `backend/creds.json` is not currently used by the code.
