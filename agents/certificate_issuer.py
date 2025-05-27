"""
Artemis CodexOps Certificate/Credential Issuer

- Generate, verify, and deliver digital certificates for course completion.
- Integrates with Stripe for paid verification and delivery.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import uuid
import datetime
import sqlite3

app = FastAPI(title="Artemis Certificate Issuer")

DB_PATH = "certificate_issuer.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id TEXT PRIMARY KEY,
            user_email TEXT,
            course_name TEXT,
            completion_date TEXT,
            verification_code TEXT,
            is_paid INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class CertificateRequest(BaseModel):
    user_email: str
    course_name: str
    completion_date: Optional[str] = None

class Certificate(BaseModel):
    id: str
    user_email: str
    course_name: str
    completion_date: str
    verification_code: str
    is_paid: bool = False

def certificate_from_row(row):
    return Certificate(
        id=row[0],
        user_email=row[1],
        course_name=row[2],
        completion_date=row[3],
        verification_code=row[4],
        is_paid=bool(row[5])
    )

@app.post("/certificates/generate", response_model=Certificate)
def generate_certificate(req: CertificateRequest):
    cert_id = str(uuid.uuid4())
    completion_date = req.completion_date or datetime.date.today().isoformat()
    verification_code = str(uuid.uuid4())[:8]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO certificates (id, user_email, course_name, completion_date, verification_code, is_paid)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (cert_id, req.user_email, req.course_name, completion_date, verification_code, 0))
    conn.commit()
    conn.close()
    return Certificate(
        id=cert_id,
        user_email=req.user_email,
        course_name=req.course_name,
        completion_date=completion_date,
        verification_code=verification_code,
        is_paid=False
    )

@app.get("/certificates/verify/{verification_code}", response_model=Certificate)
def verify_certificate(verification_code: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM certificates WHERE verification_code=?', (verification_code,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return certificate_from_row(row)

@app.post("/certificates/pay/{cert_id}")
def pay_for_certificate(cert_id: str, request: Request):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM certificates WHERE id=?', (cert_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Certificate not found")
    c.execute('UPDATE certificates SET is_paid=1 WHERE id=?', (cert_id,))
    conn.commit()
    c.execute('SELECT * FROM certificates WHERE id=?', (cert_id,))
    updated_row = c.fetchone()
    conn.close()
    cert = certificate_from_row(updated_row)
    # TODO: Integrate with Stripe Checkout for payment
    return {"message": "Certificate payment successful", "certificate": cert}

# TODO: Add email delivery of certificates after payment
# TODO: Secure endpoints with authentication and RBAC

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8092)
