# PostgreSQL Instance Naming Guide

## Understanding PostgreSQL Names in Render

When creating a PostgreSQL database in Render, you'll see two different names:

### 1. Service Name (Instance Name)
**Field**: "Name"  
**Example**: `student-card-db`  
**Purpose**: This is what you see in your Render dashboard  
**Used for**: Identifying the service in Render UI  
**Can be**: Any name you like (with hyphens, lowercase recommended)

### 2. Database Name
**Field**: "Database"  
**Example**: `student_card_db`  
**Purpose**: This is the actual PostgreSQL database name  
**Used for**: Connection strings, SQL queries, `DATABASE_URL`  
**Format**: Usually lowercase with underscores

## Recommended Names

### Service Name (Render Dashboard)
```
student-card-db
```
- Easy to identify in Render dashboard
- Uses hyphens (common for service names)
- Descriptive and clear

### Database Name (PostgreSQL)
```
student_card_db
```
- Matches your application's database name
- Uses underscores (PostgreSQL convention)
- Used in `DATABASE_URL` connection string

## Example: Creating in Render

When you create PostgreSQL in Render:

```
Name: student-card-db          ← Service name (dashboard)
Database: student_card_db      ← Database name (connection)
Region: Oregon (US West)
Plan: Free
```

## Connection String Format

After creation, Render provides `DATABASE_URL` like:

```
postgresql://user:password@host:port/student_card_db
                                         ↑
                              This is the database name
```

## Important Notes

1. **Service Name** (`student-card-db`):
   - Only used in Render dashboard
   - Can be changed later (rename service)
   - Doesn't affect connections

2. **Database Name** (`student_card_db`):
   - Used in all connection strings
   - Used in SQL queries (`USE student_card_db`)
   - Should match your application's expected database name
   - Harder to change after creation

3. **Default Behavior**:
   - If you leave "Database" field empty, Render creates a default name
   - Usually based on service name (e.g., `student_card_db_user`)
   - Better to specify `student_card_db` explicitly

## What to Use

**For your application, use:**

- **Service Name**: `student-card-db` (or any name you prefer)
- **Database Name**: `student_card_db` (should match your app's expectation)

This ensures your `DATABASE_URL` will be:
```
postgresql://...@.../student_card_db
```

And your application will connect correctly!

---

**Quick Reference**: 
- Service Name = What you see in dashboard
- Database Name = What's in connection string

