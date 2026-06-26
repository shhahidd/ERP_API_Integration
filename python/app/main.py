from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI(
    title="ERP API Integration",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "ERP API Integration is running successfully!"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/sap/journal-entries")
def get_journal_entries():
    file_path = Path(__file__).parent / "sample_data.json"

    with open(file_path, "r") as file:
        data = json.load(file)

    return data