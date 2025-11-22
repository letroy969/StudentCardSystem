# Railway Database Setup Guide (Free Alternative)

Railway offers **$5 free credit monthly** which is enough for small apps. This guide shows you how to set up MySQL on Railway instead of PlanetScale.

---

## Why Railway?

- ✅ **Free**: $5 credit/month (usually enough)
- ✅ **MySQL**: Native MySQL 8.0 support
- ✅ **No code changes**: Works with your existing code
- ✅ **No sleep**: Databases stay active
- ✅ **Easy setup**: One-click deployment

---

## Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"** or **"Login"**
3. Sign up with **GitHub** (recommended) or email
4. Authorize Railway to access your GitHub (if using GitHub)

---

## Step 2: Create MySQL Database

1. Once logged in, you'll see your dashboard
2. Click **"New Project"** (if you don't have one)
3. Give it a name: `student-card-db` (or any name)
4. Click **"New"** button (top right)
5. Select **"Database"** from the dropdown
6. Choose **"Add MySQL"**
7. Railway will automatically create a MySQL 8.0 database
8. Wait ~30 seconds for setup to complete

---

## Step 3: Get Database Credentials

1. Click on your MySQL database service (in the project)
2. Go to **"Variables"** tab
3. You'll see these environment variables:
   - `MYSQLHOST` → This is your **DB_HOST**
   - `MYSQLPORT` → This is your **DB_PORT** (usually 3306)
   - `MYSQLDATABASE` → This is your **DB_NAME**
   - `MYSQLUSER` → This is your **DB_USER**
   - `MYSQLPASSWORD` → This is your **DB_PASSWORD**

4. **Copy these values** - you'll need them for Render!

**Example values:**
```
MYSQLHOST=containers-us-west-xxx.railway.app
MYSQLPORT=3306
MYSQLDATABASE=railway
MYSQLUSER=root
MYSQLPASSWORD=xxxxx
```

---

## Step 4: Import Database Schema

### Option A: Using Railway Console (Easiest)

1. In Railway, click on your MySQL database
2. Go to **"Data"** tab
3. Click **"Open MySQL Console"** or **"Query"** button
4. A SQL console will open
5. Open `database_setup.sql` from your project
6. Copy **ALL** the contents
7. Paste into Railway SQL console
8. Click **"Run"** or press `Ctrl+Enter`
9. You should see success messages for each table

### Option B: Using MySQL Client

1. Install MySQL client (if not installed)
2. Use Railway's connection string:
   ```bash
   mysql -h containers-us-west-xxx.railway.app -P 3306 -u root -p
   ```
3. Enter password (from MYSQLPASSWORD)
4. Run:
   ```sql
   USE railway;  -- or your database name
   SOURCE database_setup.sql;
   ```

---

## Step 5: Use in Render

Now use Railway credentials in Render environment variables:

1. Go to Render Dashboard → Your Service → Environment
2. Update these variables with Railway values:

```
DB_HOST=containers-us-west-xxx.railway.app  (from MYSQLHOST)
DB_PORT=3306                                 (from MYSQLPORT)
DB_NAME=railway                              (from MYSQLDATABASE)
DB_USER=root                                 (from MYSQLUSER)
DB_PASSWORD=xxxxx                            (from MYSQLPASSWORD)
```

**That's it!** Your app will connect to Railway MySQL instead of PlanetScale.

---

## Step 6: Verify Connection

1. Deploy your app on Render
2. Visit: `https://your-app.onrender.com/test_db`
3. Should see: `"Database connected! Current time: ..."`
4. If it works, you're all set! ✅

---

## Railway Free Tier Limits

- **$5 credit/month**: Usually enough for 1-2 small databases
- **512MB RAM**: Per database
- **1GB storage**: Per database
- **No sleep**: Databases stay active 24/7

**Cost**: Free (within $5 monthly credit)

---

## Monitoring Usage

1. In Railway dashboard, click on your project
2. See **"Usage"** section
3. Monitor your $5 credit usage
4. If you exceed $5, you'll be charged (very cheap though)

---

## Troubleshooting

### Connection Failed

**Check:**
- Railway database is running (should show "Active")
- Credentials are correct (especially DB_HOST)
- DB_PORT is 3306
- Firewall allows connections (Railway handles this)

### Schema Import Failed

**Solutions:**
- Check SQL syntax (Railway uses standard MySQL)
- Make sure you're in the correct database
- Try running SQL statements one at a time

### Exceeded Free Credit

**Options:**
- Switch to TiDB Serverless (completely free)
- Or pay Railway (~$5-10/month for small database)
- Or use Supabase PostgreSQL (free, requires code changes)

---

## Alternative: TiDB Serverless (100% Free)

If Railway credit runs out, switch to **TiDB Serverless**:

1. Go to [tidbcloud.com](https://tidbcloud.com)
2. Sign up (free, no credit card)
3. Create Serverless cluster
4. Get credentials
5. Update Render environment variables
6. **Note**: TiDB uses port **4000** (not 3306), so set `DB_PORT=4000`

See `FREE_DATABASE_ALTERNATIVES.md` for more details.

---

## Quick Reference

**Railway Credentials Location:**
- Railway Dashboard → Project → MySQL Database → Variables tab

**Render Environment Variables:**
- Render Dashboard → Service → Environment tab

**Test Connection:**
- `https://your-app.onrender.com/test_db`

---

**That's it!** Railway is now your database provider. Your app works exactly the same! 🚀

