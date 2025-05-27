"""
Artemis CodexOps Automated Billing and Invoicing

- Centralize all payment flows.
- Automate invoice generation and delivery.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import uuid
import datetime
import sqlite3

app = FastAPI(title="Artemis Billing & Invoicing")

DB_PATH = "billing_invoicing.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id TEXT PRIMARY KEY,
            user_email TEXT,
            amount_usd REAL,
            description TEXT,
            issued_date TEXT,
            due_date TEXT,
            is_paid INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class Invoice(BaseModel):
    id: str
    user_email: str
    amount_usd: float
    description: str
    issued_date: str
    due_date: str
    is_paid: bool = False

@app.post("/invoices/create", response_model=Invoice)
def create_invoice(user_email: str, amount_usd: float, description: str, due_days: int = 7):
    invoice_id = str(uuid.uuid4())
    issued_date = datetime.date.today().isoformat()
    due_date = (datetime.date.today() + datetime.timedelta(days=due_days)).isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO invoices (id, user_email, amount_usd, description, issued_date, due_date, is_paid)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (invoice_id, user_email, amount_usd, description, issued_date, due_date, 0))
    conn.commit()
    conn.close()
    return Invoice(
        id=invoice_id,
        user_email=user_email,
        amount_usd=amount_usd,
        description=description,
        issued_date=issued_date,
        due_date=due_date,
        is_paid=False
    )

@app.get("/invoices/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, user_email, amount_usd, description, issued_date, due_date, is_paid FROM invoices WHERE id=?', (invoice_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return Invoice(
        id=row[0],
        user_email=row[1],
        amount_usd=row[2],
        description=row[3],
        issued_date=row[4],
        due_date=row[5],
        is_paid=bool(row[6])
    )

@app.post("/invoices/pay/{invoice_id}")
def pay_invoice(invoice_id: str, request: Request):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM invoices WHERE id=?', (invoice_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Invoice not found")
    c.execute('UPDATE invoices SET is_paid=1 WHERE id=?', (invoice_id,))
    conn.commit()
    c.execute('SELECT id, user_email, amount_usd, description, issued_date, due_date, is_paid FROM invoices WHERE id=?', (invoice_id,))
    updated_row = c.fetchone()
    conn.close()
    invoice = Invoice(
        id=updated_row[0],
        user_email=updated_row[1],
        amount_usd=updated_row[2],
        description=updated_row[3],
        issued_date=updated_row[4],
        due_date=updated_row[5],
        is_paid=bool(updated_row[6])
    )
    # TODO: Integrate with Stripe for payment
    return {"message": "Invoice paid successfully", "invoice": invoice}

@app.get("/invoices/user/{user_email}", response_model=List[Invoice])
def list_user_invoices(user_email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, user_email, amount_usd, description, issued_date, due_date, is_paid FROM invoices WHERE user_email=?', (user_email,))
    rows = c.fetchall()
    conn.close()
    return [
        Invoice(
            id=row[0],
            user_email=row[1],
            amount_usd=row[2],
            description=row[3],
            issued_date=row[4],
            due_date=row[5],
            is_paid=bool(row[6])
        ) for row in rows
    ]

# TODO: Add recurring billing, PDF generation, and reporting
# TODO: Secure endpoints with authentication and RBAC

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8096)
