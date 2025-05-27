# Artemis CodexOps API Reference

Comprehensive API documentation for all major agent endpoints. For live API exploration, see the OpenAPI/Swagger docs (coming soon).

---

## 🔌 Plugin Marketplace

- `POST /plugins/register` — Register a new plugin
- `GET /plugins` — List all plugins
- `POST /plugins/purchase/{plugin_id}` — Purchase a plugin

## 💳 API Billing & Usage

- `POST /users/register` — Register a new user
- `GET /users/{user_id}` — Get user info
- `POST /usage/record` — Record API usage
- `GET /usage/{user_id}` — Get usage stats

## 🏅 Certificates

- `POST /certificates/generate` — Generate a certificate
- `GET /certificates/verify/{verification_code}` — Verify a certificate
- `POST /certificates/pay/{cert_id}` — Pay for certificate

## 💸 Affiliate Program

- `POST /affiliates/register` — Register as an affiliate
- `POST /affiliates/track_referral` — Track a referral
- `GET /affiliates/{affiliate_id}/dashboard` — View affiliate dashboard
- `GET /affiliates/{affiliate_id}/referrals` — List referrals

## ⚡ Pay-Per-Use Agent Actions

- `POST /actions/invoke` — Invoke a premium agent action
- `GET /actions/usage/{user_id}` — Get usage/costs

## 🏢 White-Label Licensing

- `POST /clients/register` — Register a B2B client
- `GET /clients/{client_id}` — Get client info
- `POST /clients/{client_id}/deactivate` — Deactivate client

## 🧾 Billing & Invoicing

- `POST /invoices/create` — Create an invoice
- `GET /invoices/{invoice_id}` — Get invoice
- `POST /invoices/pay/{invoice_id}` — Pay invoice
- `GET /invoices/user/{user_email}` — List user invoices

## 🎟️ Live Events & Webinars

- `POST /events/create` — Create an event
- `GET /events` — List events
- `POST /tickets/purchase` — Purchase a ticket
- `GET /tickets/user/{user_email}` — List user tickets

## 📊 In-App Purchases (Analytics/Reports)

- `POST /purchase` — Purchase a report
- `GET /reports/{report_id}` — Get report content (if purchased)
- `GET /purchases/user/{user_email}` — List user purchases

---

## 🛠️ CLI & SDKs

- CLI tools and SDKs are in development. See the `cli/` directory for current scripts and utilities.

---

_Last updated: 2025-05-26_
