# Student Card System - PostgreSQL Version

Flask application for University of Mpumalanga student and lecturer digital ID cards, now using **PostgreSQL** for Render deployment.

## 🚀 Quick Start for Render

### 1. Create PostgreSQL Database in Render
- Render Dashboard → "New +" → "PostgreSQL"
- Render automatically provides `DATABASE_URL`

### 2. Initialize Database
- Go to PostgreSQL → "Connect" → "psql"
- Copy contents of `database_setup_postgresql.sql`
- Paste and execute

### 3. Deploy Application
- Connect GitHub repository
- Render auto-detects `render.yaml`
- App connects using `DATABASE_URL` automatically

### 4. Set Environment Variables
```
FLASK_ENV=production
SECRET_KEY=<generate-random-string>
DATABASE_URL=<auto-provided-by-render>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=<gmail-app-password>
MAIL_DEFAULT_SENDER=your-email@gmail.com
SUPPORT_RECIPIENT=your-email@gmail.com
PROFILE_BASE_URL=https://your-app.onrender.com
```

## 📋 Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL installed locally

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create database
createdb student_card_db

# Set environment variables
cp env.example .env
# Edit .env with your PostgreSQL credentials

# Initialize database
python setup_database_postgresql.py

# Run application
python app.py
```

## 📁 Project Structure

```
.
├── app.py                          # Main Flask application (PostgreSQL)
├── database.py                     # PostgreSQL connection module
├── database_setup_postgresql.sql  # PostgreSQL schema
├── setup_database_postgresql.py   # Database initialization script
├── requirements.txt                # Python dependencies (psycopg2-binary)
├── render.yaml                     # Render deployment config
├── Procfile                        # Process file for Render
└── static/                         # Static files (CSS, images, uploads)
```

## 🔧 Database Configuration

### Render (Production)
- Uses `DATABASE_URL` automatically provided by Render
- No manual configuration needed

### Local Development
- Option 1: Use `DATABASE_URL` in `.env`
- Option 2: Use individual variables (`DB_HOST`, `DB_PORT`, etc.)

## ✅ Features

- ✅ Student and staff registration/login
- ✅ Digital ID card creation
- ✅ Photo upload with face detection
- ✅ PDF verification (proof of registration/employment)
- ✅ QR code generation
- ✅ Public profile pages
- ✅ Support ticket system
- ✅ Email notifications

## 📚 Documentation

- `POSTGRESQL_MIGRATION_GUIDE.md` - Complete migration guide
- `POSTGRESQL_CONVERSION_SUMMARY.md` - Conversion summary
- `STEP_BY_STEP_SETUP.md` - Deployment setup guide

## 🐛 Troubleshooting

### Database Connection Failed
- Check `DATABASE_URL` is set (Render provides this automatically)
- Verify PostgreSQL database is running
- Check database credentials

### Tables Not Found
- Run `database_setup_postgresql.sql` to create tables
- Or run `python setup_database_postgresql.py`

### Import Errors
- Ensure `psycopg2-binary` is installed: `pip install psycopg2-binary`
- Check Python version (3.11+)

## 🔄 Migration from MySQL

If migrating from MySQL:
1. See `POSTGRESQL_MIGRATION_GUIDE.md` for complete guide
2. All MySQL-specific syntax has been converted
3. Schema converted to PostgreSQL format
4. All queries updated for PostgreSQL compatibility

## 📝 License

This project is for University of Mpumalanga use.

---

**Ready for Render PostgreSQL deployment!** 🚀

