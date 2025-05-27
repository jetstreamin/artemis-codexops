"""
Artemis CodexOps Affiliate Program

- Register, track, and payout affiliates for referrals.
- Automates referral tracking and earnings dashboard.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import uuid

app = FastAPI(title="Artemis Affiliate Program")

# In-memory store for demo; replace with DB in production
AFFILIATES = {}
REFERRALS = []

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
    affiliate = Affiliate(
        id=affiliate_id,
        email=email,
        referral_code=referral_code,
        earnings_usd=0.0
    )
    AFFILIATES[affiliate_id] = affiliate
    return affiliate

@app.post("/affiliates/track_referral")
def track_referral(referral_code: str, referred_email: str, amount_usd: float):
    affiliate = next((a for a in AFFILIATES.values() if a.referral_code == referral_code), None)
    if not affiliate:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    affiliate.earnings_usd += amount_usd
    referral = Referral(
        affiliate_id=affiliate.id,
        referred_email=referred_email,
        amount_usd=amount_usd
    )
    REFERRALS.append(referral)
    # TODO: Automate payout via Stripe or PayPal
    return {"message": "Referral tracked", "affiliate": affiliate}

@app.get("/affiliates/{affiliate_id}/dashboard", response_model=Affiliate)
def affiliate_dashboard(affiliate_id: str):
    affiliate = AFFILIATES.get(affiliate_id)
    if not affiliate:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    return affiliate

@app.get("/affiliates/{affiliate_id}/referrals", response_model=List[Referral])
def list_referrals(affiliate_id: str):
    return [r for r in REFERRALS if r.affiliate_id == affiliate_id]

# TODO: Add payout automation and reporting
# TODO: Secure endpoints with authentication

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093)
