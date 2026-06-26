def transform_record(record):
    return {
        "documentId": record["document_id"],
        "tenantId": record["company_code"],
        "glAccount": record["account"],
        "amount": record["amount"],
        "currency": record["currency"],
        "postingDate": record["posting_date"]
    }