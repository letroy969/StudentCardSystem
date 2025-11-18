pip install Flask Flask-Mail python-dotenv itsdangerous Werkzeug

1️⃣ Install tools
pip install Flask Flask-Mail python-dotenv itsdangerous Werkzeug

2️⃣ .env
SECRET_KEY=any_random_string
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com

3️⃣ app.py — COMPLETE PASSWORD RESET LOGIC
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Email config
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

# Token generator
serializer = URLSafeTimedSerializer(app.secret_key)

# Fake database (replace with real)
users = {
    "test@example.com": {"password": generate_password_hash("1234")}
}

🔵 A) REQUEST PASSWORD RESET

User enters their email → You send them a reset link

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    email = request.json.get("email")

    if email not in users:
        return jsonify({"error": "Email not found"}), 404

    token = serializer.dumps(email, salt="password-reset")

    reset_link = url_for("reset_password", token=token, _external=True)

    msg = Message("Password Reset Request", recipients=[email])
    msg.html = render_template("reset_email.html", reset_link=reset_link)

    mail.send(msg)

    return jsonify({"message": "Reset link sent to your email"})

🔵 B) RESET PASSWORD PAGE

User clicks the link → sees reset form

@app.route("/reset-password/<token>", methods=["GET"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="password-reset", max_age=3600)
    except:
        return "Token expired or invalid", 400

    return render_template("reset_form.html", email=email, token=token)

🔵 C) SAVE NEW PASSWORD

User submits new password

@app.route("/reset-password/<token>", methods=["POST"])
def save_new_password(token):
    try:
        email = serializer.loads(token, salt="password-reset", max_age=3600)
    except:
        return "Token expired or invalid", 400

    new_password = request.form.get("password")
    users[email]["password"] = generate_password_hash(new_password)

    return "Password reset successful!"

4️⃣ Email Template (HTML)

templates/reset_email.html

<h2>Password Reset</h2>
<p>Click the link below to reset your password:</p>
<p><a href="{{ reset_link }}">Reset Password</a></p>
<p>This link expires in 1 hour.</p>

5️⃣ Reset Form (HTML)

templates/reset_form.html

<form action="/reset-password/{{ token }}" method="POST">
    <label>New Password:</label><br>
    <input type="password" name="password" required><br><br>
    <button type="submit">Save New Password</button>
</form>

🔐 SECURITY FEATURES INCLUDED

✔ Token expires after 1 hour
✔ Token tied to user's email
✔ Hashed passwords, NOT plain text
✔ Server-side email sending
✔ Safe reset URLs like:

https://your-domain/reset-password/ASDJKASDJKAS123123