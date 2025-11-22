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

**Tech stack**: Flask 3, PostgreSQL (psycopg2-binary), Tailwind-styled templates, OpenCV/Pillow, qrcode, Gunicorn.

---

## Prerequisites

| Component | Local Dev | Render |
|-----------|-----------|--------|
| Python    | 3.11+     | Managed by Render |
| PostgreSQL | 14+ (local) | Render PostgreSQL (free tier) |
| pip       | Latest    | n/a |

---

## Quick Deploy to Render

### 1. One-Click Setup

1. **Fork/Clone this repository**
2. **Create Render account**: [render.com](https://render.com)
3. **Create PostgreSQL database** in Render
4. **Create Web Service** in Render:
   - Connect your GitHub repository
   - Render auto-detects `render.yaml` configuration
   - Link PostgreSQL database (auto-sets `DATABASE_URL`)
   - Set environment variables (see below)
5. **Initialize database**: Run `database_setup_postgresql.sql` in Render PostgreSQL console
6. **Add Render Disk**: For file persistence (see setup guide)
7. **Deploy!** Render auto-deploys on git push

### 2. Environment Variables (Set in Render Dashboard)

```
FLASK_ENV=production
SECRET_KEY=<generate-random-64-char-hex>
DATABASE_URL=<auto-provided-by-render-when-database-linked>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=<gmail-16-char-app-password>
MAIL_DEFAULT_SENDER=your-email@gmail.com
SUPPORT_RECIPIENT=your-email@gmail.com
PROFILE_BASE_URL=https://your-app.onrender.com
```

**Note**: `DATABASE_URL` is automatically set when you link PostgreSQL database to your web service!

### 3. Complete Setup Guide

See **[STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)** for detailed step-by-step instructions.

---

## Local Development

### 1. Clone & Install

```bash
git clone <repo-url> && cd card1
python -m venv .venv
.\.venv\Scripts\activate    # Windows
# or
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
copy env.example .env   # Windows
# or
cp env.example .env     # macOS/Linux
```

Update `.env` with your PostgreSQL credentials:
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/student_card_db
# OR use individual variables:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=student_card_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Create Database & Schema

```bash
# Create PostgreSQL database
createdb student_card_db

# Initialize schema
python setup_database_postgresql.py
# OR manually:
psql student_card_db < database_setup_postgresql.sql
```

### 4. Run the Server

```bash
python app.py
```

Visit `http://localhost:5000`.

---

## Production Deployment (Render)

### Prerequisites

- GitHub repository with code
- Render account (free tier available)
- Gmail account with App Password enabled

### Deployment Steps

1. **Create PostgreSQL Database** in Render
   - Render Dashboard → "New +" → "PostgreSQL"
   - Note: Render provides `DATABASE_URL` automatically

2. **Create Web Service** in Render
   - Connect GitHub repository
   - Render auto-detects `render.yaml`
   - Link PostgreSQL database (sets `DATABASE_URL` automatically)
   - Set environment variables

3. **Initialize Database Schema**
   - Render PostgreSQL → Connect → psql
   - Run `database_setup_postgresql.sql`

4. **Add Render Disk** (for file persistence)
   - Settings → Disks → Add Disk
   - Mount: `/opt/render/project/src/static/uploads`
   - Size: 1GB

5. **Deploy**
   - Render auto-deploys on git push
   - Or manually trigger deploy

**Full Guide**: See **[STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)**

---

## Database Schema

The application uses PostgreSQL with these tables:

- `users` - Authentication and user accounts
- `student_cards` - Student digital ID cards
- `lecture_cards` - Lecturer digital ID cards
- `support_tickets` - Support ticket system

**Schema File**: `database_setup_postgresql.sql`

**Initialization Script**: `setup_database_postgresql.py`

---

## Project Structure

```
.
├── app.py                          # Main Flask application
├── database.py                     # PostgreSQL connection module
├── database_setup_postgresql.sql  # PostgreSQL schema
├── setup_database_postgresql.py   # Database initialization
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render deployment config
├── Procfile                        # Process file for Render
├── runtime.txt                     # Python version
├── env.example                     # Environment variables template
├── static/                         # Static files (CSS, images, uploads)
└── templates/                      # HTML templates
```

---

## Environment Variables

See `env.example` for the full list. Critical ones:

| Variable | Purpose | Required |
|----------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection (Render auto-provides) | Yes |
| `SECRET_KEY` | Flask session/key signing | Yes |
| `MAIL_*` | Email configuration | Yes |
| `PROFILE_BASE_URL` | Base URL for QR codes | After deploy |

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `python setup_database_postgresql.py` | Initialize PostgreSQL schema |
| `python app.py` | Run Flask dev server |
| `gunicorn app:app` | Production WSGI server |

---

## Support & Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is set (Render provides this automatically)
- Check PostgreSQL database is linked to web service
- Ensure schema is initialized

### File Upload Issues
- Add Render Disk for file persistence
- Verify disk mount path matches upload folder

### Email Not Sending
- Verify Gmail App Password (16 characters)
- Check 2FA is enabled on Gmail
- Verify `MAIL_USE_TLS=True` (string)

### Deployment Issues
- Check Render logs: Dashboard → Service → Logs
- Verify all environment variables are set
- Ensure `requirements.txt` has all dependencies

**Full Troubleshooting**: See **[STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)** → Troubleshooting section

---

## Documentation

- **[STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)** - Complete deployment guide
- **[POSTGRESQL_MIGRATION_GUIDE.md](POSTGRESQL_MIGRATION_GUIDE.md)** - PostgreSQL migration details
- **[RENDER_COMPATIBILITY_CHECK.md](RENDER_COMPATIBILITY_CHECK.md)** - Render compatibility verification
- **[FINAL_RENDER_VERIFICATION.md](FINAL_RENDER_VERIFICATION.md)** - Final verification summary

---

## License

This project is for University of Mpumalanga use.

---

**Ready to deploy!** 🚀

Follow **[STEP_BY_STEP_SETUP.md](STEP_BY_STEP_SETUP.md)** for step-by-step deployment instructions.
