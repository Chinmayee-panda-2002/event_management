from hashlib import sha256
import os

from dotenv import load_dotenv
from flask_mail import Mail, Message
mail=None

def init_sso(mail_instance):
    global mail
    mail = mail_instance

load_dotenv()
def hash_password(password: str) -> str:
    """
    Hashes a password using a secure hash algorithm combined with a secret key.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    return sha256((password +  os.environ.get("SECRET_KEY")).encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def send_reset_email(email, reset_url):
    try:
        msg = Message("Password Reset Request", recipients=[email])
        msg.body = f"Please click the link to reset your password: {reset_url}"
        msg.html = f"""
        <h3>Password Reset Request</h3>
        <p>Dear User,</p>
        <p>You have requested a password reset. Click the link below to reset your password:</p>
        <p><a href="{reset_url}">Reset Password</a></p>
        <p>If you did not request this, please ignore this email.</p>
        """
        mail.send(msg)
        print(f"Password reset email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise