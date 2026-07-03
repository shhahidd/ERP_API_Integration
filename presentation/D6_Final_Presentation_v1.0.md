# Final Presentation: Custom ERP API Integration Gateway

**FDE Specialist Assignment Final Defense**  
**Presenter:** Shahid Patel  
**Client:** Meridian Manufacturing Ltd.  
**Platform:** Zetheta FinSight 4.2

---

## Slide 1: Project Overview & Core Business Problem
- **Meridian Tech Stack:** SAP S/4HANA (Universal Journal - ACDOCA table) at Pune data center.
- **Problem Statement:** CFO dashboard suffers from a 24-hour batch synchronization delay. Operational decisions are made using yesterday's numbers.
- **Objective:** Establish near-real-time data sync using standard OData API interfaces, protecting ERP performance while verifying 100% financial reconciliation.

---

## Slide 2: Technology Stack & Design Modularity
- **Language:** Python 3 (readability and speed of integration)
- **Framework:** FastAPI (native asynchronous support, automatic OpenAPI specs)
- **Validation:** Pydantic (data structures validation)
- **Database:** SQLite (local buffer cache, scalable path to PostgreSQL)
- **Server:** Uvicorn (high-performance ASGI runner)
- **Design Philosophy:** Modularity. Separate routing (`main.py`), database execution (`database.py`), schemas (`models.py`), and logger configuration (`logger.py`).

---

## Slide 3: C4 Integration Architecture
- **Level 1 (System Context):** Decouples SAP S/4HANA from the FinSight Analytics platform.
- **Level 2 (Container Level):** Shows gateway boundary containing API gateways, local caching DB, logging sinks, and export handlers.
- **Level 3 (Component Level):** Maps control flow inside the FastAPI engine, from request interceptors (middleware) to repository queries.
- *Visual reference available in `/diagrams` folder.*

---

## Slide 4: API Endpoint Specification
- `/` - Root checks.
- `/health` - API and database availability checks.
- `POST /sap/journal-entries` - Real-time insertion (returns 201 Created).
- `GET /sap/journal-entries` - Lists entries with filtering, pagination (`limit`/`offset`), and sorting (`sort_by`/`order`).
- `PUT /sap/journal-entries/{id}` - Updates entries.
- `DELETE /sap/journal-entries/{id}` - Removes entries.
- `/analytics/summary` & `/analytics/company-summary` - Calculations for dashboards.
- `/export/csv` - Streamed CSV exports for compliance.

---

## Slide 5: Data Mapping & India-Specific Localization
- **Universal Journal Mapping:** Mapped 50+ fields (ledger codes, accounts, profit centers, transaction keys) from ACDOCA to target analytics schemas.
- **Fiscal Calendar Mapping:** Maps standard Gregorian calendar inputs to the V3 April-March fiscal periods.
- **GST Preservation:** Keeps CGST/SGST/IGST breakdown integrity for tax audit trails.
- **Data Residency Compliance:** Processed and saved entirely within India borders (AWS ap-south-1) matching RBI mandates.

---

## Slide 6: Resilience & Fail-Safe Strategy
- **Exponential Backoff:** Standardized retry formulas prevent gateway thundering.
- **Circuit Breaker:** Halts downstream calls during target outage to buffer records locally.
- **Local Reconciliation Engine:** Verifies balance checks ($\text{sum of debits} = \text{sum of credits}$) before writing to DB.
- **Grafana Dashboards:** Designed 12+ monitoring panels and 15+ observability alert rules.

---

## Slide 7: Zero-Downtime Rollout Runbook
- **Rollout Method:** Blue-Green deployment to ensure zero service disruption.
- **Database Change Management:** Expand-Contract pattern to avoid schema crashes.
- **Rollback Window:** Verified netsh port forwarding switch in under 5 minutes.
- **Post-Deploy smoke testing:** Automating curl health tests immediately following load balancing.
