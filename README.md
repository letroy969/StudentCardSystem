# UMP Digital Student Card

Flask application that lets University of Mpumalanga students and lecturers generate verified digital ID cards, upload photos, manage proof-of-registration/employment PDFs, and share QR-based public profiles.

---

## Features

- Student and staff registration/login restricted to `@ump.ac.za`
- Student and lecturer dashboards with live card preview and QR code
- Secure photo capture/upload with face-detection validation
- Automatic PDF verification for proof of registration/employment (PyPDF2)
- Support ticket submission with email notifications (Flask-Mail)
- Reports view (accounts, cards, tickets)
- Public profile pages accessible via QR

Tech stack: Flask 3, MySQL (mysql-connector-python), Tailwind-styled templates, OpenCV/Pillow, qrcode, Gunicorn.

---

## Prerequisites

| Component | Local Dev | Render/PlanetScale |
|-----------|-----------|--------------------|
| Python    | 3.11+     | Managed by Render  |
| MySQL     | 8.x (local) | PlanetScale free tier |
| pip       | Latest    | n/a                |

---

## Local development

1. **Clone & install**
   ```bash
   git clone <repo-url> && cd card1
   python -m venv .venv
   .\.venv\Scripts\activate    # or source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   copy env.example .env   # Windows
   # or
   cp env.example .env     # macOS/Linux
   ```
   Update `.env` values (database, email, secret key). `app.py` already loads them via `python-dotenv`.

3. **Create database schema**
   ```bash
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS student_card_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   python setup_database.py
   ```

4. **Run the server**
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000`.

---

## Production deployment (Render + PlanetScale)

### 1. Prepare repo
- Ensure `requirements.txt`, `Procfile`, and `env.example` are committed (already done).
- Push latest code to GitHub.

### 2. PlanetScale (database)
1. Create an account at [planetscale.com](https://planetscale.com/).
2. Create a database (e.g. `student_card_db`), enable a production branch.
3. Download credentials and note host/user/password.
4. Import schema:
   ```bash
   pscale connect student_card_db main --execute "SOURCE database_setup.sql;"
   ```

### 3. Render (Flask app)
1. Create a new **Web Service** pointing to the GitHub repo.
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:app`
4. Environment variables (Render → Settings → Environment):
   ```
   FLASK_ENV=production
   SECRET_KEY=<random_string>
   DB_HOST=<planetscale-host>
   DB_PORT=3306
   DB_NAME=student_card_db
   DB_USER=<planetscale-user>
   DB_PASSWORD=<planetscale-password>
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=<your_gmail>
   MAIL_PASSWORD=<app_password>
   MAIL_DEFAULT_SENDER=<your_gmail>
   SUPPORT_RECIPIENT=<support inbox>
   ```
5. Deploy – Render will provide an HTTPS URL.

### 4. Optional: custom domain
- Add CNAME pointing to Render.
- Set `PROFILE_BASE_IP` env var if QR profiles should point to your public domain.

---

## Database utilities
- `database_setup.sql` – raw DDL (students, lectures, users, tickets).
- `setup_database.py` – idempotent Python script that creates tables/columns.

---

## Useful scripts

| Command | Description |
|---------|-------------|
| `python setup_database.py` | Creates/updates MySQL schema |
| `python app.py` | Run Flask dev server (`host=0.0.0.0`, port 5000) |
| `gunicorn app:app` | Production WSGI server (Procfile uses this) |

---

## Environment variables
See `env.example` for the full list. Critical ones:

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Flask session/key signing |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | MySQL connection |
| `MAIL_*`, `SUPPORT_RECIPIENT` | Email notifications |
| `PROFILE_BASE_IP` (optional) | Overrides auto-detected IP in QR URLs |

---

## Support & troubleshooting
- Verify MySQL connectivity (`mysql -h host -u user -p`).
- Check Render logs if deployment fails (`render.com` dashboard → Logs).
- Face detection requires OpenCV; ensure Render build uses a Python version with wheel support (3.11 works).
- For local QR profile testing on mobile, use your machine’s LAN IP (e.g. `http://10.x.x.x:5000/profile/...`).

Happy shipping! 🚀

