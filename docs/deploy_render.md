# Deploy Artemis CodexOps to Render.com (Best Free Choice)

This guide will get your Artemis CodexOps backend live on Render.com with free-tier FastAPI and Postgres, accessible globally.

---

## 1. Prepare Your Repo

- Ensure all FastAPI services (e.g., agents/plugin_marketplace.py) have a `main` entrypoint (e.g., `app = FastAPI(...)`).
- Requirements: Python 3.11+, FastAPI, Uvicorn, SQLite or Postgres support.

## 2. Create a New Web Service on Render

- Go to [Render.com](https://render.com) and sign up (free).
- Click "New Web Service" > "Connect your GitHub repo".
- Select your Artemis CodexOps repo.

### Service Settings

- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn agents/plugin_marketplace:app --host 0.0.0.0 --port 10000`
  - (Change to the correct agent for each service, e.g., `agents/api_billing:app`)
- **Instance Type:** Free

## 3. Add a Free Postgres Database

- In Render, click "New Database" > "PostgreSQL".
- Name: `codexops`
- Copy the database URL and add it as an environment variable: `DATABASE_URL`

## 4. Set Environment Variables

- `DATABASE_URL` (from Render Postgres)
- Any other secrets (e.g., JWT secret, Stripe keys)

## 5. Repeat for Each Service

- Deploy each FastAPI microservice as a separate Render web service (e.g., plugin marketplace, billing, auth, etc.).
- Use different ports (e.g., 10000, 10001, ...).

## 6. Update Web UIs

- Update all fetch URLs in web/ to point to the new Render service URLs (e.g., `https://plugin-marketplace-xxxx.onrender.com/plugins`).
- Redeploy static web assets to GitHub Pages.

## 7. Validate

- Visit each Render service URL and ensure the API is live (should return 200 OK on `/docs`).
- Test all web UIs for end-to-end functionality.

## 8. Publish

- Add all live URLs to the README and docs.
- Announce the live deployment to your community.

---

**Note:**  
- Render free tier sleeps after 15 minutes of inactivity, but wakes on request.
- For higher uptime, upgrade to the paid tier or use Railway/Fly.io as a backup.

_Last updated: 2025-05-26_
