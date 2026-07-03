import sqlite3

DATABASE = "erp.db"


def create_database():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            document_id TEXT PRIMARY KEY,
            company_code TEXT,
            account TEXT,
            amount REAL,
            currency TEXT,
            posting_date TEXT
        )
        """)


def insert_journal_entry(entry):
    with sqlite3.connect(DATABASE, timeout=10) as connection:
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO journal_entries
        (document_id, company_code, account, amount, currency, posting_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry.document_id,
            entry.company_code,
            entry.account,
            entry.amount,
            entry.currency,
            str(entry.posting_date)
        ))


def get_all_entries():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM journal_entries")

        rows = cursor.fetchall()

        return [dict(row) for row in rows]
    
def delete_journal_entry(document_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM journal_entries WHERE document_id = ?",
            (document_id,)
        )

        deleted = cursor.rowcount

    return deleted

def update_journal_entry(document_id, entry):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE journal_entries
        SET company_code = ?,
            account = ?,
            amount = ?,
            currency = ?,
            posting_date = ?
        WHERE document_id = ?
        """, (
            entry.company_code,
            entry.account,
            entry.amount,
            entry.currency,
            str(entry.posting_date),
            document_id
        ))

        updated = cursor.rowcount

    return updated

def get_journal_entry(document_id):
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM journal_entries WHERE document_id = ?",
            (document_id,)
        )

        row = cursor.fetchone()

        if row:
            return dict(row)

        return None

def get_entries(
    company_code=None,
    currency=None,
    account=None,
    start_date=None,
    end_date=None,
    sort_by=None,
    order="asc",
    limit=None,
    offset=0
):
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = "SELECT * FROM journal_entries"
        parameters = []
        conditions = []

        allowed_columns = [
            "document_id",
            "company_code",
            "account",
            "amount",
            "currency",
            "posting_date"
        ]

        if company_code:
            conditions.append("company_code = ?")
            parameters.append(company_code)

        if currency:
            conditions.append("currency = ?")
            parameters.append(currency)

        if account:
            conditions.append("account = ?")
            parameters.append(account)

        if start_date:
            conditions.append("posting_date >= ?")
            parameters.append(start_date)

        if end_date:
            conditions.append("posting_date <= ?")
            parameters.append(end_date)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if sort_by:
            if sort_by not in allowed_columns:
                sort_by = "document_id"

            if order.lower() not in ["asc", "desc"]:
                order = "asc"

            query += f" ORDER BY {sort_by} {order.upper()}"

        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            parameters.extend([limit, offset])

        cursor.execute(query, parameters)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]
    
def get_summary():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT
            COUNT(*),
            SUM(amount),
            AVG(amount),
            MAX(amount),
            MIN(amount)
        FROM journal_entries
        """)

        row = cursor.fetchone()

        return {
            "total_entries": row[0],
            "total_amount": row[1],
            "average_amount": row[2],
            "highest_amount": row[3],
            "lowest_amount": row[4]
        }
    
def get_company_summary():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("""
        SELECT
            company_code,
            COUNT(*) AS entries,
            SUM(amount) AS total_amount
        FROM journal_entries
        GROUP BY company_code
        ORDER BY company_code
        """)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

def search_entries(query):
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        search = f"%{query}%"

        cursor.execute("""
        SELECT *
        FROM journal_entries
        WHERE document_id LIKE ?
           OR company_code LIKE ?
           OR account LIKE ?
           OR currency LIKE ?
        """, (
            search,
            search,
            search,
            search
        ))

        rows = cursor.fetchall()

        return [dict(row) for row in rows]