"""
Database connection module for PostgreSQL.
Supports both DATABASE_URL (Render) and individual connection parameters.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Get PostgreSQL database connection.
    Supports DATABASE_URL (Render format) or individual environment variables.
    
    Returns:
        psycopg2.connection: Database connection object, or None if connection fails
    """
    try:
        # Check for DATABASE_URL first (Render format)
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Parse DATABASE_URL
            # Format: postgresql://user:password@host:port/dbname
            # Render may provide postgres:// which needs to be converted to postgresql://
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            
            conn = psycopg2.connect(
                database_url,
                cursor_factory=RealDictCursor
            )
            return conn
        
        # Fallback to individual environment variables (for local development)
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'student_card_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        
        conn = psycopg2.connect(
            **db_config,
            cursor_factory=RealDictCursor
        )
        return conn
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def get_db_cursor(conn):
    """
    Get a dictionary cursor from a connection.
    
    Args:
        conn: Database connection object
        
    Returns:
        psycopg2.extras.RealDictCursor: Dictionary cursor
    """
    return conn.cursor(cursor_factory=RealDictCursor)

