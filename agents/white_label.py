"""
Artemis CodexOps White-Label Platform Licensing

- Automate provisioning and branding for B2B clients.
- License management and support automation.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import uuid
import sqlite3

app = FastAPI(title="Artemis White-Label Licensing")

DB_PATH = "white_label.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            company_name TEXT,
            contact_email TEXT,
            license_key TEXT,
            branding_url TEXT,
            is_active INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class Client(BaseModel):
    id: str
    company_name: str
    contact_email: str
    license_key: str
    branding_url: Optional[str] = None
    is_active: bool = True

@app.post("/clients/register", response_model=Client)
def register_client(company_name: str, contact_email: str, branding_url: Optional[str] = None):
    client_id = str(uuid.uuid4())
    license_key = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO clients (id, company_name, contact_email, license_key, branding_url, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (client_id, company_name, contact_email, license_key, branding_url, 1))
    conn.commit()
    conn.close()
    return Client(
        id=client_id,
        company_name=company_name,
        contact_email=contact_email,
        license_key=license_key,
        branding_url=branding_url,
        is_active=True
    )

@app.get("/clients/{client_id}", response_model=Client)
def get_client(client_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, company_name, contact_email, license_key, branding_url, is_active FROM clients WHERE id=?', (client_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Client not found")
    return Client(
        id=row[0],
        company_name=row[1],
        contact_email=row[2],
        license_key=row[3],
        branding_url=row[4],
        is_active=bool(row[5])
    )

@app.post("/clients/{client_id}/deactivate")
def deactivate_client(client_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM clients WHERE id=?', (client_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Client not found")
    c.execute('UPDATE clients SET is_active=0 WHERE id=?', (client_id,))
    conn.commit()
    c.execute('SELECT id, company_name, contact_email, license_key, branding_url, is_active FROM clients WHERE id=?', (client_id,))
    updated_row = c.fetchone()
    conn.close()
    client = Client(
        id=updated_row[0],
        company_name=updated_row[1],
        contact_email=updated_row[2],
        license_key=updated_row[3],
        branding_url=updated_row[4],
        is_active=bool(updated_row[5])
    )
    return {"message": "Client deactivated", "client": client}

# TODO: Add endpoints for license renewal, support, and analytics
# TODO: Secure endpoints with authentication and RBAC

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8095)
