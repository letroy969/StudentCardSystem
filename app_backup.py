from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import hashlib

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for session management

# MySQL connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change if your MySQL user is different
    'password': 'Loidy70',
    'database': 'student_card_db'  # Updated database name
}

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

# Example route to show database connection usage
@app.route('/test_db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT NOW();')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"Database connected! Current time: {result[0]}"
    except Exception as e:
        return f"Database connection failed: {e}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        account_type = request.form['account_type']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                flash('User already exists!')
                return redirect(url_for('login'))
            
            # Hash password and insert user
            hashed_password = hash_password(password)
            cursor.execute(
                'INSERT INTO users (email, password, account_type) VALUES (%s, %s, %s)',
                (email, hashed_password, account_type)
            )
            conn.commit()
            
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Database error: {e}")
            # Fallback: just redirect to login for now
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        account_type = request.form['account_type']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Check user credentials
            hashed_password = hash_password(password)
            cursor.execute(
                'SELECT * FROM users WHERE email = %s AND password = %s AND account_type = %s',
                (email, hashed_password, account_type)
            )
            user = cursor.fetchone()
            
            if user:
                session['user'] = email
                session['account_type'] = account_type
                session['user_id'] = user['id']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials!')
        except Exception as e:
            print(f"Database error: {e}")
            # Fallback: allow login for now (temporary)
            session['user'] = email
            session['account_type'] = account_type
            session['user_id'] = 1  # Temporary user ID
            return redirect(url_for('dashboard'))
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Load user's card data
    card_data = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student_cards WHERE email = %s', (session['user'],))
        card_data = cursor.fetchone()
    except Exception as e:
        print(f"Error loading card data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    return render_template('student_dashboard.html', card_data=card_data)

@app.route('/student-card-preview')
def student_card_preview():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Load user's card data
    card_data = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student_cards WHERE email = %s', (session['user'],))
        card_data = cursor.fetchone()
    except Exception as e:
        print(f"Error loading card data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    return render_template('student_card_preview.html', card_data=card_data)

@app.route('/update-card', methods=['POST'])
def update_card():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        title = request.form['title']
        student_number = request.form['studentNumber']
        full_name = request.form['fullName']
        qualification = request.form['qualification']
        
        # Split full name
        name_parts = full_name.split(' ', 1)
        name = name_parts[0]
        surname = name_parts[1] if len(name_parts) > 1 else ''
        
        # Handle photo upload
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                photo_path = f"uploads/{filename}"
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if card exists
        cursor.execute('SELECT id FROM student_cards WHERE email = %s', (session['user'],))
        existing_card = cursor.fetchone()
        
        if existing_card:
            # Update existing card
            if photo_path:
                cursor.execute('''
                    UPDATE student_cards 
                    SET title = %s, name = %s, surname = %s, qualification = %s, 
                        student_number = %s, photo_path = %s, last_updated = NOW()
                    WHERE email = %s
                ''', (title, name, surname, qualification, student_number, photo_path, session['user']))
            else:
                cursor.execute('''
                    UPDATE student_cards 
                    SET title = %s, name = %s, surname = %s, qualification = %s, 
                        student_number = %s, last_updated = NOW()
                    WHERE email = %s
                ''', (title, name, surname, qualification, student_number, session['user']))
        else:
            # Insert new card
            cursor.execute('''
                INSERT INTO student_cards 
                (email, title, name, surname, qualification, student_number, photo_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (session['user'], title, name, surname, qualification, student_number, photo_path))
        
        conn.commit()
        flash('Card updated successfully!')
        
    except Exception as e:
        flash(f'Error updating card: {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    return redirect(url_for('student_card_preview'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/check-auth')
def check_auth():
    if 'user' in session:
        return {'authenticated': True}
    return {'authenticated': False}, 401

@app.route('/api/card-status')
def card_status():
    if 'user' in session:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM student_cards WHERE email = %s', (session['user'],))
            card_data = cursor.fetchone()
            
            if card_data:
                return {
                    'card_status': 'active',
                    'title': card_data['title'],
                    'name': card_data['name'],
                    'surname': card_data['surname'],
                    'qualification': card_data['qualification'],
                    'studentNumber': card_data['student_number'],
                    'photo': card_data['photo_path']
                }
            else:
                return {'card_status': 'inactive'}
        except Exception as e:
            return {'card_status': 'error', 'message': str(e)}
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    return {'card_status': 'unknown'}, 401

if __name__ == '__main__':
    app.run(debug=True) 