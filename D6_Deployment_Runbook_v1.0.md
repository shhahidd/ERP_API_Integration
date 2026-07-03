# D6: Production Deployment Runbook

**Version:** 1.0.0  
**Project:** Custom API Integration (SAP S/4HANA to Zetheta FinSight)  
**Client:** Meridian Manufacturing Ltd.

---

## 1. Scope and Deployment Strategy
This runbook covers the rollout of the Integration Gateway. The release uses a **Blue-Green Deployment** pattern to guarantee zero downtime and immediate rollback capability.

- **Blue Environment:** Current active production environment.
- **Green Environment:** New candidate release environment.

```
                  +---------------+
                  |  Load Balancer|
                  +---------------+
                     /          \
      Active (100%) /            \ Inactive (0%)
                   v              v
            +------------+  +------------+
            |  Blue Env  |  |  Green Env |
            |  (v1.0.0)  |  |  (v1.0.1)  |
            +------------+  +------------+
```

## 2. Pre-Deployment Checks (T-30 Minutes)
1. Verify system status page shows no ongoing outages on SAP Gateway or AWS network.
2. Confirm the nightly SAP batch window `RGGBS000` is NOT active (Avoid deployment between 01:00-04:30 IST).
3. Validate that current database lock counts are zero.
4. Take a backup of the current production SQLite database:
   ```bash
   cp erp.db backup_erp_$(date +%F).db
   ```

## 3. Database Migration (Expand-Contract Pattern)
For schema changes, we use the Expand-Contract pattern to keep environments backward-compatible.

1. **Expand Phase:** Add new fields (nullable or with defaults) to the DB schema so both old and new code can read/write without crashing.
2. **Contract Phase:** Once the new code is fully active, drop the old columns or apply constraints if necessary.

## 4. Execution Step-by-Step

### Step 4.1: Deploy to Green Environment
Deploy the FastAPI code and spin up the Green container instance:
```bash
# Clone and build the green target
git clone -b main https://github.com/shhahidd/ERP_API_Integration.git green-env
cd green-env
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

### Step 4.2: Execute Automated Smoke Tests (T-0)
Verify the green build works correctly on port 8001:
```bash
# Verify health check endpoint returns 200 OK
curl -I http://127.0.0.1:8001/health
```

### Step 4.3: Switch Traffic (T+5 Minutes)
Update the load balancer routing rules to route traffic from Blue (port 8000) to Green (port 8001):
```bash
# Route public traffic to green port
netsh interface portproxy update v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8001 connectaddress=127.0.0.1
```

---

## 5. Rollback Strategy (If Smoke Tests Fail)
If any post-deployment anomalies or latency increases (ALT-001) are triggered within 15 minutes of traffic switch, execute rollback immediately:

1. **Re-route Traffic to Blue:**
   Switch the load balancer port proxy back to the active Blue instance:
   ```bash
   netsh interface portproxy update v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=127.0.0.1
   ```
2. **Shutdown Green Environment:**
   Stop the green environment uvicorn service to release ports.
3. **Restore DB State:**
   If database write issues occurred, restore from the pre-deployment backup:
   ```bash
   cp backup_erp_YYYY-MM-DD.db erp.db
   ```
4. Log the incident in the system maintenance journal. Maximum target rollback time: **5 minutes**.
