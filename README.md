# Resume Automation API (Bubble-Ready Backend)

A modular, microservice-style backend built using **FastAPI**, designed for integration with **Bubble** or any no-code/low-code platform. This API scrapes LinkedIn-style profiles, filters them, exports to Excel/CSV, and supports email delivery via Gmail or AWS SES.

---

## 🚀 Features

- 🔐 User Signup & Login (`/auth`)
- 🌐 Profile Scraping using Apify (`/scrape`)
- 📤 Email Delivery via Gmail or AWS SES (`/email`)
- 📥 Export Filtered Profiles to Excel/CSV (`/export`)
- 🔗 RESTful API endpoints — easily connectable in Bubble

---

## 🧱 Folder Structure

```
resume_api_bubble_ready/
├── api/
│   ├── main_api.py              # FastAPI app entrypoint
│   ├── auth.py                  # Login/signup logic
│   ├── scraper.py               # Apify scraping logic
│   ├── emailer.py               # Email sending logic
│   ├── utils.py                 # Excel/CSV export utilities
│   └── routes/
│       ├── auth_routes.py       # /auth/login, /auth/signup
│       ├── scrape_routes.py     # /scrape
│       ├── email_routes.py      # /email
│       └── export_routes.py     # /export
├── .env.sample                  # Credentials template
└── requirements.txt             # Full dependencies
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/resume-api-bubble-ready.git
cd resume-api-bubble-ready
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
# Activate it:
# On Windows
.venv\Scripts\activate
# On Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` File
Rename `.env.sample` → `.env` and fill in:
```
APIFY_API_TOKEN=your_apify_token
GMAIL_USER=your_gmail@gmail.com
GMAIL_PASS=your_gmail_app_password
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
SES_SENDER=your_verified_email@example.com
```

---

## 🧪 Run the Server
```bash
uvicorn api.main_api:app --reload
```

Open in browser:
```
http://localhost:8000/docs
```

---

## 🔌 Connect to Bubble

1. Use Bubble’s API Connector
2. Set URL to your endpoint, e.g.:
   - `POST /auth/login`
   - `POST /scrape`
   - `POST /email`
   - `POST /export/excel`
3. Send `Content-Type: application/json` and match the payload
4. Use Bubble workflows to trigger actions and receive results

---

## 🧼 License

MIT License. Feel free to modify and use!
