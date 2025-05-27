"""
Artemis CodexOps Live Events and Webinars

- Enable paid live events and webinars with ticketing.
- Integrate with webinar platforms and automate ticket management.
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import uuid
import datetime
import sqlite3

app = FastAPI(title="Artemis Live Events")

DB_PATH = "live_events.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            start_time TEXT,
            end_time TEXT,
            price_usd REAL,
            webinar_url TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            event_id TEXT,
            user_email TEXT,
            purchase_time TEXT,
            is_paid INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class Event(BaseModel):
    id: str
    title: str
    description: str
    start_time: str
    end_time: str
    price_usd: float
    webinar_url: Optional[str] = None

class Ticket(BaseModel):
    id: str
    event_id: str
    user_email: str
    purchase_time: str
    is_paid: bool = False

@app.post("/events/create", response_model=Event)
def create_event(title: str, description: str, start_time: str, end_time: str, price_usd: float, webinar_url: Optional[str] = None):
    event_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (id, title, description, start_time, end_time, price_usd, webinar_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (event_id, title, description, start_time, end_time, price_usd, webinar_url))
    conn.commit()
    conn.close()
    return Event(
        id=event_id,
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time,
        price_usd=price_usd,
        webinar_url=webinar_url
    )

@app.get("/events", response_model=List[Event])
def list_events():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, title, description, start_time, end_time, price_usd, webinar_url FROM events')
    rows = c.fetchall()
    conn.close()
    return [
        Event(
            id=row[0],
            title=row[1],
            description=row[2],
            start_time=row[3],
            end_time=row[4],
            price_usd=row[5],
            webinar_url=row[6]
        ) for row in rows
    ]

@app.post("/tickets/purchase", response_model=Ticket)
def purchase_ticket(event_id: str, user_email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE id=?', (event_id,))
    event_row = c.fetchone()
    if not event_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Event not found")
    ticket_id = str(uuid.uuid4())
    purchase_time = datetime.datetime.now().isoformat()
    c.execute('''
        INSERT INTO tickets (id, event_id, user_email, purchase_time, is_paid)
        VALUES (?, ?, ?, ?, ?)
    ''', (ticket_id, event_id, user_email, purchase_time, 1))
    conn.commit()
    conn.close()
    return Ticket(
        id=ticket_id,
        event_id=event_id,
        user_email=user_email,
        purchase_time=purchase_time,
        is_paid=True
    )

@app.get("/tickets/user/{user_email}", response_model=List[Ticket])
def list_user_tickets(user_email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, event_id, user_email, purchase_time, is_paid FROM tickets WHERE user_email=?', (user_email,))
    rows = c.fetchall()
    conn.close()
    return [
        Ticket(
            id=row[0],
            event_id=row[1],
            user_email=row[2],
            purchase_time=row[3],
            is_paid=bool(row[4])
        ) for row in rows
    ]

# TODO: Integrate with webinar platforms (Zoom, Webex, etc.)
# TODO: Secure endpoints with authentication and RBAC

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8097)
