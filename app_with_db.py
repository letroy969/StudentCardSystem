from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
import mysql.connector
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import hashlib
import qrcode
from io import BytesIO
import base64
import re
import cv2
import PyPDF2

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for session management

# MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'letroy70',  # Replace with your actual password
    'database': 'student_card_db'
}

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

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

def init_db():
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Users table created successfully!")
        
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
                photo_path VARCHAR(500),
                proof_of_registration_path VARCHAR(500),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (email) REFERENCES users(email)
            )
        ''')
        print("Student cards table created successfully!")
        
        conn.commit()
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_qr_code(data):
    """Generate QR code for given data"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str

def get_student_card_data(email):
    """Get student card data from database"""
    try:
        conn = get_db_connection()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student_cards WHERE email = %s', (email,))
        card_data = cursor.fetchone()
        
        return card_data
    except Exception as e:
        print(f"Error getting student card data: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        account_type = request.form['account_type']
        
        # Validation
        if not email or not email.endswith('@ump.ac.za'):
            flash('Please enter a valid @ump.ac.za email address!', 'error')
            return render_template('register.html')
        
        # Password: 8+ chars, must contain at least one number or special char, cannot be only letters
        if (not password or len(password) < 8 or
            password.isalpha() or
            not (re.search(r'\d', password) or re.search(r'[^a-zA-Z0-9]', password))):
            flash('Password must be at least 8 characters, contain a number or special character, and cannot be only letters.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        try:
            conn = get_db_connection()
            if not conn:
                flash('Database connection failed!', 'error')
                return render_template('register.html')
                
            cursor = conn.cursor(dictionary=True)
            
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                flash('User already exists!', 'error')
                return render_template('register.html')
            
            # Hash password and insert user
            hashed_password = hash_password(password)
            cursor.execute(
                'INSERT INTO users (email, password, account_type) VALUES (%s, %s, %s)',
                (email, hashed_password, account_type)
            )
            conn.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        account_type = request.form['account_type']
        
        # Validation
        if not email or not email.endswith('@ump.ac.za'):
            flash('Please enter a valid @ump.ac.za email address!', 'error')
            return render_template('login.html')
        
        if not password or len(password) < 3:
            flash('Password must be at least 3 characters long!', 'error')
            return render_template('login.html')
        
        try:
            conn = get_db_connection()
            if not conn:
                flash('Database connection failed!', 'error')
                return render_template('login.html')
                
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
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'error')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn:
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
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('student_card_preview'))
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student_cards WHERE email = %s', (session['user'],))
        card_data = cursor.fetchone()
    except Exception as e:
        print(f"Error loading card data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn is not None:
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
        if not conn:
            flash('Database connection failed!', 'error')
            return render_template('student_card_preview.html', card_data=None)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student_cards WHERE email = %s', (session['user'],))
        card_data = cursor.fetchone()
        cursor.close()
    except Exception as e:
        print(f"Error loading card data: {e}")
    finally:
        if 'conn' in locals() and conn:
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
        
        # Handle photo upload with face detection using OpenCV
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename) and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                temp_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_' + secure_filename(file.filename))
                file.save(temp_photo_path)
                
                # Face detection using OpenCV
                import cv2
                img = cv2.imread(temp_photo_path)
                face_detected = False
                
                if img is not None:
                    # Convert to grayscale for face detection
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    
                    # Load the face cascade classifier
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    
                    # Detect faces
                    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                    
                    if len(faces) > 0:
                        face_detected = True
                        print(f"Face detected in photo: {len(faces)} face(s) found")
                    else:
                        print("No face detected in photo")
                else:
                    print("Failed to read image file")
                
                if not face_detected:
                    os.remove(temp_photo_path)
                    flash('Invalid photo: No visible human face detected. Please upload a photo with a clear face.', 'error')
                    return redirect(url_for('student_card_preview'))
                
                # Save final photo
                filename = secure_filename(f"{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.rename(temp_photo_path, filepath)
                photo_path = f"uploads/{filename}"
        
        # Handle proof of registration PDF upload with validation
        proof_path = None
        if 'proof_of_registration' in request.files:
            pdf_file = request.files['proof_of_registration']
            if pdf_file and allowed_file(pdf_file.filename) and pdf_file.filename.lower().endswith('.pdf'):
                temp_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_' + secure_filename(pdf_file.filename))
                pdf_file.save(temp_pdf_path)
                
                # Simple PDF validation - just check if it's a valid PDF file
                try:
                    import PyPDF2
                    with open(temp_pdf_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        # Just verify it's a readable PDF
                        if len(reader.pages) > 0:
                            print("PDF validation successful - file is readable")
                        else:
                            raise Exception("PDF has no pages")
                except Exception as e:
                    print(f"PDF validation error: {e}")
                    os.remove(temp_pdf_path)
                    flash('Error reading PDF file. Please ensure it is a valid PDF document.', 'error')
                    return redirect(url_for('student_card_preview'))
                
                # Save final PDF
                filename = secure_filename(f"{session['user']}_proof_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.rename(temp_pdf_path, filepath)
                proof_path = f"uploads/{filename}"
                print("PDF validation successful - all requirements met")
        
        # Save to database
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!')
            return redirect(url_for('student_card_preview'))
            
        cursor = conn.cursor()
        
        # Check if card exists
        cursor.execute('SELECT id FROM student_cards WHERE email = %s', (session['user'],))
        existing_card = cursor.fetchone()
        
        if existing_card:
            # Update existing card
            update_query = '''
                UPDATE student_cards 
                SET title = %s, name = %s, surname = %s, qualification = %s, 
                    student_number = %s, last_updated = NOW()'''
            update_params = [title, name, surname, qualification, student_number]
            if photo_path:
                update_query += ", photo_path = %s"
                update_params.append(photo_path)
            if proof_path:
                update_query += ", proof_of_registration_path = %s"
                update_params.append(proof_path)
            update_query += " WHERE email = %s"
            update_params.append(session['user'])
            cursor.execute(update_query, tuple(update_params))
        else:
            # Insert new card
            cursor.execute('''
                INSERT INTO student_cards 
                (email, title, name, surname, qualification, student_number, photo_path, proof_of_registration_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (session['user'], title, name, surname, qualification, student_number, photo_path, proof_path))
        
        conn.commit()
        flash('Card updated successfully!')
        
    except Exception as e:
        flash(f'Error updating card: {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
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
            if conn:
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
                cursor.close()
            else:
                return {'card_status': 'inactive'}
        except Exception as e:
            return {'card_status': 'inactive'}
        finally:
            if 'conn' in locals() and conn:
                conn.close()
    return {'authenticated': False}, 401

@app.route('/profile/<email>')
def public_profile(email):
    """Public profile page accessible via QR code"""
    card_data = get_student_card_data(email)
    
    if not card_data:
        return render_template('profile_not_found.html', email=email)
    
    return render_template('public_profile.html', card_data=card_data)

@app.route('/generate-qr/<email>')
def generate_qr(email):
    """Generate QR code for student profile"""
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Only allow users to generate QR for their own profile
    if session['user'] != email:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get your computer's IP address to make it accessible on the same network
    import socket
    try:
        # Get local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_url = f"http://{local_ip}:5000"
    except:
        # Fallback to localhost
        public_url = request.host_url.rstrip('/')
    
    # Create the profile URL
    profile_url = public_url + url_for('public_profile', email=email)
    
    # Generate QR code
    qr_code = generate_qr_code(profile_url)
    
    return jsonify({
        'qr_code': qr_code,
        'profile_url': profile_url,
        'local_ip': local_ip if 'local_ip' in locals() else 'localhost'
    })

@app.route('/generate-qr-json/<email>')
def generate_qr_json(email):
    """Generate QR code for student profile (JSON response with base64)"""
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Only allow users to generate QR for their own profile
    if session['user'] != email:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get your computer's IP address to make it accessible on the same network
    import socket
    try:
        # Get local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_url = f"http://{local_ip}:5000"
    except:
        # Fallback to localhost
        public_url = request.host_url.rstrip('/')
    
    # Create the profile URL
    profile_url = public_url + url_for('public_profile', email=email)
    
    # Generate QR code image and convert to base64
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return jsonify({
        'qr_code_base64': img_str,
        'profile_url': profile_url,
        'local_ip': local_ip if 'local_ip' in locals() else 'localhost'
    })

@app.route('/qr-image/<email>')
def qr_image(email):
    """Generate QR code image for student profile"""
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Only allow users to generate QR for their own profile
    if session['user'] != email:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get your computer's IP address to make it accessible on the same network
    import socket
    try:
        # Get local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_url = f"http://{local_ip}:5000"
    except:
        # Fallback to localhost
        public_url = request.host_url.rstrip('/')
    
    # Create the profile URL
    profile_url = public_url + url_for('public_profile', email=email)
    
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes for response
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    from flask import send_file
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    init_db()  # Initialize database tables
    
    # Get local IP address for network access
    import socket
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"�� Local Network URL: http://{local_ip}:5000")
        print(f"📱 QR codes will work on phones connected to the same WiFi!")
        print(f"🔗 Make sure your phone is on the same WiFi network")
    except Exception as e:
        print(f"⚠️  Could not get local IP: {e}")
        print("📱 QR codes will only work on your computer")
    
    app.run(debug=True, host='0.0.0.0') 