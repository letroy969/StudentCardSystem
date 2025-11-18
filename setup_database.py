import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'letroy70',
    'database': 'student_card_db'
}

def create_database():
    try:
        # Connect without specifying database
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' created successfully!")
        
        # Use the database
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                account_type VARCHAR(50) NOT NULL,
                security_id_number_hash VARCHAR(255),
                security_mother_name_hash VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Users table created successfully!")
        # Ensure security question columns exist on existing users table
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN security_id_number_hash VARCHAR(255)')
            print("security_id_number_hash column added to users table.")
        except Error as e:
            if e.errno == 1060:
                print("security_id_number_hash column already exists.")
            else:
                print(f"Error adding security_id_number_hash column: {e}")

        try:
            cursor.execute('ALTER TABLE users ADD COLUMN security_mother_name_hash VARCHAR(255)')
            print("security_mother_name_hash column added to users table.")
        except Error as e:
            if e.errno == 1060:
                print("security_mother_name_hash column already exists.")
            else:
                print(f"Error adding security_mother_name_hash column: {e}")
        
        # Create student_cards table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_cards (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                title VARCHAR(255),
                name VARCHAR(255),
                surname VARCHAR(255),
                qualification VARCHAR(255),
                student_number VARCHAR(255),
                campus VARCHAR(255) DEFAULT 'Mbombela Campus',
                photo_path VARCHAR(500),
                proof_of_registration_path VARCHAR(500),
                verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (email) REFERENCES users(email)
            )
        ''')
        print("Student cards table created successfully!")
        
        # Add verification_status column to existing table if it doesn't exist
        try:
            cursor.execute('''
                ALTER TABLE student_cards 
                ADD COLUMN verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending'
            ''')
            print("Verification status column added successfully!")
        except Error as e:
            if e.errno == 1060:  # Column already exists
                print("Verification status column already exists.")
            else:
                print(f"Error adding verification column: {e}")
        
        # Ensure campus column exists on student_cards
        try:
            cursor.execute('''
                ALTER TABLE student_cards 
                ADD COLUMN campus VARCHAR(255) DEFAULT 'Mbombela Campus'
            ''')
            print("Campus column added to student_cards successfully!")
        except Error as e:
            if e.errno == 1060:
                print("Campus column already exists on student_cards.")
            else:
                print(f"Error adding campus column to student_cards: {e}")

        # Create lecture_cards table if needed
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lecture_cards (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                title VARCHAR(255),
                name VARCHAR(255),
                surname VARCHAR(255),
                qualification VARCHAR(255),
                employee_number VARCHAR(255),
                campus VARCHAR(255) DEFAULT 'Mbombela Campus',
                photo_path VARCHAR(500),
                proof_of_employment_path VARCHAR(500),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE(email),
                FOREIGN KEY (email) REFERENCES users(email)
            )
        ''')
        print("Lecture cards table ensured successfully!")

        # Ensure campus column exists on lecture_cards (for legacy tables)
        try:
            cursor.execute('''
                ALTER TABLE lecture_cards 
                ADD COLUMN campus VARCHAR(255) DEFAULT 'Mbombela Campus'
            ''')
            print("Campus column added to lecture_cards successfully!")
        except Error as e:
            if e.errno == 1060:
                print("Campus column already exists on lecture_cards.")
            else:
                print(f"Error adding campus column to lecture_cards: {e}")

        conn.commit()
        print("Database setup completed successfully!")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_database() 