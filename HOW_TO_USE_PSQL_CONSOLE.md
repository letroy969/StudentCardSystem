# How to Use Render PostgreSQL Console (psql)

## Step-by-Step Guide to Access psql Console

### Step 1: Access Your PostgreSQL Database

1. In Render Dashboard, find your PostgreSQL database
2. Click on it (the one named `student-card-db`)

### Step 2: Open psql Console

1. Look for tabs at the top: **"Overview"**, **"Connect"**, **"Logs"**, etc.
2. Click on **"Connect"** tab
3. You'll see connection information and options
4. Look for a button that says:
   - **"psql"** or
   - **"Open psql"** or
   - **"Connect with psql"** or
   - **"Launch Console"**

5. Click that button

### Step 3: psql Console Opens

After clicking, you'll see:
- A terminal/console window opens
- It shows a prompt like: `student_card_db=>` or `postgres=>`
- This is the PostgreSQL command line interface

### Step 4: Paste Your SQL Schema

1. **Open** `database_setup_postgresql.sql` file from your project
2. **Select ALL** the contents (Ctrl+A or Cmd+A)
3. **Copy** it (Ctrl+C or Cmd+C)
4. **Go back to the psql console** in Render
5. **Right-click** in the console window
6. **Select "Paste"** (or press Ctrl+V / Cmd+V)
7. The SQL will appear in the console
8. **Press Enter** to execute

### Step 5: Verify Execution

You should see output like:
```
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE FUNCTION
CREATE TRIGGER
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
```

If you see these messages, **success!** ✅

---

## Visual Guide

```
Render Dashboard
    ↓
Click PostgreSQL Database (`student-card-db`)
    ↓
Click "Connect" Tab
    ↓
Click "psql" Button
    ↓
Console Opens (shows: student_card_db=>)
    ↓
Right-click → Paste SQL
    ↓
Press Enter
    ↓
See CREATE TABLE messages ✅
```

---

## Alternative: If psql Button Not Visible

If you don't see a "psql" button:

### Option 1: Use Connection String
1. In "Connect" tab, copy the connection string
2. Use it with local psql client:
   ```bash
   psql "postgresql://user:password@host:port/dbname"
   ```

### Option 2: Use Render Shell
1. Some Render plans have a "Shell" option
2. Click "Shell" tab
3. Run: `psql $DATABASE_URL`
4. Then paste your SQL

### Option 3: Use SQL Editor (if available)
1. Some Render interfaces have a SQL editor
2. Look for "SQL Editor" or "Query" tab
3. Paste SQL there and click "Run"

---

## Troubleshooting

### Can't Find psql Button
- Check if you're on the "Connect" tab
- Look for "Console" or "Terminal" options
- Try refreshing the page

### Paste Doesn't Work
- Try right-click → Paste
- Or Ctrl+V (Windows/Linux) / Cmd+V (Mac)
- Some browsers require right-click menu

### SQL Doesn't Execute
- Make sure you pressed Enter after pasting
- Check for syntax errors in the output
- Verify you're connected to the right database

### No Output After Enter
- Wait a few seconds (SQL might be executing)
- Check if there are any error messages
- Try typing `\dt` to list tables (should show your tables)

---

## Quick Checklist

- [ ] PostgreSQL database created
- [ ] Clicked on database in dashboard
- [ ] Clicked "Connect" tab
- [ ] Clicked "psql" button
- [ ] Console opened (shows prompt)
- [ ] Opened `database_setup_postgresql.sql` file
- [ ] Copied all SQL contents
- [ ] Pasted into psql console
- [ ] Pressed Enter
- [ ] Saw CREATE TABLE messages

---

## What the psql Console Looks Like

```
student_card_db=> 
```

This is where you paste your SQL. After pasting and pressing Enter:

```
student_card_db=> CREATE TABLE IF NOT EXISTS student_cards (
    id SERIAL PRIMARY KEY,
    ...
);
CREATE TABLE
student_card_db=> 
```

---

**That's where you paste!** Right in that console window after clicking "psql"! 🎯

