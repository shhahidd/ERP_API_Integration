from fastapi import FastAPI, status, HTTPException

import time
from fastapi import Request

import sqlite3

import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.logger import logger

from app.models import (
    JournalEntry,
    JournalEntryResponse,
    MessageResponse,
    SummaryResponse,
    CompanySummaryResponse
)

from app.database import (
    create_database,
    insert_journal_entry,
    get_entries,
    get_journal_entry,
    update_journal_entry,
    delete_journal_entry,
    get_summary,
    get_company_summary,
    search_entries
)

app = FastAPI(
    title="ERP API Integration",
    version="1.0.0"
)

create_database()
@app.middleware("http")
async def log_request_time(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    logger.info(
        f"{request.method} {request.url.path} - {process_time:.2f} ms"
    )

    return response

@app.get("/")
def home():
    return {"message": "ERP API Integration is running successfully!"}


@app.get("/health")
def health():
    return {
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}

@app.get(
    "/analytics/summary",
    response_model=SummaryResponse
)
def analytics_summary():
    return get_summary()

@app.get(
    "/analytics/company-summary",
    response_model=list[CompanySummaryResponse]
)
def company_summary():
    return get_company_summary()

@app.get("/sap/journal-entries/{document_id}")

@app.get("/sap/journal-entries/search")
def search_journal_entries(q: str):
    return search_entries(q)

#CREATE
@app.post(
    "/sap/journal-entries",
    status_code=status.HTTP_201_CREATED
)
def create_journal_entry(entry: JournalEntry):

    try:
        insert_journal_entry(entry)

        logger.info(f"Journal entry {entry.document_id} created.")

        return {
            "message": "Journal entry saved successfully!",
            "data": entry
        }

    except sqlite3.IntegrityError:

        logger.error(f"Duplicate document ID: {entry.document_id}")

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Document ID '{entry.document_id}' already exists."
        )
    
    class CreateJournalResponse(BaseModel):
        message: str
        data: JournalEntryResponse

#READ
@app.get(
    "/sap/journal-entries/{document_id}",
    response_model=JournalEntryResponse
)
def get_journal_entry_by_id(document_id: str):

    entry = get_journal_entry(document_id)

    if entry:
        return entry

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Journal entry '{document_id}' not found."
    )

@app.get(
    "/sap/journal-entries",
    response_model=list[JournalEntryResponse]
)
def get_journal_entries(
    company_code: str | None = None,
    currency: str | None = None,
    account: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    sort_by: str = "document_id",
    order: str = "asc",
    limit: int | None = None,
    offset: int = 0
):
    
    return get_entries(
    company_code=company_code,
    currency=currency,
    account=account,
    start_date=start_date,
    end_date=end_date,
    sort_by=sort_by,
    order=order,
    limit=limit,
    offset=offset
)

#UPDATE
@app.put("/sap/journal-entries/{document_id}")
def update_entry(document_id: str, entry: JournalEntry):

    updated = update_journal_entry(document_id, entry)

    if updated:
        logger.info(f"Journal entry {document_id} updated.")

        return {
            "message": f"{document_id} updated successfully.",
            "data": entry
        }

    logger.warning(f"Update failed. Journal entry {document_id} not found.")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Journal entry '{document_id}' not found."
    )

#DELETE
@app.delete("/sap/journal-entries/{document_id}")
def delete_entry(document_id: str):

    deleted = delete_journal_entry(document_id)

    if not deleted:
        logger.warning(f"Delete failed. Journal entry {document_id} not found.")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal entry '{document_id}' not found."
    )

    logger.info(f"Journal entry {document_id} deleted.")

    return {
        "message": f"{document_id} deleted successfully."
    }

@app.get("/export/csv")
def export_csv():

    entries = get_entries()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
    "Document ID",
    "Company Code",
    "Account",
    "Amount",
    "Currency",
    "Posting Date"
    ])

    for entry in entries:
        writer.writerow([
            entry["document_id"],
            entry["company_code"],
            entry["account"],
            entry["amount"],
            entry["currency"],
            entry["posting_date"]
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=journal_entries.csv"
        }
    )