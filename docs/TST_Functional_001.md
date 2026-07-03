# TST: Integration Testing Plan

**Version:** 1.0.0  
**Project:** Custom API Integration (SAP S/4HANA to Zetheta FinSight)  
**Client:** Meridian Manufacturing Ltd.

---

## 1. Test Environment Setup
- **API Host:** `http://127.0.0.1:8000`
- **Database:** Local SQLite (`erp.db`)
- **Validation Framework:** Pydantic 2.x
- **Testing Runner:** Python integration verification script

---

## 2. Functional Test Scenarios

### 2.1 Home API and Health Checks
- **TST-F-001:** GET `/` returns HTTP 200 welcome message.
- **TST-F-002:** GET `/health` returns status healthy, database connected.

### 2.2 Create Journal Entry (POST /sap/journal-entries)
- **TST-F-003:** Create entry with valid parameters returns HTTP 201 Created and saves data.
- **TST-F-004:** Create entry with existing Document ID returns HTTP 409 Conflict.
- **TST-F-005:** Create entry with missing document ID returns HTTP 422 Unprocessable Entity.
- **TST-F-006:** Create entry with string amount instead of float returns HTTP 422.
- **TST-F-007:** Create entry with invalid date string returns HTTP 422.

### 2.3 Read Operations (GET /sap/journal-entries)
- **TST-F-008:** Retrieve list of all journal entries returns HTTP 200.
- **TST-F-009:** Get existing journal entry by ID returns HTTP 200 and correct JSON record.
- **TST-F-010:** Get non-existent journal entry by ID returns HTTP 404 Not Found.

### 2.4 Update & Delete Operations (PUT/DELETE)
- **TST-F-011:** Update valid existing entry returns HTTP 200 and modifies fields in DB.
- **TST-F-012:** Update non-existent document ID returns HTTP 404 Not Found.
- **TST-F-013:** Delete existing entry returns HTTP 200 and removes row from DB.
- **TST-F-014:** Delete non-existent document ID returns HTTP 404 Not Found.

### 2.5 Querying, Filtering, and Sorting
- **TST-F-015:** Search entries using `/sap/journal-entries/search?q=MC01` returns matching results.
- **TST-F-016:** Filter entries by `company_code` returns correct subset of records.
- **TST-F-017:** Filter entries by currency returns correct subset.
- **TST-F-018:** Apply date range filter returns entries with posting date within bounds.
- **TST-F-019:** Sort entries by amount descending returns entries sorted correctly.
- **TST-F-020:** Pagination with limit and offset restricts result counts.

---

## 3. Non-Functional & Failure Injection Test Scenarios

### 3.1 Resilience Testing
- **TST-N-001 (Slow Query Mock):** Inject delay in SQLite query execution to trigger P95 latency monitoring alerts (ALT-001).
- **TST-N-002 (Database Locking):** Lock the SQLite file explicitly and check if the application handles lock timeout correctly with warning messages and retries.
- **TST-N-003 (Network Simulation):** Mock connection failures to Zetheta FinSight to verify the gateway switches to circuit breaker OPEN state and caches logs locally in `erp.db`.

### 3.2 Security Testing
- **TST-S-001 (Unauthorized Access):** Call endpoints without credentials or invalid auth headers and verify HTTP 401 response.
- **TST-S-002 (SQL Injection Prevention):** Inject SQL query strings in query parameters (e.g. `$q=1' OR '1'='1`) to verify Pydantic validator blocks or SQLite parameterized inputs prevent execution.
