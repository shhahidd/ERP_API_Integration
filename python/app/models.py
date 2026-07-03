from pydantic import BaseModel
from datetime import date


class JournalEntry(BaseModel):
    document_id: str
    company_code: str
    account: str
    amount: float
    currency: str
    posting_date: date

from datetime import date
from pydantic import BaseModel

class JournalEntryResponse(BaseModel):
    document_id: str
    company_code: str
    account: str
    amount: float
    currency: str
    posting_date: date


class MessageResponse(BaseModel):
    message: str


class SummaryResponse(BaseModel):
    total_entries: int
    total_amount: float | None
    average_amount: float | None
    highest_amount: float | None
    lowest_amount: float | None


class CompanySummaryResponse(BaseModel):
    company_code: str
    entries: int
    total_amount: float