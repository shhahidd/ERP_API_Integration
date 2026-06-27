from pydantic import BaseModel
from datetime import date


class JournalEntry(BaseModel):
    document_id: str
    company_code: str
    account: str
    amount: float
    currency: str
    posting_date: date