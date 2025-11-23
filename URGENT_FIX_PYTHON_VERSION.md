# 🔴 URGENT FIX: Python Version Issue

## Problem:
- Render is using **Python 3.13.4** (too new!)
- `psycopg2-binary==2.9.9` doesn't work with Python 3.13
- Need Python **3.11.9** (as specified in runtime.txt)

---

## ✅ IMMEDIATE FIX:

### Step 1: Set Python Version in Render

1. Go to **Render Dashboard** → Your Service (`StudentCardSystem`)
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.9`
5. Click **"Save Changes"**

### Step 2: Manual Deploy

1. Go to **"Manual Deploy"** button (top right)
2. Click **"Deploy latest commit"**
3. Wait for build (will now use Python 3.11.9)

---

## Why This Happened:

Render ignored `runtime.txt` and used Python 3.13.4 by default.
Setting `PYTHON_VERSION=3.11.9` environment variable forces Render to use the correct version.

---

**Do this NOW: Add PYTHON_VERSION=3.11.9 environment variable!** 🚀

