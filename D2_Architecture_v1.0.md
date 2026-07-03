# D2: Integration Architecture & Technology Stack Document

**Version:** 1.0.0  
**Project:** Custom API Integration (SAP S/4HANA to Zetheta FinSight)  
**Client:** Meridian Manufacturing Ltd.

---

## 1. System Architecture Overview
The integration service is designed using the C4 model to isolate concerns and ensure horizontal scalability. Financial postings made in SAP S/4HANA are extracted asynchronously, transformed, and loaded into Zetheta FinSight.

```
+------------------+     (OData)     +---------------------+     (JSON)     +-------------------+
|  SAP S/4HANA     | --------------> | Integration Gateway | --------------> | Zetheta FinSight  |
|  (Universal Jnl) |                 | (FastAPI + SQLite)  |                 | (Financial Plt)   |
+------------------+                 +---------------------+                 +-------------------+
                                                |
                                                v
                                     +---------------------+
                                     |   Prometheus/Logs   |
                                     +---------------------+
```

## 2. Technology Stack Justification

| Technology | Selected | Alternatives Considered | Rationale for Selection |
|------------|----------|-------------------------|-------------------------|
| **API Framework** | **FastAPI** | Flask, Django | FastAPI provides native asynchronous support, superior speed, automatic Pydantic request validation, and out-of-the-box Swagger documentation. |
| **Local Cache DB** | **SQLite** | PostgreSQL, Redis | SQLite is a serverless, zero-config relational store, perfect for transaction buffering, local reconciliation, and quick prototype deployments. |
| **Data Validation** | **Pydantic** | Marshmallow, manual | Pydantic executes data validation at C-speed, integrating seamlessly with FastAPI's request-response lifecycle. |
| **Deployment Server**| **Uvicorn** | Gunicorn, Waitress | Uvicorn is an ultra-fast ASGI server that maximizes Python's asynchronous request processing throughput. |

## 3. C4 Architecture Level Design
- **System Context (Level 1):** The Integration Gateway interacts with SAP S/4HANA as the source system of record and Zetheta FinSight as the target analytics consumer.
- **Container Level (Level 2):** Detail shown in [DGM_C4_Container.png](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/diagrams/DGM_C4_Container.png). It consists of the FastAPI Router, Pydantic Validator, SQLite Buffering Database, Python Logger, and CSV Export Engine.
- **Component Level (Level 3):** Detail shown in [DGM_C4_Component.png](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/diagrams/DGM_C4_Component.png). It maps inner-component dependencies between HTTP request routes, DB query executors, and local logging sinks.

## 4. Risk Register & Mitigation Strategy

| Risk ID | Risk Description | Severity | Mitigation Strategy |
|---------|------------------|----------|---------------------|
| **RSK-01** | SAP gateway overload during delta extractions | High | Implement a Circuit Breaker pattern on RFC connections. Cap ODP delta queries to run every 30 minutes. |
| **RSK-02** | Data Residency regulatory breach (RBI FEMA Guidelines) | Critical | Configure AWS deployment to use only the ap-south-1 (Mumbai) region. Enforce encryption-at-rest. |
| **RSK-03** | Inconsistent journal records (unbalanced debits/credits) | High | Implement local reconciliation checks in `database.py` that verify sum of debits equals credits per document before caching. |
| **RSK-04** | Loss of network connection to FinSight API | Medium | Use the local SQLite database as a store-and-forward queue with exponential backoff retries. |
