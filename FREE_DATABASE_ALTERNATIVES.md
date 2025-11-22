# Free Database Alternatives to PlanetScale

Your app uses MySQL, so here are the best **free** MySQL-compatible database options that work with Render.

---

## 🏆 Best Free MySQL Alternatives

### Option 1: Railway (Recommended) ⭐

**Why Railway?**
- ✅ **Free tier**: $5 free credit monthly (enough for small apps)
- ✅ **MySQL support**: Native MySQL 8.0
- ✅ **Easy setup**: One-click deployment
- ✅ **No sleep**: Databases stay active
- ✅ **Same connection**: Works with `mysql-connector-python`

**Free Tier Limits:**
- $5 credit/month (usually enough for 1-2 small databases)
- 512MB RAM per database
- 1GB storage
- No sleep/pause

**Setup Steps:**

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub (free)

2. **Create MySQL Database**
   - Click **"New Project"**
   - Click **"New"** → **"Database"** → **"Add MySQL"**
   - Railway creates database automatically
   - Wait ~30 seconds for setup

3. **Get Credentials**
   - Click on your MySQL database
   - Go to **"Variables"** tab
   - Copy these values:
     - `MYSQLHOST` → Use as `DB_HOST`
     - `MYSQLPORT` → Use as `DB_PORT` (usually 3306)
     - `MYSQLDATABASE` → Use as `DB_NAME`
     - `MYSQLUSER` → Use as `DB_USER`
     - `MYSQLPASSWORD` → Use as `DB_PASSWORD`

4. **Import Schema**
   - Click **"Query"** tab in Railway
   - Copy contents of `database_setup.sql`
   - Paste and run

5. **Use in Render**
   - Use Railway credentials in Render environment variables
   - Same as PlanetScale setup!

**Cost**: Free (with $5 monthly credit)

---

### Option 2: TiDB Serverless (MySQL Compatible)

**Why TiDB?**
- ✅ **Completely free**: No credit card required
- ✅ **MySQL compatible**: Works with `mysql-connector-python`
- ✅ **5GB storage**: More than PlanetScale free tier
- ✅ **No sleep**: Always active
- ✅ **Auto-scaling**: Handles traffic spikes

**Free Tier Limits:**
- 5 GiB storage per database
- Up to 5 databases
- Unlimited requests
- Always active (no sleep)

**Setup Steps:**

1. **Create TiDB Account**
   - Go to [tidbcloud.com](https://tidbcloud.com)
   - Sign up (free, no credit card)

2. **Create Cluster**
   - Click **"Create Cluster"**
   - Choose **"Serverless"** (free tier)
   - Select region closest to you
   - Click **"Create"**

3. **Get Connection Info**
   - After cluster is ready, click **"Connect"**
   - Copy connection string or get:
     - **Host**: `xxxxx.tidbcloud.com`
     - **Port**: `4000` (TiDB uses port 4000, not 3306)
     - **User**: `root` (or provided username)
     - **Password**: Set during cluster creation
     - **Database**: Create one or use default

4. **Import Schema**
   - Use TiDB Cloud console SQL editor
   - Or connect with MySQL client:
     ```bash
     mysql -h xxxxx.tidbcloud.com -P 4000 -u root -p < database_setup.sql
     ```

5. **Update Render Config**
   - Set `DB_PORT=4000` (not 3306!)
   - Use TiDB host, user, password in Render

**Cost**: Free forever

---

### Option 3: Northflank (MySQL)

**Why Northflank?**
- ✅ **Free tier**: 2 databases free
- ✅ **MySQL support**: Native MySQL
- ✅ **Easy management**: Web console
- ✅ **No sleep**: Always active

**Free Tier Limits:**
- 2 databases
- 1GB storage per database
- 512MB RAM
- Always active

**Setup Steps:**

1. **Create Northflank Account**
   - Go to [northflank.com](https://northflank.com)
   - Sign up (free)

2. **Create MySQL Database**
   - Click **"New Service"** → **"Database"** → **"MySQL"**
   - Choose free tier
   - Create database

3. **Get Credentials**
   - Go to database → **"Connection"** tab
   - Copy host, port, user, password, database name

4. **Import Schema**
   - Use Northflank SQL console
   - Or connect with MySQL client

5. **Use in Render**
   - Same as other options

**Cost**: Free (2 databases)

---

### Option 4: Aiven (MySQL)

**Why Aiven?**
- ✅ **Free trial**: $300 credit for 30 days
   - After trial: Pay-as-you-go (very cheap for small apps)
- ✅ **MySQL support**: Native MySQL
- ✅ **Reliable**: Enterprise-grade infrastructure

**Free Tier:**
- $300 credit for 30 days (free trial)
- After trial: ~$10-15/month for small database (pay-as-you-go)

**Setup Steps:**

1. **Create Aiven Account**
   - Go to [aiven.io](https://aiven.io)
   - Sign up (free trial)

2. **Create MySQL Service**
   - Click **"Create Service"**
   - Choose **"MySQL"**
   - Select **"Startup"** plan (cheapest)
   - Choose region
   - Create service

3. **Get Credentials**
   - Go to service → **"Overview"** tab
   - Copy connection details:
     - Host, Port, User, Password, Database

4. **Import Schema**
   - Use Aiven console or MySQL client

**Cost**: Free trial, then ~$10-15/month

---

## 🔄 Alternative: Switch to PostgreSQL (Free Options)

If you're open to switching from MySQL to PostgreSQL, these options are **completely free**:

### Supabase (PostgreSQL) ⭐

**Why Supabase?**
- ✅ **Completely free**: No credit card required
- ✅ **500MB storage**: Free tier
- ✅ **Always active**: No sleep
- ✅ **Easy to use**: Great dashboard

**Setup Steps:**

1. **Create Supabase Account**
   - Go to [supabase.com](https://supabase.com)
   - Sign up (free)

2. **Create Project**
   - Click **"New Project"**
   - Fill in details
   - Wait for setup (~2 minutes)

3. **Get Connection String**
   - Go to **"Settings"** → **"Database"**
   - Copy connection string or get:
     - Host, Port (5432), Database, User, Password

4. **Update Your Code**
   - Change `mysql-connector-python` to `psycopg2-binary` in requirements.txt
   - Update `app.py` to use PostgreSQL connection
   - Convert SQL schema (mostly compatible)

**Cost**: Free (500MB storage)

---

### Neon (PostgreSQL)

**Why Neon?**
- ✅ **Completely free**: No credit card required
- ✅ **500MB storage**: Free tier
- ✅ **Serverless**: Auto-scales
- ✅ **Branching**: Database branching feature

**Setup Steps:**

1. **Create Neon Account**
   - Go to [neon.tech](https://neon.tech)
   - Sign up (free)

2. **Create Project**
   - Click **"Create Project"**
   - Choose region
   - Create project

3. **Get Connection String**
   - Copy connection string from dashboard
   - Or get individual values

4. **Update Code** (same as Supabase)
   - Switch to PostgreSQL
   - Update requirements.txt
   - Update app.py

**Cost**: Free (500MB storage)

---

## 📊 Comparison Table

| Provider | Type | Free Tier | Storage | Sleep? | Best For |
|----------|------|-----------|---------|--------|----------|
| **Railway** | MySQL | $5 credit/month | 1GB | No | Easiest setup |
| **TiDB** | MySQL | Free forever | 5GB | No | Most storage |
| **Northflank** | MySQL | 2 databases | 1GB each | No | Multiple DBs |
| **Aiven** | MySQL | $300 trial | Varies | No | Enterprise |
| **Supabase** | PostgreSQL | Free | 500MB | No | Easiest PG |
| **Neon** | PostgreSQL | Free | 500MB | No | Serverless PG |

---

## 🎯 Recommendation

### For MySQL (No Code Changes):

**Best Choice: Railway** ⭐
- Easiest setup
- Works with your existing code
- $5 free credit is usually enough
- No sleep issues

**Alternative: TiDB Serverless**
- Completely free
- More storage (5GB)
- MySQL compatible
- Slightly more setup

### For PostgreSQL (Requires Code Changes):

**Best Choice: Supabase** ⭐
- Easiest PostgreSQL option
- Great free tier
- Excellent documentation
- Would need to update code (see below)

---

## 🔧 How to Switch to PostgreSQL (If You Choose)

If you want to use Supabase or Neon (PostgreSQL), you'll need to:

### Step 1: Update requirements.txt

Change:
```python
mysql-connector-python==8.2.0
```

To:
```python
psycopg2-binary==2.9.9
```

### Step 2: Update app.py

Change:
```python
import mysql.connector
```

To:
```python
import psycopg2
from psycopg2.extras import RealDictCursor
```

Change database connection:
```python
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None
```

Change cursor usage:
```python
cursor = conn.cursor(dictionary=True)  # MySQL
# To:
cursor = conn.cursor(cursor_factory=RealDictCursor)  # PostgreSQL
```

### Step 3: Update SQL Schema

PostgreSQL uses slightly different syntax:
- `AUTO_INCREMENT` → `SERIAL` or `GENERATED ALWAYS AS IDENTITY`
- `DATETIME` → `TIMESTAMP`
- `ENUM` → Same, but syntax slightly different

Most of your schema will work as-is!

---

## 🚀 Quick Setup Guide: Railway (Recommended)

1. **Sign up**: [railway.app](https://railway.app) (free)
2. **Create MySQL**: New Project → Database → Add MySQL
3. **Get credentials**: Database → Variables tab
4. **Import schema**: Database → Query tab → Paste `database_setup.sql`
5. **Use in Render**: Copy credentials to Render environment variables

**That's it!** Your app will work exactly the same.

---

## 💡 My Recommendation

**Use Railway** for the easiest setup:
- ✅ No code changes needed
- ✅ Free $5 credit monthly
- ✅ Same MySQL connection
- ✅ Easy to set up
- ✅ No sleep issues

If Railway credit runs out, switch to **TiDB Serverless** (completely free).

---

## 📚 Updated Setup Guide

I'll update `STEP_BY_STEP_SETUP.md` to include Railway as the primary option. Would you like me to do that?

---

**Need help setting up Railway?** Let me know and I can create a detailed Railway setup guide!

