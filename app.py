from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file, abort, get_flashed_messages
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import Error as Psycopg2Error
import os
from werkzeug.utils import secure_filename
import hashlib
from PIL import Image
import qrcode
from io import BytesIO
import base64
from dotenv import load_dotenv
from database import get_db_connection
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except Exception:
    cv2 = None  # type: ignore
    np = None  # type: ignore
    OPENCV_AVAILABLE = False

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', 'digital_card_secret_key')  # Needed for session management

# Email configuration using Flask-Mail (defaults to provided Gmail account)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'umpdigitalc@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'Digital#70')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)
SUPPORT_RECIPIENT = os.getenv('SUPPORT_RECIPIENT', app.config['MAIL_DEFAULT_SENDER'])

# Database connection is now handled by database.py module
# It supports both DATABASE_URL (Render) and individual environment variables

def normalize_security_answer(answer: str) -> str:
    """Normalize security answers by removing spaces and casing."""
    return ''.join(answer.strip().lower().split())

def hash_security_answer(answer: str) -> str:
    normalized = normalize_security_answer(answer)
    if not normalized:
        return ''
    return hashlib.sha256(normalized.encode()).hexdigest()

def send_ticket_email(student_email, subject, message):
    """Send email notification for support ticket"""
    try:
        if not SUPPORT_RECIPIENT:
            print("Support recipient email not configured.")
            return False
        body = f"""
New Support Ticket Received

Student Email: {student_email}
Subject: {subject}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message:
{message}

---
This is an automated notification from the Student Card System.
        """
        msg = Message(subject=f"Support Ticket from {student_email}: {subject}", recipients=[SUPPORT_RECIPIENT])
        msg.body = body
        mail.send(msg)
        print(f"Email sent successfully for ticket from {student_email}")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB max file size

# Ensure upload folder exists (works in both local and Render)
if not os.path.exists(UPLOAD_FOLDER):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    except OSError as e:
        print(f"Warning: Could not create upload folder: {e}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_profile_base_url():
    """Get the base URL for profile links, works in both local and production."""
    # Check for environment variable first (for production) - highest priority
    profile_base = os.getenv('PROFILE_BASE_URL')
    if profile_base:
        return profile_base.rstrip('/')
    
    # Detect Render environment - Render sets RENDER_EXTERNAL_URL
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    if render_url:
        return render_url.rstrip('/')
    
    # Check if we're in production environment
    is_production = os.getenv('FLASK_ENV') == 'production' or os.getenv('RENDER') == 'true'
    
    if is_production:
        try:
            # In production, use request.host with HTTPS
            scheme = 'https' if request.is_secure or os.getenv('RENDER') else 'http'
            return f"{scheme}://{request.host}"
        except RuntimeError:
            # Outside request context, fallback
            return 'https://your-app.onrender.com'  # Fallback - should be overridden by PROFILE_BASE_URL
    
    # Local development: try to get local IP, fallback to request.host
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return f"http://{local_ip}:5000"
    except:
        try:
            return f"http://{request.host}"
        except RuntimeError:
            return "http://localhost:5000"

# get_db_connection() is now imported from database.py
# It handles PostgreSQL connections with DATABASE_URL support

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password_strength(password):
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/~`' for c in password)
    if not has_letter:
        return False, 'Password must include at least one letter.'
    if not has_digit:
        return False, 'Password must include at least one number.'
    if not has_special:
        return False, 'Password must include at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?/~`).'
    return True, ''

def detect_faces(image_path):
    """Detect faces in the uploaded image"""
    try:
        print(f"OpenCV available: {OPENCV_AVAILABLE}")
        if not OPENCV_AVAILABLE:
            # OpenCV not available; do basic image validation instead
            with Image.open(image_path) as img:
                # Basic validation - check if image has reasonable dimensions
                width, height = img.size
                if width < 200 or height < 200:
                    return False, "Image is too small. Please upload a clearer image."
                if width > 4000 or height > 4000:
                    return False, "Image is too large. Please upload a smaller image."
                
                # Without OpenCV, we can't detect faces properly
                print("OpenCV not available - rejecting image for face detection")
                return False, "Face detection not available. Please ensure OpenCV is properly installed."
        
        print("Using OpenCV for face detection")
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            return False, "Could not load image"
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Load the face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces with more strict parameters
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1,      # How much the image size is reduced at each image scale
            minNeighbors=5,       # How many neighbors each candidate rectangle should have
            minSize=(30, 30),     # Minimum possible object size
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        print(f"Detected {len(faces)} face(s)")
        
        if len(faces) == 0:
            return False, "No human face detected. Please ensure your face is clearly visible and try again."
        elif len(faces) > 1:
            return False, "Multiple faces detected. Please upload an image with only one face."
        else:
            # Check if the face is reasonably sized and positioned
            x, y, w, h = faces[0]
            face_area = w * h
            image_area = image.shape[0] * image.shape[1]
            face_percentage = face_area / image_area
            
            print(f"Face area: {face_area}, Image area: {image_area}, Percentage: {face_percentage:.2%}")
            
            # More strict face size validation
            if face_percentage < 0.08:  # Face should be at least 8% of the image
                return False, "Oops! No human Face detected, please upload a clear picture of yourself"
            elif face_percentage > 0.7:  # Face shouldn't be more than 70% of the image
                return False, "Face too large. Please step back from the camera and try again."
            
            # Check if face is reasonably centered (not at the very edge)
            center_x = x + w // 2
            center_y = y + h // 2
            img_center_x = image.shape[1] // 2
            img_center_y = image.shape[0] // 2
            
            # Face should be reasonably centered (within 40% of image center)
            if (abs(center_x - img_center_x) > image.shape[1] * 0.4 or 
                abs(center_y - img_center_y) > image.shape[0] * 0.4):
                return False, "Face not centered. Please position your face in the center of the frame."
            
            # Additional validation: check for reasonable face proportions
            aspect_ratio = w / h
            if aspect_ratio < 0.7 or aspect_ratio > 1.4:  # Face should be roughly square-ish
                return False, "Face proportions not suitable. Please ensure your face is facing forward."

            return True, "Face detected successfully. Your photo has been captured and saved for your student card."
            
    except Exception as e:
        return False, f"Error detecting faces: {str(e)}"

def detect_faces_fast(image_path):
    """Fast face detection for live photos - optimized for speed"""
    try:
        if not OPENCV_AVAILABLE:
            # Fallback to basic validation if OpenCV is not available
            with Image.open(image_path) as img:
                if img.width < 100 or img.height < 100:
                    return False, "Image too small"
                return True, "Image validation passed"
        
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            return False, "Could not load image"
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Load the face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Fast face detection with optimized parameters
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.2,  # Faster detection
            minNeighbors=3,   # Lower threshold for speed
            minSize=(20, 20), # Smaller minimum size
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        if len(faces) == 0:
            return False, "No face detected"
        elif len(faces) > 1:
            return False, "Multiple faces detected"
        else:
            # Basic face size check
            face = faces[0]
            face_area = face[2] * face[3]
            image_area = image.shape[0] * image.shape[1]
            face_percentage = (face_area / image_area) * 100
            
            if face_percentage < 0.5:  # Very small face
                return False, "Face too small"
            else:
                return True, "Face detected successfully"
                
    except Exception as e:
        return False, f"Face detection error: {str(e)}"

def validate_file_size(file):
    """Validate file size"""
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    return size <= MAX_FILE_SIZE

def validate_image_quality(image_path):
    """Validate image quality and dimensions"""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            # Check minimum dimensions
            if width < 200 or height < 200:
                return False, "Image is too small. Minimum size is 200x200 pixels"
            
            # Check maximum dimensions
            if width > 4000 or height > 4000:
                return False, "Image is too large. Maximum size is 4000x4000 pixels"
            
            # Check aspect ratio (should be reasonable for a photo)
            aspect_ratio = width / height
            if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                return False, "Image aspect ratio is not suitable for a photo"
            
            return True, "Image quality is acceptable"
            
    except Exception as e:
        return False, f"Error validating image: {str(e)}"

def validate_pdf_file(file):
    """Validate PDF file"""
    try:
        # Check file extension
        if not file.filename.lower().endswith('.pdf'):
            return False, "File must be a PDF"
        
        # Check file size
        if not validate_file_size(file):
            return False, f"File size too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
        
        # Read first few bytes to check if it's actually a PDF
        file.seek(0)
        header = file.read(4)
        file.seek(0)
        
        if header != b'%PDF':
            return False, "File is not a valid PDF"
        
        return True, "PDF file is valid"
        
    except Exception as e:
        return False, f"Error validating PDF: {str(e)}"

def verify_proof_of_employment(file_path, employee_number, full_name):
    """Verify proof of employment using Python libraries"""
    try:
        # Try to import PyPDF2 for PDF text extraction
        try:
            import PyPDF2
            PDF_AVAILABLE = True
        except ImportError:
            PDF_AVAILABLE = False
        
        if not PDF_AVAILABLE:
            # If PyPDF2 not available, do basic validation
            return True
        
        print(f"Looking for employee number: {employee_number}")
        print(f"Looking for name: {full_name}")
        
        # Extract text from PDF
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if PDF has pages
            if len(pdf_reader.pages) == 0:
                print("Verification failed: PDF has no pages")
                return False
            
            # Extract text from all pages to get complete document
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text()
            
            text = full_text.lower()
            print(f"PDF text preview: {text[:200]}...")  # Print first 200 characters for debugging
            
            # Check 1: Must contain "2025"
            if '2025' not in text:
                print("Verification failed: 2025 not found in document")
                print(f"Available text: {text[:500]}")  # Show more text for debugging
                return False
            else:
                print("✓ 2025 found in document")
            
            # Check 2: Must contain University of Mpumalanga keywords
            ump_keywords = [
                'university of mpumalanga', 'ump', 'mpumalanga university'
            ]
            ump_found = any(keyword in text for keyword in ump_keywords)
            if not ump_found:
                print("Verification failed: University of Mpumalanga not found in document")
                print(f"Available text: {text[:500]}")  # Show more text for debugging
                return False
            else:
                print("✓ University of Mpumalanga found in document")
            
            # Check 3: Employee number from form must match document
            if str(employee_number).lower() not in text:
                print(f"Verification failed: Employee number {employee_number} not found in document")
                print(f"Available text: {text[:500]}")  # Show more text for debugging
                return False
            else:
                print(f"✓ Employee number {employee_number} found in document")
            
            # Check 4: Name must match document (try both full name and partial matches)
            name_parts = full_name.lower().split()
            name_match = any(part in text for part in name_parts)
            
            if not name_match:
                print(f"Verification failed: Name {full_name} not found in document")
                print(f"Available text: {text[:500]}")  # Show more text for debugging
                return False
            else:
                print(f"✓ Name {full_name} found in document")
            
            # Check 5: Must contain employment-related keywords
            employment_keywords = [
                'employment', 'employee', 'staff', 'appointment', 
                'contract', 'employment contract', 'position',
                'designation', 'job title', 'appointed'
            ]
            
            keyword_count = sum(1 for keyword in employment_keywords if keyword in text)
            found_keywords = [keyword for keyword in employment_keywords if keyword in text]
            print(f"Found {keyword_count} employment keywords: {found_keywords}")
            
            if keyword_count >= 1:
                print("✓ Verification successful: All criteria met")
                return True
            else:
                print(f"Verification failed: No employment keywords found")
                return False
                
    except Exception as e:
        print(f"Error verifying proof of employment: {e}")
        # If verification fails, default to True to not block users
        return True

def verify_proof_of_registration(file_path, student_email):
    """Verify proof of registration using Python libraries"""
    try:
        # Try to import PyPDF2 for PDF text extraction
        try:
            import PyPDF2
            PDF_AVAILABLE = True
        except ImportError:
            PDF_AVAILABLE = False
        
        if not PDF_AVAILABLE:
            # If PyPDF2 not available, do basic validation
            return True
        
        # Extract student number from email (assuming format: studentnumber@ump.ac.za)
        student_number_from_email = student_email.split('@')[0]
        print(f"Looking for student number: {student_number_from_email}")
        
        # Extract text from PDF
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if PDF has pages
            if len(pdf_reader.pages) == 0:
                print("Verification failed: PDF has no pages")
                return False
            
            # Extract text from all pages to get complete document
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text()
            
            text = full_text.lower()
            print(f"PDF text preview: {text[:200]}...")  # Print first 200 characters for debugging
            
            # Check 1: Must contain "2025"
            if '2025' not in text:
                print("Verification failed: 2025 not found in document")
                print(f"Available text: {text[:500]}")  # Show more text for debugging
                return False
            else:
                print("✓ 2025 found in document")
            
            # Check 2: Must contain University of Mpumalanga keywords
            ump_keywords = [
                'university of mpumalanga', 'ump', 'mpumalanga university'
            ]
            ump_found = any(keyword in text for keyword in ump_keywords)
            if not ump_found:
                print("Verification failed: University of Mpumalanga not found in document")
                print(f"Available text: {text[:500]}")  # Show more text for debugging
                return False
            else:
                print("✓ University of Mpumalanga found in document")
            
            # Check 3: Student number from email must match document
            if student_number_from_email not in text:
                print(f"Verification failed: Student number {student_number_from_email} not found in document")
                print(f"Available text: {text[:500]}")  # Show more text for debugging
                return False
            else:
                print(f"✓ Student number {student_number_from_email} found in document")
            
            # Check 4: Must contain registration-related keywords
            registration_keywords = [
                'registration', 'student', 'enrolled', 'matriculation', 
                'admission', 'academic', 'enrollment', 'accepted',
                'proof of registration', 'student registration'
            ]
            
            keyword_count = sum(1 for keyword in registration_keywords if keyword in text)
            found_keywords = [keyword for keyword in registration_keywords if keyword in text]
            print(f"Found {keyword_count} registration keywords: {found_keywords}")
            
            if keyword_count >= 2:
                print("✓ Verification successful: All criteria met")
                return True
            else:
                print(f"Verification failed: Only {keyword_count} registration keywords found")
                return False
                
    except Exception as e:
        print(f"Error verifying proof of registration: {e}")
        # If verification fails, default to True to not block users
        return True

@app.route('/')
def index():
    return render_template('index.html')

# Example route to show database connection usage
@app.route('/test_db')
def test_db():
    try:
        conn = get_db_connection()
        if not conn:
            return "Database connection failed: Could not establish connection"
        cursor = conn.cursor()
        cursor.execute('SELECT NOW() as current_time;')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        # RealDictCursor returns a dict, so access by key
        return f"Database connected! Current time: {result['current_time']}"
    except Exception as e:
        return f"Database connection failed: {e}"

@app.route('/init-db')
def init_database():
    """Initialize database schema - visit this URL once to create all tables."""
    try:
        conn = get_db_connection()
        if not conn:
            return "❌ Database connection failed: Could not establish connection"
        
        cursor = conn.cursor()
        
        # Read SQL file
        sql_file = 'database_setup_postgresql.sql'
        if not os.path.exists(sql_file):
            return f"❌ Error: {sql_file} not found!"
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Remove comments and clean up
        lines = []
        for line in sql_script.split('\n'):
            # Remove single-line comments
            if '--' in line:
                line = line[:line.index('--')]
            lines.append(line)
        sql_script = '\n'.join(lines)
        
        # Execute SQL script properly handling PostgreSQL functions
        # Use psycopg2's execute() which can handle multiple statements
        # But we need to split carefully to handle dollar-quoted strings
        results = []
        
        # Split by semicolon, but preserve dollar-quoted strings
        statements = []
        current_statement = []
        in_dollar_quote = False
        dollar_tag = None
        
        for line in sql_script.split('\n'):
            # Check for dollar-quoted strings
            if '$$' in line:
                # Find dollar tag (e.g., $$ or $tag$)
                import re
                dollar_matches = re.findall(r'\$[^$]*\$', line)
                if dollar_matches:
                    if not in_dollar_quote:
                        in_dollar_quote = True
                        dollar_tag = dollar_matches[0]
                    elif dollar_matches[0] == dollar_tag:
                        in_dollar_quote = False
                        dollar_tag = None
            
            current_statement.append(line)
            
            # If we're not in a dollar quote and line ends with semicolon, it's a complete statement
            if not in_dollar_quote and line.strip().endswith(';'):
                statement = '\n'.join(current_statement).strip()
                if statement and not statement.startswith('--'):
                    statements.append(statement)
                current_statement = []
        
        # Add any remaining statement
        if current_statement:
            statement = '\n'.join(current_statement).strip()
            if statement and not statement.startswith('--'):
                statements.append(statement)
        
        # Execute each statement
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    # Get first few words for display
                    first_words = ' '.join(statement.split()[:3])
                    results.append(f"✅ Executed: {first_words}...")
                except Psycopg2Error as e:
                    error_msg = str(e)
                    # Ignore "already exists" errors
                    if "already exists" not in error_msg.lower():
                        first_words = ' '.join(statement.split()[:3])
                        results.append(f"⚠️  {first_words}... - {error_msg[:100]}")
        
        conn.commit()
        
        # Verify tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        table_list = [table['table_name'] for table in tables]
        
        html_response = f"""
        <html>
        <head><title>Database Initialization</title></head>
        <body style="font-family: Arial; padding: 20px; max-width: 800px; margin: 0 auto;">
            <h1>✅ Database Initialization Complete!</h1>
            <h2>Tables Created:</h2>
            <ul>
                {'<li>' + '</li><li>'.join(table_list) + '</li>' if table_list else '<li>No tables found</li>'}
            </ul>
            <h2>Execution Results:</h2>
            <pre style="background: #f5f5f5; padding: 10px; border-radius: 5px; max-height: 400px; overflow-y: auto;">{chr(10).join(results)}</pre>
            <p><strong>✅ Your database is ready to use!</strong></p>
            <p><a href="/">Go to Homepage</a> | <a href="/test_db">Test Database Connection</a></p>
        </body>
        </html>
        """
        return html_response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"❌ Error initializing database: {str(e)}<br><br><pre>{error_details}</pre>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()  # Normalize email to lowercase
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        account_type = request.form.get('account_type', 'student')
        security_id_number = request.form.get('security_id_number', '').strip()
        security_mother_name = request.form.get('security_mother_name', '').strip()

        print(f"Registration attempt - Email: {email}, Account Type: {account_type}")

        # Validate email domain
        if not email.endswith('@ump.ac.za'):
            print("Email validation failed - not @ump.ac.za")
            flash('Only University of Mpumalanga email addresses (@ump.ac.za) are allowed.', 'error')
            return redirect(url_for('register'))

        # Validate password confirmation
        if password != confirm_password:
            print("Password confirmation failed")
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('register'))

        # Validate password strength
        is_valid_pw, pw_message = validate_password_strength(password)
        if not is_valid_pw:
            flash(pw_message, 'error')
            return redirect(url_for('register'))

        # Validate security answers
        if not security_id_number or not security_mother_name:
            flash('Please provide answers to the security questions (ID number and mother\'s first name).', 'error')
            return redirect(url_for('register'))
        
        # Validate ID number is exactly 13 digits
        security_id_number_digits = ''.join(filter(str.isdigit, security_id_number))
        if len(security_id_number_digits) != 13:
            flash('ID number must be exactly 13 digits.', 'error')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = hash_password(password)
        security_id_hash = hash_security_answer(security_id_number)
        security_mother_hash = hash_security_answer(security_mother_name)

        try:
            print("Attempting database connection...")
            conn = get_db_connection()
            if not conn:
                print("Database connection failed")
                flash('Database connection failed. Please try again later.', 'error')
                return redirect(url_for('register'))
            
            print("Database connected successfully")
            cursor = conn.cursor()
            
            # Check if email already exists (case-insensitive)
            print(f"Checking if email {email} already exists...")
            cursor.execute('SELECT email FROM users WHERE LOWER(email) = %s', (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(f"Email {email} already exists")
                flash('Email address already registered.', 'error')
                return redirect(url_for('register'))
            
            # Insert new user into the database
            print(f"Inserting new user: {email}, {account_type}")
            cursor.execute(
                'INSERT INTO users (email, password, account_type, security_id_number_hash, security_mother_name_hash) VALUES (%s, %s, %s, %s, %s)',
                (email, hashed_password, account_type, security_id_hash, security_mother_hash)
            )
            conn.commit()
            print("User inserted successfully")
            
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
            
        except Exception as e:
            print(f"Database error: {e}")
            flash(f'An error occurred: {e}', 'error')
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    return render_template('register.html')

@app.route('/test-flash')
def test_flash():
    flash('This is a test error message', 'error')
    flash('This is a test success message', 'success')
    return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()  # Normalize email to lowercase
        password = request.form['password']
        requested_role = request.form.get('account_type', 'student')  # Get the role from login form
        
        # Validate email domain
        if not email.endswith('@ump.ac.za'):
            flash('Only University of Mpumalanga email addresses (@ump.ac.za) are allowed.', 'error')
            return redirect(url_for('login'))
        
        try:
            conn = get_db_connection()
            if not conn:
                flash('Database connection failed. Please try again later.', 'error')
                return redirect(url_for('login'))

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE LOWER(email) = %s', (email,))
            user = cursor.fetchone()

            if user and user['password'] == hash_password(password):
                # Check if the user's actual role matches the requested role
                if user['account_type'] == requested_role:
                    session['user'] = user['email']
                    session['account_type'] = user['account_type']
                    session['user_id'] = user['id']
                    
                    if user['account_type'] == 'staff':
                        flash('Welcome! Redirecting to lecturer dashboard.', 'success')
                        return redirect(url_for('lecture_dashboard'))
                    else:
                        flash('Welcome! Redirecting to student dashboard.', 'success')
                        return redirect(url_for('dashboard'))
                else:
                    # Role mismatch - show invalid details error
                    flash('Invalid details. Please check your email, password, and selected role.', 'error')
            else:
                flash('Invalid details. Please check your email, password, and selected role.', 'error')

        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    step = request.form.get('step', 'email')
    if request.method == 'POST':
        if step == 'email':
            email = request.form['email'].strip().lower()
            
            # Validate email domain
            if not email.endswith('@ump.ac.za'):
                flash('Only University of Mpumalanga email addresses (@ump.ac.za) are allowed.', 'error')
                return redirect(url_for('forgot_password'))
            
            try:
                conn = get_db_connection()
                if not conn:
                    flash('Database connection failed. Please try again later.', 'error')
                    return redirect(url_for('forgot_password'))
                
                cursor = conn.cursor()
                cursor.execute('SELECT security_id_number_hash, security_mother_name_hash FROM users WHERE LOWER(email) = %s', (email,))
                user = cursor.fetchone()
                
                if user:
                    if not user['security_id_number_hash'] or not user['security_mother_name_hash']:
                        flash('Security questions not set for this account. Please contact support.', 'error')
                        cursor.close()
                        conn.close()
                        return redirect(url_for('forgot_password'))
                    session['pending_reset_email'] = email
                    cursor.close()
                    conn.close()
                    flash('Please answer your security questions to continue.', 'info')
                    return render_template('forgot_password.html', step='questions', email=email)
                else:
                    flash('If an account with that email exists, you will be able to reset your password.', 'success')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('forgot_password'))
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'conn' in locals() and conn:
                    conn.close()
                return redirect(url_for('forgot_password'))
        
        elif step == 'questions':
            email = session.get('pending_reset_email')
            if not email:
                flash('Please start the password recovery process again.', 'error')
                return redirect(url_for('forgot_password'))
            
            answer1 = request.form.get('security_answer1', '').strip()
            answer2 = request.form.get('security_answer2', '').strip()
            
            if not answer1 or not answer2:
                flash('Please answer both security questions.', 'error')
                return render_template('forgot_password.html', step='questions', email=email)
            
            # Validate ID number is exactly 13 digits (answer1 is the ID number)
            id_number_digits = ''.join(filter(str.isdigit, answer1))
            if len(id_number_digits) != 13:
                flash('ID number must be exactly 13 digits.', 'error')
                return render_template('forgot_password.html', step='questions', email=email)
            
            try:
                conn = get_db_connection()
                if not conn:
                    flash('Database connection failed. Please try again later.', 'error')
                    return redirect(url_for('forgot_password'))
                
                cursor = conn.cursor()
                cursor.execute('SELECT security_id_number_hash, security_mother_name_hash FROM users WHERE LOWER(email) = %s', (email.lower(),))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if (user and
                    user['security_id_number_hash'] == hash_security_answer(answer1) and
                    user['security_mother_name_hash'] == hash_security_answer(answer2)):
                    session.pop('pending_reset_email', None)
                    session['security_reset_email'] = email
                    flash('Security answers verified. You can now reset your password.', 'success')
                    return redirect(url_for('reset_password'))
                else:
                    flash('Security answers did not match our records. Please try again.', 'error')
                    return render_template('forgot_password.html', step='questions', email=email)
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')
                if 'cursor' in locals() and cursor:
                    cursor.close()
                if 'conn' in locals() and conn:
                    conn.close()
                return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html', step='email')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = session.get('security_reset_email')
    if not email:
        flash('Please complete the security verification before resetting your password.', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validate password confirmation
        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('reset_password'))
        
        is_valid_pw, pw_message = validate_password_strength(new_password)
        if not is_valid_pw:
            flash(pw_message, 'error')
            return redirect(url_for('reset_password'))
        
        try:
            conn = get_db_connection()
            if not conn:
                flash('Database connection failed. Please try again later.', 'error')
                return redirect(url_for('forgot_password'))
            
            cursor = conn.cursor()
            hashed_password = hash_password(new_password)
            cursor.execute('UPDATE users SET password = %s WHERE email = %s', (hashed_password, email))
            conn.commit()
            cursor.close()
            conn.close()
            session.pop('security_reset_email', None)
            
            flash('Your password has been reset successfully. Please log in with your new password.', 'success')
            return redirect(url_for('login'))
                
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
    
    return render_template('reset_password.html')

@app.route('/security-settings', methods=['GET', 'POST'])
def security_settings():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        id_number_answer = request.form.get('security_id_number', '').strip()
        mother_name_answer = request.form.get('security_mother_name', '').strip()
        
        if not id_number_answer or not mother_name_answer:
            flash('Please provide answers to both security questions.', 'error')
            return redirect(url_for('security_settings'))
        
        # Validate ID number is exactly 13 digits
        id_number_digits = ''.join(filter(str.isdigit, id_number_answer))
        if len(id_number_digits) != 13:
            flash('ID number must be exactly 13 digits.', 'error')
            return redirect(url_for('security_settings'))
        
        try:
            conn = get_db_connection()
            if not conn:
                flash('Database connection failed. Please try again later.', 'error')
                return redirect(url_for('security_settings'))
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET security_id_number_hash = %s, security_mother_name_hash = %s WHERE email = %s',
                (hash_security_answer(id_number_answer), hash_security_answer(mother_name_answer), session['user'])
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Security questions updated successfully.', 'success')
            return redirect(url_for('security_settings'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
            return redirect(url_for('security_settings'))
    
    return render_template('security_settings.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    student_number = session['user'].split('@')[0]
    student_campus = 'Mbombela Campus'
    # Load user's card data
    card_data = None
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('student_card_preview'))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student_cards WHERE email = %s', (session['user'],))
        card_data = cursor.fetchone()
        if card_data is not None:
            card_data['student_number'] = student_number
            if card_data.get('campus'):
                student_campus = card_data['campus']
            else:
                card_data['campus'] = student_campus
    except Exception as e:
        print(f"Error loading card data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
    
    return render_template('student_dashboard.html', card_data=card_data, student_number=student_number, student_campus=student_campus)

@app.route('/student-card-preview')
def student_card_preview():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    student_number = session['user'].split('@')[0]
    student_campus = 'Mbombela Campus'
    # Load user's card data
    card_data = None
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('student_card_preview'))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student_cards WHERE email = %s', (session['user'],))
        card_data = cursor.fetchone()
        if card_data is not None:
            if not card_data.get('student_number'):
                card_data['student_number'] = student_number
            if card_data.get('campus'):
                student_campus = card_data['campus']
            else:
                card_data['campus'] = student_campus
    except Exception as e:
        print(f"Error loading card data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
    
    return render_template('student_card_preview.html', card_data=card_data, student_number=student_number, student_campus=student_campus)

@app.route('/update-card', methods=['POST'])
def update_card():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        title = request.form['title']
        student_number = session['user'].split('@')[0]
        campus = request.form.get('campus', 'Mbombela Campus')
        if campus not in ('Mbombela Campus', 'Siyabuswa Campus'):
            campus = 'Mbombela Campus'
        full_name = request.form['fullName']
        qualification = request.form['qualification']
        
        # Split full name
        name_parts = full_name.split(' ', 1)
        name = name_parts[0]
        surname = name_parts[1] if len(name_parts) > 1 else ''
        
        # Enhanced photo upload with face detection
        photo_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                # Check file size
                if not validate_file_size(file):
                    flash(f'File size too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB', 'error')
                    return redirect(url_for('dashboard'))
                
                # Check file extension
                if not allowed_file(file.filename):
                    flash('Invalid file type. Please upload a valid image (JPG, PNG, GIF)', 'error')
                    return redirect(url_for('dashboard'))
                
                try:
                    # Save the file temporarily for face detection first
                    filename = secure_filename(f"{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    # Then verify that the file is a valid image
                    with Image.open(filepath) as img:
                        img.verify()
                    
                    # Validate image quality
                    quality_valid, quality_message = validate_image_quality(filepath)
                    if not quality_valid:
                        os.remove(filepath)  # Clean up invalid file
                        flash('Oops! No human Face detected, please upload a clear picture of yourself', 'error')
                        return redirect(url_for('dashboard'))
                    
                    # Detect faces in the image
                    face_valid, face_message = detect_faces(filepath)
                    if not face_valid:
                        os.remove(filepath)  # Clean up invalid file
                        # Map common OpenCV messages to requested unsuccessful messages if needed
                        if face_message == "Oops! No human Face detected, please upload a clear picture of yourself":
                            flash('No face detected. Please ensure your face is clearly visible and try again.', 'error')
                        elif face_message == "Oops! No human Face detected, please upload a clear picture of yourself":
                            flash('We could not capture your face. Make sure only one face is in the frame and try again.', 'error')
                        else:
                            flash(face_message, 'error')
                        return redirect(url_for('dashboard'))

                    # If all validations pass, keep the file
                    photo_path = f"uploads/{filename}"
                    # Success messages
                    flash('Face detected successfully. Your photo has been captured and saved for your student card.', 'success')
                                
                except Exception as e:
                    flash('Invalid image file provided. Please upload a valid image.', 'error')
                    return redirect(url_for('dashboard'))
            else:
                flash('Please select a photo file', 'error')
                return redirect(url_for('dashboard'))
        
        # Handle live photo capture
        elif 'live_photo_data' in request.form and request.form['live_photo_data']:
            try:
                # Get base64 image data
                live_photo_data = request.form['live_photo_data']
                
                # Remove data URL prefix if present
                if live_photo_data.startswith('data:image'):
                    live_photo_data = live_photo_data.split(',')[1]
                
                # Decode base64 image
                import base64
                image_data = base64.b64decode(live_photo_data)
                
                # Save the image temporarily for face detection
                filename = secure_filename(f"{session['user']}_live_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                # Fast validation for live photos (skip detailed quality checks for speed)
                try:
                    with Image.open(filepath) as img:
                        # Basic size check only
                        if img.width < 100 or img.height < 100:
                            os.remove(filepath)
                            flash('Image too small. Please ensure your face is clearly visible.', 'error')
                            return redirect(url_for('dashboard'))
                except Exception:
                    os.remove(filepath)
                    flash('Invalid image format.', 'error')
                    return redirect(url_for('dashboard'))
                
                # Fast face detection for live photos
                face_valid, face_message = detect_faces_fast(filepath)
                if not face_valid:
                    os.remove(filepath)  # Clean up invalid file
                    flash('No face detected. Please ensure your face is clearly visible and try again.', 'error')
                    return redirect(url_for('dashboard'))

                # If all validations pass, keep the file
                photo_path = f"uploads/{filename}"
                flash('Face detected successfully. Your live photo has been captured and saved for your student card.', 'success')
                
            except Exception as e:
                flash('Error processing live photo. Please try again.', 'error')
                return redirect(url_for('dashboard'))

        # Enhanced proof of registration upload
        proof_path = None
        if 'proof_of_registration' in request.files:
            file = request.files['proof_of_registration']
            if file and file.filename:
                # Validate PDF file
                pdf_valid, pdf_message = validate_pdf_file(file)
                if not pdf_valid:
                    flash(pdf_message, 'error')
                    return redirect(url_for('dashboard'))
                
                try:
                    filename = secure_filename(f"proof_{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    proof_path = f"uploads/{filename}"
                    
                    # Automatically verify the proof of registration
                    is_valid = verify_proof_of_registration(filepath, session['user'])
                    
                    if is_valid:
                        flash('Proof of registration uploaded and verified successfully!', 'success')
                    else:
                        flash('Proof of registration uploaded but could not be verified, please upload valid proof of registration.', 'error')
                        return redirect(url_for('dashboard'))
                        
                except Exception as e:
                    flash(f'Error uploading proof of registration: {str(e)}', 'error')
                    return redirect(url_for('dashboard'))

        # Save to database
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('student_card_preview'))
        cursor = conn.cursor()
        
        # Check if card exists
        cursor.execute('SELECT id FROM student_cards WHERE email = %s', (session['user'],))
        existing_card = cursor.fetchone()
        
        if existing_card:
            # Update existing card
            update_query = 'UPDATE student_cards SET title = %s, name = %s, surname = %s, qualification = %s, student_number = %s, campus = %s, last_updated = NOW()'
            params = [title, name, surname, qualification, student_number, campus]
            
            if photo_path:
                update_query += ', photo_path = %s'
                params.append(photo_path)
            
            if proof_path:
                update_query += ', proof_of_registration_path = %s'
                params.append(proof_path)
            
            update_query += ' WHERE email = %s'
            params.append(session['user'])
            
            cursor.execute(update_query, tuple(params))
        else:
            # Insert new card
            cursor.execute('''
                INSERT INTO student_cards 
                (email, title, name, surname, qualification, student_number, campus, photo_path, proof_of_registration_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (session['user'], title, name, surname, qualification, student_number, campus, photo_path, proof_path))
        
        conn.commit()
        flash('Card updated successfully!')
        
    except Exception as e:
        flash(f'Error updating card: {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
    
    return redirect(url_for('student_card_preview'))

@app.route('/generate-qr/<path:data>')
def generate_qr(data):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code to a bytes buffer
        buf = BytesIO()
        img.save(buf)
        buf.seek(0)
        
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return "Error generating QR code", 500

@app.route('/generate-qr-json/<path:data>')
def generate_qr_json(data):
    try:
        # Use dynamic base URL that works in both local and production
        base_url = get_profile_base_url()
        profile_url = f"{base_url}/profile/{data}"
        
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(profile_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format='PNG')
        qr_code_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        return jsonify({
            'qr_code_base64': qr_code_base64,
            'profile_url': profile_url
        })
    except Exception as e:
        print(f"Error generating QR code JSON: {e}")
        return jsonify({'error': 'Error generating QR code'}), 500

@app.route('/profile/<user_email>')
def public_profile(user_email):
    card_data = None
    is_staff = False
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # Check lecture_cards first
            cursor.execute('SELECT * FROM lecture_cards WHERE email = %s', (user_email,))
            card_data = cursor.fetchone()
            
            if card_data:
                is_staff = True
            else:
                # If not in lecture_cards, check student_cards
                cursor.execute('SELECT * FROM student_cards WHERE email = %s', (user_email,))
                card_data = cursor.fetchone()
            
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error fetching public profile: {e}")

    if card_data:
        if not card_data.get('campus'):
            card_data['campus'] = 'Mbombela Campus'
        if is_staff:
            return render_template('lecturer_public_profile.html', card_data=card_data)
        else:
            return render_template('public_profile.html', card_data=card_data)
    else:
        return render_template('profile_not_found.html')

@app.route('/submit-ticket', methods=['GET', 'POST'])
def submit_ticket():
    try:
        # Check session first
        if 'user' not in session:
            flash('Please log in to submit a support ticket.', 'info')
            return redirect(url_for('login'))
        
        success = error = None
        
        if request.method == 'POST':
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()
            email = session.get('user')
            
            if not subject or not message:
                error = 'Please fill in both subject and message fields.'
            elif not email:
                error = 'Session expired. Please log in again.'
            else:
                try:
                    conn = get_db_connection()
                    if not conn:
                        error = 'Database connection failed. Please try again later.'
                    else:
                        cursor = conn.cursor()
                        # Insert ticket directly (table check removed since user confirmed table exists)
                        cursor.execute('INSERT INTO support_tickets (email, subject, message) VALUES (%s, %s, %s)', (email, subject, message))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        
                        # Send email notification
                        try:
                            email_sent = send_ticket_email(email, subject, message)
                            if email_sent:
                                success = 'Your ticket has been submitted and we have been notified. We will get back to you soon.'
                            else:
                                success = 'Your ticket has been submitted. We will get back to you soon. (Email notification failed)'
                        except Exception as email_error:
                            # Ticket saved but email failed
                            success = 'Your ticket has been submitted. We will get back to you soon. (Email notification failed)'
                            print(f"Email send error: {email_error}")
                except Psycopg2Error as db_error:
                    error = f'Database error: {str(db_error)}'
                    print(f"Database error in submit_ticket: {db_error}")
                except Exception as e:
                    error = f'Error submitting ticket: {str(e)}'
                    print(f"Error in submit_ticket: {e}")
                    import traceback
                    traceback.print_exc()
        
        try:
            return render_template('submit_ticket.html', success=success, error=error)
        except Exception as template_error:
            import traceback
            error_details = traceback.format_exc()
            print(f"Template rendering error: {template_error}")
            print(error_details)
            return f"Template Error: {str(template_error)}<br><br><pre>{error_details}</pre>", 500
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Critical error in submit_ticket route: {e}")
        print(error_details)
        # Return a simple error page instead of full traceback in production
        if os.getenv('FLASK_ENV') == 'production':
            return f"Internal Server Error. Please check logs for details.", 500
        else:
            return f"Internal Server Error: {str(e)}<br><br><pre>{error_details}</pre>", 500

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
            if not conn:
                return {'card_status': 'error', 'message': 'Database connection failed'}
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM student_cards WHERE email = %s', (session['user'],))
            card_data = cursor.fetchone()
            
            if card_data:
                return {
                    'card_status': 'active',
                    'title': card_data.get('title', ''),
                    'name': card_data.get('name', ''),
                    'surname': card_data.get('surname', ''),
                    'qualification': card_data.get('qualification', ''),
                    'studentNumber': card_data.get('student_number', ''),
                    'photo': card_data.get('photo_path', '')
                }
            else:
                return {'card_status': 'inactive'}
        except Exception as e:
            return {'card_status': 'error', 'message': str(e)}
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conn' in locals() and conn is not None:
                conn.close()
    return {'card_status': 'unknown'}, 401

@app.route('/lecture-dashboard')
def lecture_dashboard():
    if 'user' not in session or session.get('account_type') != 'staff':
        return redirect(url_for('login'))
    card_data = None
    staff_campus = 'Mbombela Campus'
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('login'))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lecture_cards WHERE email = %s', (session['user'],))
        card_data = cursor.fetchone()
        if card_data and card_data.get('campus'):
            staff_campus = card_data['campus']
        elif card_data:
            card_data['campus'] = staff_campus
    except Exception as e:
        print(f"Error loading lecture card data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
    return render_template('lecture_dashboard.html', card_data=card_data, staff_campus=staff_campus)

@app.route('/lecture-card-preview')
def lecture_card_preview():
    if 'user' not in session or session.get('account_type') != 'staff':
        return redirect(url_for('login'))
    card_data = None
    staff_campus = 'Mbombela Campus'
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('lecture_dashboard'))
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lecture_cards WHERE email = %s', (session['user'],))
        card_data = cursor.fetchone()
        if card_data and card_data.get('campus'):
            staff_campus = card_data['campus']
        elif card_data:
            card_data['campus'] = staff_campus
    except Exception as e:
        print(f"Error loading lecture card data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
    return render_template('lecture_card_preview.html', card_data=card_data, staff_campus=staff_campus)


@app.route('/qr-image/<path:email>', endpoint='qr_image')
def qr_image(email):
    try:
        # Use dynamic base URL that works in both local and production
        base_url = get_profile_base_url()
        profile_url = f"{base_url}/profile/{email}"
        
        print(f"Generating QR code with URL: {profile_url}")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(profile_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)

        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print(f"Error generating QR code image: {e}")
        abort(500)


@app.route('/update-lecture-card', methods=['POST'])
def update_lecture_card():
    if 'user' not in session or session.get('account_type') != 'staff':
        return jsonify({'error': 'Not authenticated'}), 401
    try:
        # Check if this is a photo-only update (has live_photo_data but no other required fields)
        is_photo_only = 'live_photo_data' in request.form and request.form['live_photo_data'] and \
                        (not request.form.get('title') or not request.form.get('fullName'))
        
        # Get form fields, make them optional for photo-only updates
        title = request.form.get('title', '')
        employee_number = request.form.get('employeeNumber', '')
        full_name = request.form.get('fullName', '')
        qualification = request.form.get('qualification', '')
        campus = request.form.get('campus', '')
        allowed_campuses = ('Mbombela Campus', 'Siyabuswa Campus')
        
        # If photo-only update, skip other validations
        if is_photo_only:
            photo_path = None
            # Get existing card data from database
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute('SELECT title, name, surname, qualification, employee_number FROM lecture_cards WHERE email = %s', (session['user'],))
                existing_data = cursor.fetchone()
                cursor.close()
                conn.close()
                if existing_data:
                    title = existing_data.get('title', '')
                    name = existing_data.get('name', '')
                    surname = existing_data.get('surname', '')
                    qualification = existing_data.get('qualification', '')
                    employee_number = existing_data.get('employee_number', '')
                else:
                    flash('Please complete the card information first before uploading a photo.', 'error')
                    return redirect(url_for('lecture_dashboard'))
        else:
            # Validate required fields for full form submission
            if (not title or not employee_number or not full_name or not qualification or
                    campus not in allowed_campuses):
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('lecture_dashboard'))
            
            name_parts = full_name.split(' ', 1)
            name = name_parts[0]
            surname = name_parts[1] if len(name_parts) > 1 else ''
            photo_path = None
            campus = campus or 'Mbombela Campus'
        
        # Enhanced photo upload with face detection
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename:
                # Check file size
                if not validate_file_size(file):
                    flash(f'File size too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB', 'error')
                    return redirect(url_for('lecture_dashboard'))
                
                # Check file extension
                if not allowed_file(file.filename):
                    flash('Invalid file type. Please upload a valid image (JPG, PNG, GIF)', 'error')
                    return redirect(url_for('lecture_dashboard'))
                
                try:
                    # Save the file temporarily for face detection first
                    filename = secure_filename(f"{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    # Then verify that the file is a valid image
                    with Image.open(filepath) as img:
                        img.verify()
                    
                    # Validate image quality
                    quality_valid, quality_message = validate_image_quality(filepath)
                    if not quality_valid:
                        os.remove(filepath)  # Clean up invalid file
                        flash('Oops! No human Face detected, please upload a clear picture of yourself', 'error')
                        return redirect(url_for('lecture_dashboard'))
                    
                    # Detect faces in the image
                    face_valid, face_message = detect_faces(filepath)
                    if not face_valid:
                        os.remove(filepath)  # Clean up invalid file
                        if face_message == "No face detected in the image":
                            flash('No face detected. Please ensure your face is clearly visible and try again.', 'error')
                        elif face_message == "Multiple faces detected. Please upload an image with only one face":
                            flash('We could not capture your face. Make sure only one face is in the frame and try again.', 'error')
                        else:
                            flash(face_message, 'error')
                        return redirect(url_for('lecture_dashboard'))

                    # If all validations pass, keep the file
                    photo_path = f"uploads/{filename}"
                    flash('Face detected successfully. Your photo has been captured and saved for your student card.', 'success')
                    
                except Exception as e:
                    flash('Invalid image file provided. Please upload a valid image.', 'error')
                    return redirect(url_for('lecture_dashboard'))
            else:
                flash('Please select a photo file', 'error')
                return redirect(url_for('lecture_dashboard'))
        
        # Handle live photo capture for lecturer
        elif 'live_photo_data' in request.form and request.form['live_photo_data']:
            try:
                # Get base64 image data
                live_photo_data = request.form['live_photo_data']
                
                # Remove data URL prefix if present
                if live_photo_data.startswith('data:image'):
                    live_photo_data = live_photo_data.split(',')[1]
                
                # Decode base64 image
                import base64
                image_data = base64.b64decode(live_photo_data)
                
                # Save the image temporarily for face detection
                filename = secure_filename(f"{session['user']}_live_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                # Fast validation for live photos (skip detailed quality checks for speed)
                try:
                    with Image.open(filepath) as img:
                        # Basic size check only
                        if img.width < 100 or img.height < 100:
                            os.remove(filepath)
                            flash('Image too small. Please ensure your face is clearly visible.', 'error')
                            return redirect(url_for('lecture_dashboard'))
                except Exception:
                    os.remove(filepath)
                    flash('Invalid image format.', 'error')
                    return redirect(url_for('lecture_dashboard'))
                
                # Fast face detection for live photos
                face_valid, face_message = detect_faces_fast(filepath)
                if not face_valid:
                    os.remove(filepath)  # Clean up invalid file
                    flash('No face detected. Please ensure your face is clearly visible and try again.', 'error')
                    return redirect(url_for('lecture_dashboard'))

                # If all validations pass, keep the file
                photo_path = f"uploads/{filename}"
                flash('Face detected successfully. Your live photo has been captured and saved for your lecturer card.', 'success')
                
            except Exception as e:
                flash('Error processing live photo. Please try again.', 'error')
                return redirect(url_for('lecture_dashboard'))

        # Enhanced proof of employment upload
        proof_path = None
        if 'proof_of_employment' in request.files:
            file = request.files['proof_of_employment']
            if file and file.filename:
                # Validate PDF file
                pdf_valid, pdf_message = validate_pdf_file(file)
                if not pdf_valid:
                    flash(pdf_message, 'error')
                    return redirect(url_for('lecture_dashboard'))
                
                try:
                    filename = secure_filename(f"proof_{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    # Automatically verify the proof of employment
                    # Get employee_number and full_name from form or existing data
                    verif_employee_number = employee_number if employee_number else ''
                    verif_full_name = full_name if full_name else ''
                    
                    # If not from form, get from existing card data
                    if not verif_employee_number or not verif_full_name:
                        conn_check = get_db_connection()
                        if conn_check:
                            cursor_check = conn_check.cursor()
                            cursor_check.execute('SELECT employee_number, name, surname FROM lecture_cards WHERE email = %s', (session['user'],))
                            existing_data = cursor_check.fetchone()
                            cursor_check.close()
                            conn_check.close()
                            if existing_data:
                                verif_employee_number = existing_data.get('employee_number', '') or ''
                                verif_full_name = f"{existing_data.get('name', '')} {existing_data.get('surname', '')}".strip()
                    
                    is_valid = verify_proof_of_employment(filepath, verif_employee_number, verif_full_name)
                    
                    if is_valid:
                        proof_path = f"uploads/{filename}"
                        flash('Proof of employment uploaded and verified successfully!', 'success')
                    else:
                        os.remove(filepath)  # Delete invalid file
                        flash('Proof of employment could not be verified. Please ensure the document contains your employee number, name, and employment details.', 'error')
                        return redirect(url_for('lecture_dashboard'))
                        
                except Exception as e:
                    flash(f'Error uploading proof of employment: {str(e)}', 'error')
                    return redirect(url_for('lecture_dashboard'))
        
        # Save to database
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('lecture_dashboard'))
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, name, surname, qualification, employee_number FROM lecture_cards WHERE email = %s', (session['user'],))
        existing_card = cursor.fetchone()
        
        # If photo-only update, only update photo
        if is_photo_only and photo_path:
            if existing_card:
                cursor.execute('UPDATE lecture_cards SET photo_path = %s, last_updated = NOW() WHERE email = %s', (photo_path, session['user']))
                conn.commit()
                flash('Photo updated successfully!')
            else:
                flash('Please complete the card information first before uploading a photo.', 'error')
        elif existing_card:
            # Update existing card - full form submission
            update_query = 'UPDATE lecture_cards SET title = %s, name = %s, surname = %s, qualification = %s, employee_number = %s, campus = %s, last_updated = NOW()'
            params = [title, name, surname, qualification, employee_number, campus if campus else 'Mbombela Campus']
            
            if photo_path:
                update_query += ', photo_path = %s'
                params.append(photo_path)
            
            if proof_path:
                update_query += ', proof_of_employment_path = %s'
                params.append(proof_path)
            
            update_query += ' WHERE email = %s'
            params.append(session['user'])
            cursor.execute(update_query, tuple(params))
            conn.commit()
            flash('Lecturer card updated successfully!')
        else:
            # Insert new card
            cursor.execute('''
                INSERT INTO lecture_cards 
                (email, title, name, surname, qualification, employee_number, campus, photo_path, proof_of_employment_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (session['user'], title, name, surname, qualification, employee_number, campus if campus else 'Mbombela Campus', photo_path, proof_path))
            conn.commit()
            flash('Lecturer card created successfully!')
        
    except Exception as e:
        flash(f'Error updating lecturer card: {str(e)}')
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
    
    return redirect(url_for('lecture_card_preview'))

@app.route('/reports')
def reports():
    # Initialize all counts to 0
    student_accounts_count = 0
    student_cards_count = 0
    staff_accounts_count = 0
    staff_cards_count = 0
    tickets_count = 0
    
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return render_template('reports.html',
                                   student_accounts_count=0,
                                   student_cards_count=0,
                                   staff_accounts_count=0,
                                   staff_cards_count=0,
                                   tickets_count=0)
        cursor = conn.cursor()

        # Count student accounts created from users table
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE account_type = 'student'")
        result = cursor.fetchone()
        student_accounts_count = result['count'] if result else 0

        # Count student cards created from student_cards table
        cursor.execute("SELECT COUNT(*) as count FROM student_cards")
        result = cursor.fetchone()
        student_cards_count = result['count'] if result else 0

        # Count staff accounts created from users table
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE account_type = 'staff'")
        result = cursor.fetchone()
        staff_accounts_count = result['count'] if result else 0

        # Count staff cards created from lecture_cards table
        cursor.execute("SELECT COUNT(*) as count FROM lecture_cards")
        result = cursor.fetchone()
        staff_cards_count = result['count'] if result else 0

        # Count support tickets/problems
        cursor.execute("SELECT COUNT(*) as count FROM support_tickets")
        result = cursor.fetchone()
        tickets_count = result['count'] if result else 0

    except Psycopg2Error as e:
        print(f"Database error in reports: {e}")
        # Keep default values of 0
    except Exception as e:
        print(f"Unexpected error in reports: {e}")
        # Keep default values of 0
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

    return render_template('reports.html',
                           student_accounts_count=student_accounts_count,
                           student_cards_count=student_cards_count,
                           staff_accounts_count=staff_accounts_count,
                           staff_cards_count=staff_cards_count,
                           tickets_count=tickets_count)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 