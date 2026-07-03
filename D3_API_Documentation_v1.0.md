# D3: API Specifications & Documentation

**Version:** 1.0.0  
**Project:** Custom API Integration (SAP S/4HANA to Zetheta FinSight)  
**Client:** Meridian Manufacturing Ltd.

---

## 1. Overview
The Integration Gateway provides RESTful JSON endpoints for managing financial journal entries extracted from SAP ERP. The documentation below details the communication protocols, paging, authentication, and error formats.

## 2. Global API Settings
- **Protocol:** HTTPS only
- **Format:** JSON (`application/json`)
- **Authentication:** Basic Auth / Bearer Token (validated against Azure AD / Keycloak credentials)
- **Time Zone:** Indian Standard Time (IST - UTC+05:30)

## 3. Core API Endpoints

### 3.1 Create Journal Entry
- **Endpoint:** `POST /sap/journal-entries`
- **Description:** Receives a new journal entry payload from SAP, validates field compliance, and inserts it.
- **Request Headers:**
  - `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "document_id": "JE1001",
    "company_code": "MC01",
    "account": "400100",
    "amount": 1250.00,
    "currency": "INR",
    "posting_date": "2026-06-01"
  }
  ```
- **Success Response (201 Created):**
  ```json
  {
    "message": "Journal entry saved successfully!",
    "data": {
      "document_id": "JE1001",
      "company_code": "MC01",
      "account": "400100",
      "amount": 1250.0,
      "currency": "INR",
      "posting_date": "2026-06-01"
    }
  }
  ```

### 3.2 Get All Journal Entries
- **Endpoint:** `GET /sap/journal-entries`
- **Description:** Retrieve entries filtered by company code, currency, GL account, and posting dates. Includes pagination and sorting.
- **Query Parameters:**
  - `company_code` (string, optional)
  - `currency` (string, optional)
  - `account` (string, optional)
  - `start_date` (string `YYYY-MM-DD`, optional)
  - `end_date` (string `YYYY-MM-DD`, optional)
  - `sort_by` (string, default: `document_id`)
  - `order` (string: `asc` or `desc`, default: `asc`)
  - `limit` (integer, optional)
  - `offset` (integer, default: 0)
- **Success Response (200 OK):**
  ```json
  [
    {
      "document_id": "JE1001",
      "company_code": "MC01",
      "account": "400100",
      "amount": 1250.0,
      "currency": "INR",
      "posting_date": "2026-06-01"
    }
  ]
  ```

### 3.3 Analytics Summary
- **Endpoint:** `GET /analytics/summary`
- **Description:** Retrieve overall KPIs (totals, averages, and min/max metrics) for dashboard rendering.
- **Success Response (200 OK):**
  ```json
  {
    "total_entries": 150,
    "total_amount": 187500.0,
    "average_amount": 1250.0,
    "highest_amount": 50000.0,
    "lowest_amount": 100.0
  }
  ```

---

## 4. Error Handling and Resilience
The API standardizes errors to aid client debugging:

- **400 Bad Request:** Missing parameters or query format error.
- **404 Not Found:** Resource not found (e.g. invalid document ID).
- **409 Conflict:** Document ID already exists (integrity constraint violation).
- **422 Unprocessable Entity:** Schema validation error (e.g. invalid date format, string instead of float for amount).

### Sample Error Response (409 Conflict)
```json
{
  "detail": "Document ID 'JE1001' already exists."
}
```
