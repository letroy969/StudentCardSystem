# Pre-Deployment Checklist

Use this checklist before deploying to Render to ensure everything is ready.

## Code Changes ✅

- [x] Removed hardcoded passwords from `app.py`
- [x] All sensitive data uses environment variables
- [x] `Procfile` exists and is correct: `web: gunicorn app:app`
- [x] `runtime.txt` specifies Python version: `python-3.11.9`
- [x] `requirements.txt` includes all dependencies
- [x] `render.yaml` created for easy deployment

## Files Ready ✅

- [x] `app.py` - Main application file
- [x] `requirements.txt` - All Python dependencies
- [x] `Procfile` - Gunicorn start command
- [x] `runtime.txt` - Python version
- [x] `database_setup.sql` - Database schema
- [x] `env.example` - Environment variable template
- [x] `render.yaml` - Render deployment config
- [x] `DEPLOYMENT.md` - Complete deployment guide
- [x] `RENDER_QUICK_START.md` - Quick reference

## Database Setup

- [ ] PlanetScale account created
- [ ] Database `student_card_db` created
- [ ] Schema imported from `database_setup.sql`
- [ ] Database password created
- [ ] Credentials saved securely

## Email Setup

- [ ] Gmail account ready (`umpdigitalcard@gmail.com`)
- [ ] 2-Factor Authentication enabled
- [ ] App Password generated (16 characters)
- [ ] App Password saved securely

## Render Configuration

- [ ] Render account created
- [ ] GitHub repository connected
- [ ] Web service created
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn app:app`
- [ ] All environment variables set (see DEPLOYMENT.md)
- [ ] Render Disk added for file persistence (optional but recommended)

## Environment Variables

Verify all these are set in Render Dashboard:

- [ ] `FLASK_ENV=production`
- [ ] `SECRET_KEY` (random 64-char hex string)
- [ ] `DB_HOST` (PlanetScale host)
- [ ] `DB_PORT=3306`
- [ ] `DB_NAME=student_card_db`
- [ ] `DB_USER` (PlanetScale username)
- [ ] `DB_PASSWORD` (PlanetScale password)
- [ ] `MAIL_SERVER=smtp.gmail.com`
- [ ] `MAIL_PORT=587`
- [ ] `MAIL_USE_TLS=True`
- [ ] `MAIL_USERNAME=umpdigitalcard@gmail.com`
- [ ] `MAIL_PASSWORD` (Gmail App Password)
- [ ] `MAIL_DEFAULT_SENDER=umpdigitalcard@gmail.com`
- [ ] `SUPPORT_RECIPIENT=umpdigitalcard@gmail.com`
- [ ] `PROFILE_BASE_URL` (set after first deploy)

## Post-Deployment Testing

After deployment, test these features:

- [ ] Homepage loads (`/`)
- [ ] Database connection works (`/test_db`)
- [ ] User registration works
- [ ] User login works
- [ ] Student card creation works
- [ ] Photo upload works
- [ ] PDF upload works
- [ ] QR code generation works
- [ ] Public profile accessible (`/profile/<email>`)
- [ ] Support ticket submission works
- [ ] Email notifications work
- [ ] Reports page loads (if accessible)

## Security Checklist

- [ ] No hardcoded passwords in code
- [ ] `SECRET_KEY` is strong and random
- [ ] `.env` file is in `.gitignore`
- [ ] Database credentials are secure
- [ ] Gmail App Password is secure
- [ ] HTTPS enabled (Render does this automatically)

## Performance Checklist

- [ ] Render Disk added for file persistence
- [ ] Database connection pooling configured
- [ ] Static files served correctly
- [ ] No unnecessary debug mode enabled

## Documentation

- [ ] `DEPLOYMENT.md` reviewed
- [ ] `RENDER_QUICK_START.md` reviewed
- [ ] Team members have access to documentation
- [ ] Environment variables documented

## Ready to Deploy! 🚀

Once all items are checked, you're ready to deploy!

1. Push code to GitHub
2. Render will auto-deploy (if enabled)
3. Monitor logs for errors
4. Test all features
5. Set `PROFILE_BASE_URL` after first deploy

---

**Need Help?** See `DEPLOYMENT.md` for detailed instructions.

