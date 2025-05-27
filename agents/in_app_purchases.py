"""
Artemis CodexOps In-App Purchases for Advanced Analytics/Reports

- Upsell advanced analytics and reporting features to power users.
- Integrate with Stripe for one-click purchases.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import uuid
import sqlite3

app = FastAPI(title="Artemis In-App Purchases")

DB_PATH = "in_app_purchases.db"

REPORTS = {
    "analytics_1": "Advanced Analytics Report 1",
    "analytics_2": "Advanced Analytics Report 2"
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id TEXT PRIMARY KEY,
            user_email TEXT,
            report_id TEXT,
            is_paid INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class Purchase(BaseModel):
    id: str
    user_email: str
    report_id: str
    is_paid: bool = False

@app.post("/purchase", response_model=Purchase)
def purchase_report(user_email: str, report_id: str):
    if report_id not in REPORTS:
        raise HTTPException(status_code=404, detail="Report not found")
    purchase_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO purchases (id, user_email, report_id, is_paid)
        VALUES (?, ?, ?, ?)
    ''', (purchase_id, user_email, report_id, 1))
    conn.commit()
    conn.close()
    return Purchase(
        id=purchase_id,
        user_email=user_email,
        report_id=report_id,
        is_paid=True
    )

@app.get("/reports/{report_id}")
def get_report(report_id: str, user_email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM purchases WHERE report_id=? AND user_email=? AND is_paid=1', (report_id, user_email))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=403, detail="Report not purchased")
    return {"report_id": report_id, "content": REPORTS[report_id]}

@app.get("/purchases/user/{user_email}", response_model=List[Purchase])
def list_user_purchases(user_email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, user_email, report_id, is_paid FROM purchases WHERE user_email=?', (user_email,))
    rows = c.fetchall()
    conn.close()
    return [
        Purchase(
            id=row[0],
            user_email=row[1],
            report_id=row[2],
            is_paid=bool(row[3])
        ) for row in rows
    ]

# TODO: Add more analytics/report types and dynamic pricing
# TODO: Secure endpoints with authentication and RBAC

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8098)
