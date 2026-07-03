# ERP API Integration Gateway

**Version:** 1.0.0  
**Framework:** FastAPI + SQLite  
**Methodology:** Zetheta 15-Day FDE Challenge

---

## 1. Overview
The **ERP API Integration Gateway** is a RESTful integration gateway that simulates the data sync of financial journal entries from a client's ERP system (SAP S/4HANA) to the Zetheta FinSight analytics platform.

This gateway handles OData schema parsing, validates entries using Pydantic, stores logs locally, provides aggregated analytics, and streams compliance CSV exports.

---

## 2. Directory Structure
```text
ERP_API_Integration/
│
├── api/
│   ├── API_SAP_JournalEntry.yaml       # OpenAPI spec for SAP OData Extraction
│   ├── API_FinSight_JournalEntry.yaml  # OpenAPI spec for FinSight Gateway
│   └── Postman_Collection.json         # Postman API Collection
│
├── app/                                # FastAPI Application Package
│   ├── database.py                     # Database SQLite operations
│   ├── logger.py                       # Python Logging setup
│   ├── main.py                         # API Routes & Middleware
│   └── models.py                       # Pydantic Schemas
│
├── diagrams/                           # C4 Model Diagram Assets
│   ├── DGM_C4_SystemContext.drawio     # System Context XML
│   ├── DGM_C4_SystemContext.png        # System Context Image
│   ├── DGM_C4_Container.drawio         # Container Diagram XML
│   ├── DGM_C4_Container.png            # Container Diagram Image
│   ├── DGM_C4_Component.drawio         # Component Diagram XML
│   └── DGM_C4_Component.png            # Component Diagram Image
│
├── docs/                               # QA and Stakeholder Documents
│   ├── D6_Stakeholder_Communication_v1.0.md  # CFO, IT, Admin memos
│   ├── TEST CASES.md                   # Basic Test Cases table
│   └── TST_Functional_001.md           # 20+ Test Case Scenarios
│
├── presentation/                       # Final Slides
│   └── D6_Final_Presentation_v1.0.md   # Presentation script (Markdown)
│
├── screenshots/                        # Swagger & UI Run Verification
│   ├── 01-swagger-home.png
│   ├── 02-create-entry.png
│   ├── 03-get-all-entries.png
│   ├── 04-filter-sort-pagination.png
│   └── ... (additional UI confirmations)
│
├── CHANGELOG.md                        # Day-by-day project logs
├── D1_Requirements_v1.0.md             # Business goals and constraints
├── D2_Architecture_v1.0.md             # Tech justification and risk matrix
├── D3_API_Documentation_v1.0.md        # API Developer Documentation
├── MAP_JournalEntry_v1.0.md            # 50+ Field Mapping & DQ Checks
├── D5_Resilience_v1.0.md               # Retry, CB, dashboard, and alerts spec
├── D6_Deployment_Runbook_v1.0.md       # Zero-downtime blue-green rollout
├── erp.db                              # SQLite database file
├── erp.log                             # Local application log file
├── requirements.txt                    # Project requirements
└── README.md                           # This document
```

---

## 3. Getting Started

### 3.1 Create a Virtual Environment
```bash
python -m venv venv
```

### 3.2 Activate the Environment
- **Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Unix / macOS:**
  ```bash
  source venv/bin/activate
  ```

### 3.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.4 Run the Integration Gateway
```bash
uvicorn app.main:app --reload
```
The server will start on: `http://127.0.0.1:8000`

---

## 4. API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/` | Root Welcome |
| **GET** | `/health` | Gateway & Database Health Status |
| **POST**| `/sap/journal-entries` | Create/Save Journal Entry |
| **GET** | `/sap/journal-entries` | Query Journal Entries (Filter/Sort/Page) |
| **GET** | `/sap/journal-entries/{id}` | Get Journal Entry by Document ID |
| **PUT** | `/sap/journal-entries/{id}` | Update Existing Journal Entry |
| **DELETE**| `/sap/journal-entries/{id}`| Delete Journal Entry |
| **GET** | `/sap/journal-entries/search` | Full-text query on entries |
| **GET** | `/analytics/summary` | General totals & average financial metrics |
| **GET** | `/analytics/company-summary`| Entries & totals broken down by Company Code |
| **GET** | `/export/csv` | Streamed download of all entries in CSV |

---

## 5. Verification and QA
- **Swagger Documentation:** Access interactive documentation at `http://127.0.0.1:8000/docs`
- **ReDoc Documentation:** Access clean reference layout at `http://127.0.0.1:8000/redoc`
- **Automated Verification:** Execute the functional verify suite via uvicorn and request verification tests mapped in [docs/TST_Functional_001.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/docs/TST_Functional_001.md).