import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEET_ID
from datetime import datetime
import uuid


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

def get_po_master_sheet():

    client = get_sheet_client()

    workbook = client.open_by_key(
        GOOGLE_SHEET_ID
    )

    worksheet = workbook.worksheet(
        "PO_MASTER"
    )

    return worksheet

def get_sheet_client():

    credentials = Credentials.from_service_account_file(
        "service_account.json",
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    return client

def fetch_po(po_number: str):

    sheet = get_po_master_sheet()

    records = sheet.get_all_records()

    for row in records:

        if str(row["po_number"]) == str(po_number):
            return row

    return None

def get_sheet(sheet_name: str):

    client = get_sheet_client()

    workbook = client.open_by_key(
        GOOGLE_SHEET_ID
    )

    return workbook.worksheet(
        sheet_name
    )

def write_invoice_result(state):

    sheet = get_sheet(
        "INVOICE_RESULTS"
    )

    row = [

        state["invoice_id"],
        state["invoice_number"],
        state["extracted_data"].get(
            "invoice_date", ""
        ),
        state["extracted_data"].get(
            "vendor_name", ""
        ),
        state["extracted_data"].get(
            "po_number", ""
        ),
        state["extracted_data"].get(
            "amount", 0
        ),

        state["invoice_status"],
        state["severity"],
        state["risk_score"],
        state["recommended_approver"],
        state["final_recommendation"],

        "",
        datetime.now().isoformat()

    ]

    sheet.append_row(row)


def write_exception(
    invoice_number,
    po_number,
    exception_data
):

    sheet = get_sheet(
        "EXCEPTIONS"
    )

    row = [

        str(uuid.uuid4()),

        invoice_number,
        po_number,

        exception_data.get(
            "type", ""
        ),

        exception_data.get(
            "severity", ""
        ),

        exception_data.get(
            "description", ""
        ),

        exception_data.get(
            "expected_value", ""
            ),

        exception_data.get(
            "actual_value", ""
        ),

        exception_data.get(
            "recommended_action", ""
        ),
        datetime.now().isoformat()

    ]

    sheet.append_row(row)


def write_audit_log(
    invoice_number,
    agent_name,
    step_name,
    action,
    status,
    reason,
    confidence_score=1.0
):

    sheet = get_sheet(
        "AUDIT_TRAIL"
    )

    row = [

        str(uuid.uuid4()),

        invoice_number,
        agent_name,
        step_name,
        action,
        status,
        reason,
        confidence_score,

        datetime.now().isoformat()
    ]

    sheet.append_row(row)