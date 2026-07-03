# D1: Integration Requirements & Discovery Document

**Version:** 1.0.0  
**Project:** Custom API Integration (SAP S/4HANA to Zetheta FinSight)  
**Client:** Meridian Manufacturing Ltd.

---

## 1. Executive Summary
Meridian Manufacturing Ltd. operates seven plants across India, utilizing SAP S/4HANA as its core ERP. Currently, financial reporting is limited by a 24-hour batch delay, preventing the CFO from making real-time capital allocation and operational decisions. This document outlines the requirements for building a custom API integration service to sync journal entries from SAP to the Zetheta FinSight analytics platform.

## 2. Business Objectives
- **Real-Time Visibility:** Transition financial reporting from daily batches to near-real-time data sync.
- **Data Integrity:** Achieve 100% reconciliation accuracy between SAP ledger postings and analytics summaries.
- **Operational Continuity:** Ensure integration processes do not degrade performance on production ERP workloads.
- **Regulatory Compliance:** Adhere to RBI guidelines on domestic financial data residency and Company Law Schedule III layouts.

## 3. Stakeholder Matrix & Concerns

| Persona | Role | Primary Concern | Communication Style |
|---------|------|-----------------|---------------------|
| **Ananya Krishnan** | CFO | Dashboard freshness, reporting accuracy, ROI. | High-level business KPIs, no jargon. |
| **Rajesh Venkataraman** | VP of IT Infrastructure | Service stability, system load, security compliance. | Detailed service parameters, SLAs. |
| **Priya Deshmukh** | SAP Basis Administrator | RFC pool depletion, database locking during batch windows. | SAP transaction codes, Basis settings. |
| **Marcus Wei** | Zetheta Platform Engineer | API contract compliance, data validation, rate limits. | JSON schemas, OpenAPI standard, error codes. |
| **Dr. Sanjay Kulkarni** | Head of Internal Audit | Financial controls, reconciliation trail, audit logging. | Ledger matching, trace keys. |

## 4. Key Functional Requirements
- **FR1:** Continuous extraction of journal entry headers and line items from SAP via standard Gateway OData interfaces.
- **FR2:** Data validation and mapping from SAP's schema (ACDOCA table) to the FinSight JSON payload formats.
- **FR3:** Multi-company and multi-currency transactions aggregation and analytics summaries.
- **FR4:** Secure database storage (using SQLite prototype, migrating to PostgreSQL) to log transactions locally before transmission.
- **FR5:** Interactive API documentation via Swagger UI / ReDoc.
- **FR6:** On-demand CSV export of journal entry records.

## 5. Non-Functional Constraints

- **SAP Batch Window:** The nightly batch job `RGGBS000` runs 01:00-04:30 IST. Heavy data extraction is strictly prohibited during this window.
- **RFC Pool Limit:** Maximum 50 concurrent Remote Function Call (RFC) connections. Over-allocation will block critical dialog users.
- **Data Residency:** Financial data must be processed and stored entirely within the Indian AWS region (Mumbai, ap-south-1) to comply with RBI guidelines.
- **Bandwidth Cap:** Integration must not consume more than 25% of the shared 450Mbps MPLS plant network link during business hours (09:00-18:00 IST).
