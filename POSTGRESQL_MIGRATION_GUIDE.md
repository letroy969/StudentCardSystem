# PostgreSQL Migration Guide

Complete guide for migrating from MySQL to PostgreSQL for Render deployment.

## ✅ Conversion Complete

Your Flask application has been fully converted from MySQL to PostgreSQL. All changes have been made to support Render's PostgreSQL database.

## What Changed

### 1. Database Driver
- **Before**: `mysql-connector-python`
- **After**: `psycopg2-binary`

### 2. Connection Method
- **Before**: Individual DB_HOST, DB_USER, DB_PASSWORD variables
- **After**: Supports `DATABASE_URL` (Render format) + fallback to individual variables

### 3. Database Schema Changes
- `AUTO_INCREMENT` → `SERIAL`
- `ENUM` → `VARCHAR` with `CHECK` constraints
- `DATETIME` → `TIMESTAMP`
- `ON UPDATE CURRENT_TIMESTAMP` → PostgreSQL trigger function

### 4. Query Syntax
- Parameterized queries (`%s`) remain the same ✅
- `NOW()` function works the same ✅
- `COUNT(*)` queries updated to use aliases for RealDictCursor

### 5. Cursor Handling
- **Before**: `cursor(dictionary=True)` for MySQL
- **After**: `RealDictCursor` automatically used (returns dicts)

## Files Updated

### Core Files
- ✅ `app.py` - Updated to use PostgreSQL
- ✅ `requirements.txt` - Replaced MySQL with PostgreSQL driver
- ✅ `database.py` - New PostgreSQL connection module
- ✅ `database_setup_postgresql.sql` - PostgreSQL schema
- ✅ `setup_database_postgresql.py` - Database initialization script
- ✅ `render.yaml` - Updated for PostgreSQL
- ✅ `env.example` - Updated with PostgreSQL config

## Setup Instructions

### For Render Deployment

1. **Create PostgreSQL Database in Render**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Render automatically provides `DATABASE_URL`

2. **Set Environment Variables**
   - Render automatically sets `DATABASE_URL`
   - No need to set individual DB_* variables

3. **Initialize Database**
   - Option A: Use Render's PostgreSQL console
     - Go to your PostgreSQL database → "Connect" → "psql"
     - Copy contents of `database_setup_postgresql.sql`
     - Paste and execute
   
   - Option B: Run initialization script locally
     ```bash
     export DATABASE_URL="postgresql://user:pass@host:port/dbname"
     python setup_database_postgresql.py
     ```

4. **Deploy Application**
   - Push code to GitHub
   - Render will auto-deploy
   - App will connect using `DATABASE_URL`

### For Local Development

1. **Install PostgreSQL**
   ```bash
   # macOS
   brew install postgresql
   
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # Windows
   # Download from postgresql.org
   ```

2. **Create Database**
   ```bash
   createdb student_card_db
   ```

3. **Set Environment Variables**
   Create `.env` file:
   ```bash
   DATABASE_URL=postgresql://postgres:password@localhost:5432/student_card_db
   # OR use individual variables:
   DB_HOST, DB_PORT, etc.
   ```

4. **Initialize Database**
   ```bash
   python setup_database_postgresql.py
   ```

5. **Run Application**
   ```bash
   python app.py
   ```

## Database Schema

The PostgreSQL schema (`database_setup_postgresql.sql`) includes:

- ✅ `users` table - Authentication
- ✅ `student_cards` table - Student card data
- ✅ `lecture_cards` table - Lecturer card data
- ✅ `support_tickets` table - Support tickets
- ✅ Indexes for performance
- ✅ Trigger for `updated_at` timestamp

## Key Differences from MySQL

### 1. Connection String Format
```python
# MySQL
mysql://user:pass@host:port/db

# PostgreSQL
postgresql://user:pass@host:port/db
```

### 2. Auto-increment
```sql
-- MySQL
id INT AUTO_INCREMENT PRIMARY KEY

-- PostgreSQL
id SERIAL PRIMARY KEY
```

### 3. ENUM Types
```sql
-- MySQL
status ENUM('open', 'closed')

-- PostgreSQL
status VARCHAR(20) CHECK (status IN ('open', 'closed'))
```

### 4. Timestamps
```sql
-- MySQL
updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

-- PostgreSQL (uses trigger)
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- + trigger function
```

## Testing

### Test Database Connection
```bash
# Visit in browser after deployment
https://your-app.onrender.com/test_db
```

Should show: `"Database connected! Current time: [timestamp]"`

### Test All Features
- ✅ Registration
- ✅ Login
- ✅ Card creation
- ✅ File uploads
- ✅ QR codes
- ✅ Support tickets

## Troubleshooting

### Connection Failed
**Error**: `Database connection failed`

**Solutions**:
1. Check `DATABASE_URL` is set in Render
2. Verify PostgreSQL database is running
3. Check database credentials

### Table Not Found
**Error**: `relation "users" does not exist`

**Solution**: Run `database_setup_postgresql.sql` to create tables

### Syntax Error
**Error**: PostgreSQL syntax errors

**Solutions**:
1. Ensure using `database_setup_postgresql.sql` (not MySQL version)
2. Check all queries use PostgreSQL syntax
3. Verify no MySQL-specific functions used

## Migration Checklist

- [x] Replace MySQL driver with PostgreSQL
- [x] Update connection logic
- [x] Convert database schema
- [x] Update all SQL queries
- [x] Fix cursor handling
- [x] Update environment variables
- [x] Create initialization script
- [x] Update documentation

## Next Steps

1. **Deploy to Render**
   - Create PostgreSQL database
   - Deploy application
   - Initialize database schema

2. **Test Everything**
   - Test all routes
   - Verify database operations
   - Check file uploads

3. **Monitor**
   - Check Render logs
   - Monitor database performance
   - Verify all features work

---

**Your application is now ready for PostgreSQL deployment on Render!** 🚀

