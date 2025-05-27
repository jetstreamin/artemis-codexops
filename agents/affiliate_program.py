"""
Artemis CodexOps Affiliate Program

- Register, track, and payout affiliates for referrals.
- Automates referral tracking and earnings dashboard.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import uuid
import sqlite3

app = FastAPI(title="Artemis Affiliate Program")

DB_PATH = "affiliate_program.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS affiliates (
            id TEXT PRIMARY KEY,
            email TEXT,
            referral_code TEXT,
            earnings_usd REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id TEXT PRIMARY KEY,
            affiliate_id TEXT,
            referred_email TEXT,
            amount_usd REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class Affiliate(BaseModel):
    id: str
    email: str
    referral_code: str
    earnings_usd: float = 0.0

class Referral(BaseModel):
    affiliate_id: str
    referred_email: str
    amount_usd: float

@app.post("/affiliates/register", response_model=Affiliate)
def register_affiliate(email: str):
    affiliate_id = str(uuid.uuid4())
    referral_code = str(uuid.uuid4())[:8]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO affiliates (id, email, referral_code, earnings_usd)
        VALUES (?, ?, ?, ?)
    ''', (affiliate_id, email, referral_code, 0.0))
    conn.commit()
    conn.close()
    return Affiliate(
        id=affiliate_id,
        email=email,
        referral_code=referral_code,
        earnings_usd=0.0
    )

@app.post("/affiliates/track_referral")
def track_referral(referral_code: str, referred_email: str, amount_usd: float):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, earnings_usd FROM affiliates WHERE referral_code=?', (referral_code,))
    row = c.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Affiliate not found")
    affiliate_id, earnings_usd = row
    new_earnings = earnings_usd + amount_usd
    c.execute('UPDATE affiliates SET earnings_usd=? WHERE id=?', (new_earnings, affiliate_id))
    referral_id = str(uuid.uuid4())
    c.execute('''
        INSERT INTO referrals (id, affiliate_id, referred_email, amount_usd)
        VALUES (?, ?, ?, ?)
    ''', (referral_id, affiliate_id, referred_email, amount_usd))
    conn.commit()
    c.execute('SELECT id, email, referral_code, earnings_usd FROM affiliates WHERE id=?', (affiliate_id,))
    aff_row = c.fetchone()
    conn.close()
    affiliate = Affiliate(
        id=aff_row[0],
        email=aff_row[1],
        referral_code=aff_row[2],
        earnings_usd=aff_row[3]
    )
    # TODO: Automate payout via Stripe or PayPal
    return {"message": "Referral tracked", "affiliate": affiliate}

@app.get("/affiliates/{affiliate_id}/dashboard", response_model=Affiliate)
def affiliate_dashboard(affiliate_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, email, referral_code, earnings_usd FROM affiliates WHERE id=?', (affiliate_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    return Affiliate(
        id=row[0],
        email=row[1],
        referral_code=row[2],
        earnings_usd=row[3]
    )

@app.get("/affiliates/{affiliate_id}/referrals", response_model=List[Referral])
def list_referrals(affiliate_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT affiliate_id, referred_email, amount_usd FROM referrals WHERE affiliate_id=?', (affiliate_id,))
    rows = c.fetchall()
    conn.close()
    return [Referral(affiliate_id=row[0], referred_email=row[1], amount_usd=row[2]) for row in rows]

# TODO: Add payout automation and reporting
# TODO: Secure endpoints with authentication

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093)
