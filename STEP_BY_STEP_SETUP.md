# Step-by-Step Pre-Deployment Setup Guide

Complete walkthrough for deploying your Flask app to Render with PostgreSQL.

---

## Part 1: Render PostgreSQL Database Setup ⭐

**You're using Render PostgreSQL** - Render provides PostgreSQL databases automatically!

### Step 1.1: Create Render Account

1. Go to [render.com](https://render.com)
2. Click **"Get Started"** or **"Sign up"**
3. Sign up with GitHub (recommended) or email
4. Verify your email if required

### Step 1.2: Create PostgreSQL Database

1. Once logged in, click **"New +"** button (top right)
2. Select **"PostgreSQL"**
3. Fill in the form:
   - **Name**: `student-card-db` (service name - what you see in Render dashboard)
   - **Database**: `student_card_db` (actual database name - used in connection strings)
   - **Region**: Choose closest to your users
   - **Plan**: **Free** (sufficient for development)
4. Click **"Create Database"**
5. Wait ~30 seconds for database to be created

**Important Notes**: 
- **Name** (`student-card-db`) = Service/instance name in Render dashboard
- **Database** (`student_card_db`) = Actual PostgreSQL database name (used in `DATABASE_URL`)
- **"Deploy PostgreSQL Instance"**: Render does this automatically when you click "Create Database" - you don't need to select anything!
- After clicking "Create Database", the database is automatically deployed and ready to use

### Step 1.3: Get Database Connection Info

1. Once database is created, click on it
2. You'll see **"Connection Info"** section
3. **Important**: Render automatically provides `DATABASE_URL` environment variable
4. You can also see individual connection details:
   - **Host**: `dpg-xxxxx-a.oregon-postgres.render.com`
   - **Port**: `5432`
   - **Database**: `student_card_db`
   - **User**: `student_card_db_user`
   - **Password**: `xxxxx` (shown once, save it!)

**Note**: You don't need to manually set `DATABASE_URL` - Render does this automatically when you link the database to your web service!

### Step 1.4: Initialize Database Schema

**Option A: Using Render PostgreSQL Console (Easiest)**

1. In Render dashboard, click on your PostgreSQL database
2. Go to **"Connect"** tab
3. Click **"psql"** button (opens PostgreSQL console)
4. A terminal will open
5. Open `database_setup_postgresql.sql` from your project
6. Copy **ALL** the contents of `database_setup_postgresql.sql`
7. Paste into the PostgreSQL console
8. Press `Enter` to execute
9. You should see `CREATE TABLE` messages for each table

**Option B: Using psql Client**

1. Install PostgreSQL client (if not installed)
2. Use Render's connection string:
   ```bash
   psql "postgresql://user:password@host:port/dbname"
   ```
   (Get the connection string from Render → Database → Connect)
3. Run:
   ```sql
   \i database_setup_postgresql.sql
   ```
   Or paste the SQL file contents directly

**That's it!** Your Render PostgreSQL database is ready to use!

---

## Part 2: Gmail App Password Setup

### Step 2.1: Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Sign in with your Gmail account (`umpdigitalcard@gmail.com`)
3. Under **"How you sign in to Google"**, find **"2-Step Verification"**
4. Click **"2-Step Verification"**
5. If not enabled:
   - Click **"Get started"**
   - Follow the setup wizard
   - You'll need your phone for verification
   - Complete the setup
6. If already enabled, you're good to go!

### Step 2.2: Generate App Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Or: Google Account → Security → 2-Step Verification → App passwords
2. You may need to sign in again
3. Under **"Select app"**, choose **"Mail"**
4. Under **"Select device"**, choose **"Other (Custom name)"**
5. Type: `Render Deployment` (or any name)
6. Click **"Generate"**
7. **IMPORTANT**: Copy the 16-character password immediately!
   - It looks like: `abcd efgh ijkl mnop` (16 characters, may have spaces)
   - Remove spaces when using: `abcdefghijklmnop`
8. **Save this password** - you'll need it for Render!

**Note**: If you don't see "App passwords" option:
- Make sure 2FA is enabled first
- Some accounts may need to verify identity first

---

## Part 3: Render Web Service Setup

### Step 3.1: Connect GitHub Repository

1. In Render dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see **"Connect a repository"** section
4. If not connected:
   - Click **"Connect account"** or **"Configure account"**
   - Authorize Render to access your GitHub
   - Select repositories (choose **"All repositories"** or specific ones)
   - Click **"Install"**
5. Search for your repository: `letroy969/StudentCardSystem`
6. Click **"Connect"** next to your repository

### Step 3.2: Configure Web Service

Fill in these settings:

**Basic Settings:**
- **Name**: `ump-digital-card` (or your preferred name)
- **Region**: Choose closest to your users (e.g., `Oregon (US West)`)
- **Branch**: `main` (or `master` if that's your main branch)
- **Root Directory**: Leave **empty** (unless your app is in a subdirectory)

**Build & Deploy:**
- **Environment**: `Python 3` (should auto-detect)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Auto-Deploy**: `Yes` (deploys automatically on git push)
- **Datadog API Key**: Leave empty (optional - not needed for basic deployment)

**Advanced Settings:**
- Leave defaults for now

**Note**: Datadog is optional monitoring. Render's built-in logs and metrics are sufficient for most use cases. See `DATADOG_MONITORING.md` for details.

### Step 3.3: Link PostgreSQL Database

**IMPORTANT**: This automatically sets `DATABASE_URL`!

1. In the web service configuration, scroll to **"Add-ons"** section
2. Click **"Add PostgreSQL"** or **"Link Database"**
3. Select your PostgreSQL database (created in Step 1.2)
4. Render will automatically:
   - Link the database to your web service
   - Set `DATABASE_URL` environment variable
   - Make database accessible to your app

**That's it!** No need to manually set database credentials!

### Step 3.4: Set Environment Variables

**Before clicking "Create Web Service"**, scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** for each of these:

#### Required Variables:

1. **FLASK_ENV**
   - Key: `FLASK_ENV`
   - Value: `production`

2. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: Generate using:
     ```bash
     python -c "import secrets; print(secrets.token_hex(32))"
     ```
     Or use an online generator: [randomkeygen.com](https://randomkeygen.com/)
     - Copy a 64-character hex string

3. **DATABASE_URL**
   - Key: `DATABASE_URL`
   - Value: **Auto-set by Render** (when you link PostgreSQL database)
   - **You don't need to set this manually!**

4. **MAIL_SERVER**
   - Key: `MAIL_SERVER`
   - Value: `smtp.gmail.com`

5. **MAIL_PORT**
   - Key: `MAIL_PORT`
   - Value: `587`

6. **MAIL_USE_TLS**
   - Key: `MAIL_USE_TLS`
   - Value: `True` (as a string, not boolean)

7. **MAIL_USERNAME**
   - Key: `MAIL_USERNAME`
   - Value: `umpdigitalcard@gmail.com`

8. **MAIL_PASSWORD**
   - Key: `MAIL_PASSWORD`
   - Value: Your Gmail App Password (from Step 2.2)
     - 16 characters, no spaces

9. **MAIL_DEFAULT_SENDER**
   - Key: `MAIL_DEFAULT_SENDER`
   - Value: `umpdigitalcard@gmail.com`

10. **SUPPORT_RECIPIENT**
    - Key: `SUPPORT_RECIPIENT`
    - Value: `umpdigitalcard@gmail.com`

**After adding all variables**, double-check:
- ✅ All 10 variables are added (DATABASE_URL is auto-set)
- ✅ No typos in variable names
- ✅ Values are correct (especially MAIL_PASSWORD)

### Step 3.5: Create and Deploy

1. Scroll to bottom of page
2. Click **"Create Web Service"**
3. Wait for build to start (you'll see build logs)
4. Build takes 5-10 minutes
5. Watch the logs for any errors

**Common Build Issues:**
- If build fails, check logs for error messages
- Most common: Missing dependency (check requirements.txt)
- OpenCV build issues: Usually resolves automatically

### Step 3.6: Get Your App URL

1. Once build completes, you'll see **"Live"** status
2. Your app URL will be displayed at the top
   - Example: `https://ump-digital-card.onrender.com`
3. **Copy this URL** - you'll need it for PROFILE_BASE_URL!

### Step 3.7: Set PROFILE_BASE_URL (After First Deploy)

1. In Render dashboard, go to your service
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - Key: `PROFILE_BASE_URL`
   - Value: Your app URL (from Step 3.6)
     - Example: `https://ump-digital-card.onrender.com`
5. Click **"Save Changes"**
6. This will trigger an automatic redeploy (wait 2-3 minutes)

---

## Part 4: Add Render Disk (CRITICAL!)

### Step 4.1: Navigate to Disk Settings

1. In Render dashboard, go to your web service
2. Click **"Settings"** tab (left sidebar)
3. Scroll down to **"Disks"** section

### Step 4.2: Add Disk

1. Click **"Add Disk"** button
2. Fill in the form:
   - **Name**: `uploads-disk`
   - **Mount Path**: `/opt/render/project/src/static/uploads`
     - ⚠️ **IMPORTANT**: This must match exactly!
   - **Size**: `1GB` (free tier allows up to 1GB)
3. Click **"Add Disk"**
4. Render will show a warning about redeploy - click **"OK"** or **"Continue"**
5. Your service will automatically redeploy (takes 2-3 minutes)

### Step 4.3: Verify Disk

1. After redeploy completes, check **"Logs"** tab
2. Look for disk mount confirmation
3. Your uploads will now persist across redeploys!

**Why This Is Critical:**
- Without a disk, uploaded files are lost every time Render redeploys
- With a disk, files persist permanently
- The mount path must match where your app saves files (`static/uploads`)

---

## Part 5: Verify Deployment

### Step 5.1: Test Basic Functionality

1. Visit your app URL: `https://your-app.onrender.com`
2. Homepage should load without errors

### Step 5.2: Test Database Connection

1. Visit: `https://your-app.onrender.com/test_db`
2. Should see: `"Database connected! Current time: [timestamp]"`
3. If you see an error, check:
   - PostgreSQL database is linked to your service
   - Database schema is initialized (Step 1.4)
   - Check Render logs for specific errors

### Step 5.3: Test Registration

1. Go to: `https://your-app.onrender.com/register`
2. Try registering with a test email ending in `@ump.ac.za`
3. Should redirect to login page after successful registration

### Step 5.4: Test Login

1. Go to: `https://your-app.onrender.com/login`
2. Login with your test account
3. Should redirect to dashboard

### Step 5.5: Test File Upload

1. After logging in, try uploading a photo
2. File should upload successfully
3. Check if file persists after redeploy (if disk is added)

---

## Troubleshooting

### Database Connection Fails

**Symptoms**: `/test_db` shows connection error

**Solutions**:
1. Check PostgreSQL database is **linked** to your web service
   - Go to your service → Settings → Add-ons
   - Should show your PostgreSQL database
2. Verify database schema is initialized
   - Run `database_setup_postgresql.sql` if not done
3. Check Render logs for specific error messages
4. Verify `DATABASE_URL` is set (should be automatic)

### Email Not Sending

**Symptoms**: Support tickets don't send emails

**Solutions**:
1. Verify Gmail App Password is correct (16 characters)
2. Check `MAIL_USERNAME` matches Gmail account
3. Ensure 2FA is enabled on Gmail
4. Check `MAIL_USE_TLS` is set to `"True"` (string)

### QR Codes Point to Wrong URL

**Symptoms**: QR codes link to localhost or wrong domain

**Solutions**:
1. Set `PROFILE_BASE_URL` environment variable (Step 3.7)
2. Ensure it matches your Render app URL exactly
3. Redeploy after setting

### Files Lost on Redeploy

**Symptoms**: Uploaded photos/PDFs disappear

**Solutions**:
1. Add Render Disk (Part 4)
2. Verify mount path is correct: `/opt/render/project/src/static/uploads`
3. Check disk is properly mounted in Render dashboard

### Build Fails

**Symptoms**: Build fails with errors

**Solutions**:
1. Check Render logs for specific error
2. Verify `requirements.txt` has all dependencies
3. Check Python version matches `runtime.txt` (3.11.9)
4. Ensure `gunicorn` is in requirements.txt

---

## Quick Reference Checklist

Use this checklist as you go through the setup:

### PostgreSQL Database
- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Database schema initialized (`database_setup_postgresql.sql`)
- [ ] Database linked to web service

### Gmail
- [ ] 2FA enabled
- [ ] App Password generated
- [ ] 16-character password saved

### Render Web Service
- [ ] GitHub repository connected
- [ ] Web service created
- [ ] PostgreSQL database linked (auto-sets DATABASE_URL)
- [ ] All environment variables set
- [ ] Service deployed successfully
- [ ] App URL copied
- [ ] PROFILE_BASE_URL set (after first deploy)
- [ ] Render Disk added
- [ ] Disk mount path verified

### Testing
- [ ] Homepage loads
- [ ] Database test passes (`/test_db`)
- [ ] Registration works
- [ ] Login works
- [ ] File upload works
- [ ] QR codes work

---

## Need Help?

If you get stuck:

1. **Check Render Logs**: Dashboard → Service → Logs
2. **Check PostgreSQL Logs**: Dashboard → Database → Logs
3. **Review Error Messages**: They usually tell you what's wrong
4. **Verify Environment Variables**: Double-check all values
5. **Test Database Connection**: Use `/test_db` endpoint

---

**You're all set!** 🚀

Once all steps are complete, your app will be live and working exactly like it does on localhost!
