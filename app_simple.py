from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key'  # Needed for session management

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Simple registration - just redirect to login
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        account_type = request.form['account_type']
        
        # Simple validation
        if not email or '@' not in email:
            flash('Please enter a valid email address!')
            return render_template('login.html')
        
        if not password or len(password) < 3:
            flash('Password must be at least 3 characters long!')
            return render_template('login.html')
        
        # For demo purposes, accept any valid email/password combination
        # In a real app, you'd check against a database
        session['user'] = email
        session['account_type'] = account_type
        session['user_id'] = 1  # Temporary user ID
        flash('Login successful!')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('student_dashboard.html', card_data=None)

@app.route('/student-card-preview')
def student_card_preview():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('student_card_preview.html', card_data=None)

@app.route('/update-card', methods=['POST'])
def update_card():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Simple card update - just redirect to preview
    flash('Card updated successfully!')
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
        return {'card_status': 'inactive'}
    return {'authenticated': False}, 401

if __name__ == '__main__':
    app.run(debug=True) 