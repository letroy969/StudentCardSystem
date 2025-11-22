"""
Database initialization script for PostgreSQL.
Run this script to create all tables in your PostgreSQL database.
"""
import os
from dotenv import load_dotenv
from database import get_db_connection

load_dotenv()

def init_database():
    """Initialize PostgreSQL database with all required tables."""
    print("Connecting to PostgreSQL database...")
    conn = get_db_connection()
    
    if not conn:
        print("ERROR: Could not connect to database!")
        print("Please check your DATABASE_URL or DB_* environment variables.")
        return False
    
    print("Connected successfully!")
    
    try:
        cursor = conn.cursor()
        
        # Read SQL file
        sql_file = 'database_setup_postgresql.sql'
        if not os.path.exists(sql_file):
            print(f"ERROR: {sql_file} not found!")
            return False
        
        with open(sql_file, 'r') as f:
            sql_script = f.read()
        
        # Execute SQL script
        print("Creating tables...")
        cursor.execute(sql_script)
        conn.commit()
        
        print("✅ Database initialized successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - student_cards")
        print("  - lecture_cards")
        print("  - support_tickets")
        
        # Verify tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print("\nExisting tables:")
        for table in tables:
            print(f"  - {table['table_name']}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        conn.rollback()
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("PostgreSQL Database Initialization")
    print("=" * 50)
    print()
    
    success = init_database()
    
    if success:
        print("\n" + "=" * 50)
        print("Setup complete! Your database is ready to use.")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("Setup failed! Please check the errors above.")
        print("=" * 50)
        exit(1)

