from fastapi import FastAPI

from app.models import JournalEntry
from app.database import (
    create_database,
    insert_journal_entry,
    get_all_entries,
    update_journal_entry,
    delete_journal_entry,
)

app = FastAPI(
    title="ERP API Integration",
    version="1.0.0"
)

create_database()

@app.get("/")
def home():
    return {"message": "ERP API Integration is running successfully!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/sap/journal-entries")
def create_journal_entry(entry: JournalEntry):
    insert_journal_entry(entry)

    return {
        "message": "Journal entry saved successfully!",
        "data": entry
    }

@app.get("/sap/journal-entries")
def get_journal_entries():
    return get_all_entries()

@app.put("/sap/journal-entries/{document_id}")
def update_entry(document_id: str, entry: JournalEntry):

    updated = update_journal_entry(document_id, entry)

    if updated:
        return {
            "message": f"{document_id} updated successfully.",
            "data": entry
        }

    return {
        "message": f"{document_id} not found."
    }

@app.delete("/sap/journal-entries/{document_id}")
def delete_entry(document_id: str):

    deleted = delete_journal_entry(document_id)

    if deleted:
        return {
            "message": f"{document_id} deleted successfully."
        }

    return {
        "message": f"{document_id} not found."
    }