# D5: Resilience, Reconciliation & Monitoring Document

**Version:** 1.0.0  
**Project:** Custom API Integration (SAP S/4HANA to Zetheta FinSight)  
**Client:** Meridian Manufacturing Ltd.

---

## 1. Resilience & Error Handling Framework
To withstand network glitches, API rate-limiting, and server failures, the integration pipeline implements the following patterns:

- **Exponential Backoff with Jitter:**
  When a transmission fails, the loader retries using a randomized delay formula to prevent thundering herd problems on the receiving API:
  $$\text{wait} = \min\left(120, \text{random}(1, 2) \times 2^{\text{attempt}}\right) \text{ seconds}$$
- **Circuit Breaker:**
  Transitions to **Open** state if 5 consecutive calls fail. During open state, calls to FinSight are immediately queued locally in SQLite, avoiding network overhead. After 30 seconds, it transitions to **Half-Open** to test recovery with a single query.
- **Bulkhead Isolation:**
  Allocates dedicated thread pools and DB connection limits per data category. If the AP (Accounts Payable) queue blocks due to high volume, it will not disrupt GL (General Ledger) postings.
- **Timeout Limits:**
  Enforce strict timeout bounds on connections:
  - SAP gateway extraction calls: Max 10 seconds.
  - FinSight API payloads loading: Max 5 seconds.
  - Local SQLite operations: Timeout 10 seconds.

---

## 2. Reconciliation Specification
To prove data integrity across the pipeline (source ERP to destination FinSight), a daily automated reconciliation service runs at 05:00 IST (after the SAP batch window closed):

- **Control Totals Check:**
  $$\sum \text{Amount (Source)} = \sum \text{Amount (Destination)}$$
- **Uniqueness Check:**
  Verify 100% uniqueness of `document_id` in destination platform.
- **Data Completeness Check:**
  Flag any entries where mandatory fields (Company Code, Account, Amount) are missing.
- **Mismatch Mitigation:**
  If a balance break is detected, the service automatically halts synchronization, creates a reconciliation break ticket, and emails the Audit team.

---

## 3. Monitoring Dashboard Specification (12+ Panels in Grafana)
The system exposes metrics that map to Grafana visualization panels:

1. **Extraction Throughput (records/sec):** Real-time counter of pulled SAP journal lines.
2. **Gateway API Latency (ms):** P50, P95, P99 request duration metrics.
3. **Database Health State:** Online/Offline indicator of SQLite cache.
4. **Active RFC Pools:** Number of busy SAP network connections (out of 50).
5. **Loading Error Rate (%):** Ratio of failed payloads to FinSight.
6. **Queue Depth:** Number of journal entries cached locally waiting for sync.
7. **Reconciliation Status:** Green (Balanced), Red (Break detected) dashboard panel.
8. **Network Bandwidth (Mbps):** Real-time monitoring of plant network utilization.
9. **Circuit Breaker Status:** Closed, Open, Half-Open states.
10. **GST Compliance Validation Rate:** Percentage of records passing local GST calculation checks.
11. **System Resource Usage:** CPU & Memory stats of FastAPI host.
12. **Slow Query Monitor:** Lists queries executing > 500ms.

---

## 4. Observability Alerting Rules (15+ Rules)

| Rule ID | Metric Monitored | Trigger Threshold | Severity | Alert Action |
|---------|------------------|-------------------|----------|--------------|
| **ALT-001** | Gateway latency | P95 > 2.0s for 5 mins | Warning | Ops Slack Notification |
| **ALT-002** | Gateway error rate | > 2% for 3 mins | High | Ops PagerDuty Alert |
| **ALT-003** | Local Queue size | > 10,000 entries | High | PagerDuty (Possible sync block) |
| **ALT-004** | Active RFC connections | > 45 (out of 50 limit)| Warning | Log warnings, slow throttling |
| **ALT-005** | Circuit Breaker state | State == OPEN | High | Email Platform Lead |
| **ALT-006** | Reconciliation balance | Net Difference != 0.00 | Critical | Email Audit team & halt sync |
| **ALT-007** | Network bandwidth | > 112.5Mbps (25% limit)| Warning | Rate limit sync throughput |
| **ALT-008** | CPU utilization | > 85% for 10 mins | Warning | Ops slack warning |
| **ALT-009** | Memory utilization | > 90% for 5 mins | High | Restart API container |
| **ALT-010** | Database file access | SQLite lock timeout > 10s| High | Alert DB administrator |
| **ALT-011** | Dead Letter Queue | DLQ size > 0 | Warning | Log trace and alert support |
| **ALT-012** | Extraction Frequency | Sync delay > 45 mins | High | Notify VP of IT |
| **ALT-013** | GST Mismatches | Mismatch count > 0 | High | Email Tax compliance team |
| **ALT-014** | Process Crash | API service offline | Critical | Auto-restart & PagerDuty |
| **ALT-015** | Unauthorized request | > 10 failed login attempts| High | Ban client IP & alert SecOps |
