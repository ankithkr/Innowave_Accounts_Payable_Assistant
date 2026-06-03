from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total_price: float

class InvoiceData(BaseModel):
    vendor_name: str
    invoice_number: str
    amount: float
    invoice_date: date
    items: List[InvoiceItem] = []

class AuditCheckResult(BaseModel):
    check_name: str
    passed: bool
    details: Optional[str] = None

class WorkflowState(BaseModel):
    invoice_id: str
    file_path: str
    extracted_data: Optional[InvoiceData] = None
    audit_checks: List[AuditCheckResult] = []
    gl_account: Optional[str] = None
    cost_center: Optional[str] = None
    status: str = "PENDING"
    errors: List[str] = []
