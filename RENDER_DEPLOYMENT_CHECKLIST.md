# Render Deployment Checklist

This checklist ensures your Student Card System works exactly the same on Render as it does on localhost.

## Pre-Deployment Checklist

### ✅ 1. Code Configuration

- [x] **Environment Variables**: All sensitive data uses `os.getenv()` (no hardcoded credentials)
- [x] **Database Connection**: Uses environment variables for DB_HOST, DB_USER, DB_PASSWORD, etc.
- [x] **Email Configuration**: Uses environment variables for SMTP settings
- [x] **Profile URL Detection**: `get_profile_base_url()` function handles both local and production
- [x] **Upload Folder**: Properly creates upload directory if it doesn't exist
- [x] **Debug Mode**: Disabled in production (`debug=False`)
- [x] **Port Configuration**: Uses `PORT` environment variable (Render sets this automatically)

### ✅ 2. File Structure

- [x] **requirements.txt**: Contains all dependencies including `gunicorn`
- [x] **runtime.txt**: Specifies Python version (3.11.9)
- [x] **render.yaml**: Configured with proper build and start commands
- [x] **Procfile**: Contains `web: gunicorn app:app` (backup deployment method)
- [x] **database_setup.sql**: Contains complete database schema

### ✅ 3. Dependencies

All required packages are in `requirements.txt`:
- Flask==3.0.0
- Flask-Mail==0.10.0
- mysql-connector-python==8.2.0
- Pillow>=10.2.0
- qrcode[pil]>=7.4.2
- python-dotenv>=1.0.0
- opencv-python>=4.8.0
- numpy>=1.26.0
- PyPDF2>=3.0.1
- Werkzeug>=3.0.0
- gunicorn>=21.2.0

## Render Setup Checklist

### ✅ 4. Database Setup (PlanetScale)

- [ ] **Database Created**: PlanetScale database `student_card_db` exists
- [ ] **Schema Imported**: Run `database_setup.sql` in PlanetScale console
- [ ] **Credentials Obtained**: Have DB_HOST, DB_USER, DB_PASSWORD ready
- [ ] **Database Active**: Database is not sleeping (PlanetScale free tier sleeps after inactivity)

### ✅ 5. Gmail App Password

- [ ] **2FA Enabled**: Two-factor authentication enabled on Gmail account
- [ ] **App Password Generated**: 16-character app password created
- [ ] **Password Saved**: App password saved securely (you'll need it for Render)

### ✅ 6. Render Service Configuration

- [ ] **Repository Connected**: GitHub repo connected to Render
- [ ] **Service Created**: Web service created in Render dashboard
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT` (or use render.yaml)
- [ ] **Python Version**: 3.11.9 (auto-detected from runtime.txt)

### ✅ 7. Environment Variables in Render

Add these in Render Dashboard → Environment:

**Required Variables:**
```bash
FLASK_ENV=production
SECRET_KEY=<generate-with: python -c "import secrets; print(secrets.token_hex(32))">
DB_HOST=<your-planetscale-host>.psdb.cloud
DB_PORT=3306
DB_NAME=student_card_db
DB_USER=<your-planetscale-username>
DB_PASSWORD=<your-planetscale-password>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=umpdigitalcard@gmail.com
MAIL_PASSWORD=<your-16-char-gmail-app-password>
MAIL_DEFAULT_SENDER=umpdigitalcard@gmail.com
SUPPORT_RECIPIENT=umpdigitalcard@gmail.com
```

**After First Deploy:**
```bash
PROFILE_BASE_URL=https://your-app-name.onrender.com
```

**Important Notes:**
- Replace `<...>` placeholders with actual values
- `MAIL_USE_TLS` should be the string `"True"` (not boolean)
- `PROFILE_BASE_URL` should be set AFTER first deployment (you'll get the URL from Render)

### ✅ 8. Render Disk Setup (CRITICAL for File Uploads)

**⚠️ IMPORTANT**: Without a Render Disk, uploaded files will be lost on redeploy!

- [ ] **Disk Added**: Go to Settings → Disks → Add Disk
- [ ] **Disk Name**: `uploads-disk`
- [ ] **Mount Path**: `/opt/render/project/src/static/uploads`
- [ ] **Disk Size**: `1GB` (free tier allows this)
- [ ] **Service Restarted**: Service redeployed after adding disk

## Post-Deployment Verification

### ✅ 9. Basic Functionality Tests

Test these URLs and features after deployment:

- [ ] **Homepage**: `https://your-app.onrender.com/` loads without errors
- [ ] **Database Connection**: `https://your-app.onrender.com/test_db` shows "Database connected! Current time: ..."
- [ ] **Registration**: Can register new account with `@ump.ac.za` email
- [ ] **Login**: Can login with registered account
- [ ] **Student Dashboard**: Dashboard loads after login
- [ ] **Lecturer Dashboard**: Lecturer login works (if testing staff account)

### ✅ 10. Core Feature Tests

- [ ] **Photo Upload**: Can upload profile photo (with face detection)
- [ ] **Live Photo Capture**: Live camera capture works
- [ ] **PDF Upload**: Can upload proof of registration/employment PDF
- [ ] **Card Creation**: Can create student/lecturer card with all fields
- [ ] **Card Preview**: Card preview page displays correctly
- [ ] **QR Code Generation**: QR code generates and displays on card
- [ ] **Public Profile**: `/profile/<email>` route works and displays card
- [ ] **QR Code Scanning**: QR code links to correct profile URL
- [ ] **Support Ticket**: Can submit support ticket
- [ ] **Email Notifications**: Support ticket emails are sent
- [ ] **Reports Page**: Reports page loads (if accessible)

### ✅ 11. Production-Specific Tests

- [ ] **HTTPS**: All URLs use HTTPS (Render does this automatically)
- [ ] **Profile URLs**: QR codes point to correct Render URL (not localhost)
- [ ] **File Persistence**: Uploaded files persist after redeploy (if Render Disk added)
- [ ] **Session Management**: Sessions work correctly (login persists)
- [ ] **Static Files**: CSS, images, and other static files load correctly
- [ ] **Error Handling**: Error pages display correctly

## Common Issues & Solutions

### Issue: Database Connection Failed
**Symptoms**: `/test_db` shows connection error
**Solutions**:
- Verify PlanetScale credentials in Render environment variables
- Check PlanetScale database is active (not sleeping)
- Ensure `DB_HOST` includes `.psdb.cloud` domain
- Check PlanetScale database password hasn't expired

### Issue: Email Not Sending
**Symptoms**: Support tickets don't send emails
**Solutions**:
- Verify Gmail App Password is correct (16 characters, no spaces)
- Check `MAIL_USERNAME` matches Gmail account
- Ensure 2FA is enabled on Gmail account
- Verify `MAIL_USE_TLS` is set to `"True"` (string, not boolean)

### Issue: QR Codes Point to Wrong URL
**Symptoms**: QR codes link to localhost or wrong domain
**Solutions**:
- Set `PROFILE_BASE_URL` environment variable in Render
- Ensure `PROFILE_BASE_URL` matches your Render app URL exactly
- Redeploy after setting the variable
- Check `get_profile_base_url()` function is working correctly

### Issue: Files Lost on Redeploy
**Symptoms**: Uploaded photos/PDFs disappear after redeploy
**Solutions**:
- Add Render Disk (see step 8 above)
- Verify disk mount path matches upload folder: `/opt/render/project/src/static/uploads`
- Check disk is properly mounted in Render dashboard
- Consider migrating to cloud storage (S3, Cloudinary) for production

### Issue: OpenCV Build Fails
**Symptoms**: Build fails with OpenCV errors
**Solutions**:
- Verify Python version is 3.11.9 (check runtime.txt)
- Check `opencv-python` is in requirements.txt
- Render should handle OpenCV automatically, but if issues persist, check build logs

### Issue: App Crashes on Start
**Symptoms**: Service fails to start
**Solutions**:
- Check Render logs for specific error messages
- Verify all environment variables are set correctly
- Ensure `gunicorn` is in requirements.txt
- Check start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Issue: Static Files Not Loading
**Symptoms**: CSS/images don't load
**Solutions**:
- Verify `static_folder='static'` in Flask app initialization
- Check static files are committed to Git
- Ensure file paths are relative (not absolute)
- Check Render build logs for file copy errors

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `FLASK_ENV` | Yes | Flask environment | `production` |
| `SECRET_KEY` | Yes | Flask secret key | Random 64-char hex |
| `DB_HOST` | Yes | Database host | `xxx.psdb.cloud` |
| `DB_PORT` | Yes | Database port | `3306` |
| `DB_NAME` | Yes | Database name | `student_card_db` |
| `DB_USER` | Yes | Database username | `xxxxx` |
| `DB_PASSWORD` | Yes | Database password | `pscale_pw_xxx` |
| `MAIL_SERVER` | Yes | SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | Yes | SMTP port | `587` |
| `MAIL_USE_TLS` | Yes | Use TLS | `"True"` (string) |
| `MAIL_USERNAME` | Yes | Email username | `your@email.com` |
| `MAIL_PASSWORD` | Yes | Email app password | `16-char-password` |
| `MAIL_DEFAULT_SENDER` | Yes | Default sender | `your@email.com` |
| `SUPPORT_RECIPIENT` | Yes | Support email | `support@email.com` |
| `PROFILE_BASE_URL` | No* | Base URL for QR codes | `https://app.onrender.com` |

*Required after first deployment for QR codes to work correctly

## Final Checklist Before Going Live

- [ ] All environment variables set correctly
- [ ] Database schema imported successfully
- [ ] Test registration/login works
- [ ] QR codes generate correctly
- [ ] Public profiles accessible
- [ ] File uploads work (Render Disk added)
- [ ] Email notifications work
- [ ] Support ticket submission works
- [ ] HTTPS enabled (automatic on Render)
- [ ] All static files load correctly
- [ ] No errors in Render logs
- [ ] Performance is acceptable

## Monitoring After Deployment

1. **Check Render Logs Regularly**: Dashboard → Service → Logs
2. **Monitor Database**: PlanetScale dashboard for connection issues
3. **Test Core Features**: Periodically test registration, login, card creation
4. **Check Disk Usage**: Monitor Render Disk usage if using persistent storage
5. **Review Error Logs**: Watch for any recurring errors

## Support Resources

- **Render Documentation**: https://render.com/docs
- **PlanetScale Documentation**: https://planetscale.com/docs
- **Flask Deployment Guide**: https://flask.palletsprojects.com/en/latest/deploying/
- **Gunicorn Documentation**: https://gunicorn.org/

---

**Last Updated**: 2025-01-27
**Version**: 1.0

