# CHANGELOG

All notable changes to the ERP API Integration project are documented in this file, organized by the 15-day project methodology.

---

## [Day 15] - 2026-07-04
### Added
- Finished all project deliverables and naming alignments.
- Created final presentation slides at [D6_Final_Presentation_v1.0.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/presentation/D6_Final_Presentation_v1.0.md).
- Completed repository clean-up (removing nested python directory, configuring root `venv`).

---

## [Day 12-14] - 2026-07-01 to 2026-07-03
### Added
- Created stakeholder communication memos at [D6_Stakeholder_Communication_v1.0.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/docs/D6_Stakeholder_Communication_v1.0.md).
- Created QA test plan containing 20+ functional/non-functional test cases at [TST_Functional_001.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/docs/TST_Functional_001.md).
- Developed zero-downtime blue-green deployment instructions at [D6_Deployment_Runbook_v1.0.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/D6_Deployment_Runbook_v1.0.md).

---

## [Day 9-11] - 2026-06-28 to 2026-06-30
### Added
- Specified the resilience and error handling framework at [D5_Resilience_v1.0.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/D5_Resilience_v1.0.md).
- Defined retry formulas with exponential backoff and circuit breaker parameters.
- Designed 12+ dashboard panels and 15+ Prometheus alerting rules.

---

## [Day 6-8] - 2026-06-25 to 2026-06-27
### Added
- Generated the field mapping specification at [MAP_JournalEntry_v1.0.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/MAP_JournalEntry_v1.0.md) showing 50+ mapped elements from SAP S/4HANA (ACDOCA table) to FinSight.
- Implemented 25+ data quality validation rules (Null check, range validation, currency matching).
- Refactored `database.py` to support transactional query parameter filtering.

---

## [Day 3-5] - 2026-06-22 to 2026-06-24
### Added
- Created OpenAPI 3.0 specs for both extraction and ingestion components:
  - [API_SAP_JournalEntry.yaml](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/api/API_SAP_JournalEntry.yaml)
  - [API_FinSight_JournalEntry.yaml](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/api/API_FinSight_JournalEntry.yaml)
- Mapped all routes into the [Postman_Collection.json](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/api/Postman_Collection.json).
- Authored [D3_API_Documentation_v1.0.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/D3_API_Documentation_v1.0.md).

---

## [Day 2] - 2026-06-21
### Added
- Renamed and formatted C4 diagram files:
  - [DGM_C4_SystemContext.drawio](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/diagrams/DGM_C4_SystemContext.drawio) (Level 1)
  - [DGM_C4_Container.drawio](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/diagrams/DGM_C4_Container.drawio) (Level 2)
  - [DGM_C4_Component.drawio](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/diagrams/DGM_C4_Component.drawio) (Level 3)
- Compiled architecture and NFR specifications at [D2_Architecture_v1.0.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/D2_Architecture_v1.0.md).

---

## [Day 1] - 2026-06-20
### Added
- Configured project initial repository and branch structure.
- Drafted initial requirements and stakeholder matrices at [D1_Requirements_v1.0.md](file:///c:/Users/ShahidPatel/Downloads/ERP_API_Integration/D1_Requirements_v1.0.md).
