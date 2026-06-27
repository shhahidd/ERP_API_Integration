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