# Innowave Accounts Payable Assistant

An automated solution for managing accounts payable workflows, invoice details extraction, audit validation checks, exception handling, and approval loops powered by AI agents.

## Project Structure

```
Innowave_Accounts_Payable_Assistant/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── backend/
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── extractor.py
│   │   ├── validator.py
│   │   ├── exception.py
│   │   ├── approval.py
│   │   └── recommender.py
│   ├── main.py
│   ├── workflow.py
│   ├── tools.py
│   ├── models.py
│   ├── google_services.py
│   ├── prompts.py
│   └── config.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup & Running

1. **Backend**:
   - Install dependencies: `pip install -r requirements.txt`
   - Run the FastAPI server: `uvicorn backend.main:app --reload`
2. **Frontend**:
   - Open `frontend/index.html` in your browser, or host it locally.
