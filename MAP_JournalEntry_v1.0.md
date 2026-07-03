# MAP: Journal Entry Mapping & Data Quality Specification

**Version:** 1.0.0  
**Project:** Custom API Integration (SAP S/4HANA to Zetheta FinSight)  
**Client:** Meridian Manufacturing Ltd.

---

## 1. Field Mapping (50+ Fields mapped across ACDOCA and FinSight)
Below is the direct mapping of SAP S/4HANA Universal Journal (ACDOCA) fields to the destination Financial Analytics (FinSight) schema.

| # | SAP ACDOCA Field | SAP Data Type | FinSight Field | Target Data Type | Transformation Logic / Business Rules |
|---|------------------|---------------|----------------|------------------|---------------------------------------|
| 1 | `RCLNT` | CHAR(3) | `client_id` | STRING | Pass-through (e.g. '800') |
| 2 | `RLDNR` | CHAR(2) | `ledger_id` | STRING | Target default is '0L' (Leading Ledger) |
| 3 | `RBUKRS` | CHAR(4) | `company_code` | STRING | Map company codes MC01, MC02, MC03 |
| 4 | `GJAHR` | NUMC(4) | `fiscal_year` | INT | Pass-through fiscal year |
| 5 | `BELNR` | CHAR(10)| `document_id` | STRING | Pass-through (e.g., '1000000001') |
| 6 | `DOCLN` | CHAR(6) | `line_item_id` | STRING | Auto-generated index '001', '002' etc. |
| 7 | `BLART` | CHAR(2) | `document_type`| STRING | Maps journal entry classifications |
| 8 | `BUDAT` | DATS(8) | `posting_date` | DATE | Map DATS YYYYMMDD to ISO YYYY-MM-DD |
| 9 | `BLDAT` | DATS(8) | `document_date`| DATE | Map document date to ISO format |
| 10| `MONAT` | NUMC(2) | `posting_period`| INT | Map SAP posting period (1-12, 13-16) |
| 11| `USNAM` | CHAR(12)| `created_by` | STRING | Map user login to analytical account owner |
| 12| `HKONT` | CHAR(10)| `account_number`| STRING | Map GL Account mapping (Schedule III format) |
| 13| `TSL` | CURR(23,2)| `amount` | DECIMAL | Map raw ledger transaction amount |
| 14| `RWCUR` | CUKY(5) | `currency` | STRING | Convert transaction currency ISO code |
| 15| `HSL` | CURR(23,2)| `amount_inr` | DECIMAL | INR translation at posting day exchange rate |
| 16| `KOSAR` | CHAR(1) | `cost_center_type`|STRING | Flatten cost center categories |
| 17| `KOSTL` | CHAR(10)| `cost_center` | STRING | Cost Center ID flattened for analytics |
| 18| `LTEXT` | CHAR(40)| `cost_center_desc`|STRING| Enrich with Cost Center master name |
| 19| `PRCTR` | CHAR(10)| `profit_center` | STRING | Profit Center ID |
| 20| `SEGMENT`| CHAR(10)| `segment_id` | STRING | Segment reporting categorization |
| 21| `SGTXT` | CHAR(50)| `line_description`|STRING| General line narration text |
| 22| `KTOPL` | CHAR(4) | `chart_of_accounts`|STRING| Map to local Chart of Accounts (schedule III) |
| 23| `GSBER` | CHAR(4) | `business_area`| STRING | Geographic plant business area mapping |
| 24| `WERKS` | CHAR(4) | `plant_code` | STRING | Link line item to manufacturing plant code |
| 25| `MATNR` | CHAR(40)| `material_number`|STRING| For direct stock consumption transactions |
| 26| `MENGE` | QUAN(13,3)| `quantity` | DECIMAL | Inventory consumed units |
| 27| `MEINS` | UNIT(3) | `unit_of_measure`|STRING| Base unit of measure |
| 28| `MWSKZ` | CHAR(2) | `tax_code` | STRING | GST tax code classification |
| 29| `TXBHW` | CURR(13,2)| `tax_base_amount`|DECIMAL| Tax base calculation |
| 30| `CGST_AMT`|CURR(13,2)| `cgst_amount` | DECIMAL | CGST breakdown for Indian taxation |
| 31| `SGST_AMT`|CURR(13,2)| `sgst_amount` | DECIMAL | SGST breakdown for Indian taxation |
| 32| `IGST_AMT`|CURR(13,2)| `igst_amount` | DECIMAL | IGST breakdown for Indian taxation |
| 33| `VALUT` | DATS(8) | `value_date` | DATE | Value date for cash/bank postings |
| 34| `XBILK` | CHAR(1) | `is_balance_sheet`|BOOLEAN| Determine if Balance Sheet / P&L account |
| 35| `BSCHL` | CHAR(2) | `posting_key` | STRING | Debit/Credit sign key identifier |
| 36| `SHKZG` | CHAR(1) | `debit_credit_ind`|STRING| S (Debit) or H (Credit) validation indicator |
| 37| `REBZG` | CHAR(10)| `invoice_reference`|STRING| Invoice document linkage ID |
| 38| `AUGBL` | CHAR(10)| `clearing_document`|STRING| Clearing status matching index |
| 39| `AUGDT` | DATS(8) | `clearing_date`| DATE | ISO date format of invoice clearing |
| 40| `HBKID` | CHAR(5) | `house_bank_id`| STRING | Bank routing details |
| 41| `HKTID` | CHAR(5) | `account_id` | STRING | Bank account index identifier |
| 42| `BWTAR` | CHAR(10)| `valuation_type`| STRING | Inventory valuation method mapping |
| 43| `EBELN` | CHAR(10)| `purchase_order`| STRING | Purchase Order document reference |
| 44| `EBELP` | NUMC(5) | `po_line_item` | INT | Purchase Order item split line |
| 45| `VBUND` | CHAR(6) | `trading_partner`|STRING| Trading partner company for eliminations |
| 46| `ZUONR` | CHAR(18)| `assignment_number`|STRING| Assignment sorting key |
| 47| `AWTYP` | CHAR(5) | `reference_type`| STRING | Source document reference transaction type |
| 48| `AWREF` | CHAR(10)| `reference_document`|STRING| Link to sales billing or production order |
| 49| `VERSN` | CHAR(3) | `ledger_version`| STRING | Ledger reporting version |
| 50| `TIMESTAMP`|DECIMAL(15)| `extraction_timestamp`|INT| Epoch timestamp of ODP delta capture |

---

## 2. Data Quality & Validation Rules (25+ Rules)

The integration pipeline executes structural and semantic data quality checks at the gateway layer:

### Completeness Rules (Null Checks)
1. **VAL-001:** `document_id` must not be null or blank.
2. **VAL-002:** `company_code` must be present.
3. **VAL-003:** `account_number` must be populated.
4. **VAL-004:** `amount` must be a valid numeric type and present.
5. **VAL-005:** `posting_date` must not be null.

### Validity Rules (Form and Data Formats)
6. **VAL-006:** `posting_date` must conform to standard ISO-8601 (`YYYY-MM-DD`).
7. **VAL-007:** `amount` must be positive. Crediting or debiting direction is determined by standard signs.
8. **VAL-008:** `currency` must be a valid 3-character ISO-4217 code (INR, USD, EUR, GBP).
9. **VAL-009:** `company_code` must match active corporate entity codes (MC01, MC02, MC03).
10. **VAL-010:** `account_number` must be numeric and consist of exactly 6 digits.

### Consistency Rules (Domain Mapping)
11. **VAL-011:** If `currency` is "INR", CGST/SGST/IGST breakdown check is executed.
12. **VAL-012:** Posting date must map to a valid fiscal year period (Variant V3 - Indian April-March).
13. **VAL-013:** Cost Center must map to a valid regional code structure (e.g. starting with `CC_`).
14. **VAL-014:** Profit Center must correspond to active plant profit codes.
15. **VAL-015:** Cross-entity entries must balance trading partner IDs (`VBUND` field).

### Double-Entry Integrity Rules (Reconciliation)
16. **VAL-016:** Net sum of debits and credits for a single Accounting Document (`BELNR`) must equal zero.
17. **VAL-017:** CGST and SGST must be equal for intra-state transactions.
18. **VAL-018:** IGST must be zero if CGST/SGST are positive.
19. **VAL-019:** Total document balance in local currency must equal document balance in transaction currency after conversion.
20. **VAL-020:** Invoice line item reference `REBZG` must exist for payments.

### Unique/System Rules
21. **VAL-021:** `document_id` must be unique in the local database.
22. **VAL-022:** Line item index must increase sequentially.
23. **VAL-023:** System checks database connection status before entry creation.
24. **VAL-024:** Request payload must not exceed 10MB memory size.
25. **VAL-025:** Posting period (MONAT) must be in the range 1-16 (accounting adjustments period).
