from flask import Flask
from flask_cors import CORS 
from db import db  
from models import User, EventOrganizer, Event, Ticket  
from dotenv import load_dotenv
import os
from endpoint import endpoint
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from utils import init_sso
def create_app():
    
    load_dotenv()

    app = Flask(__name__, template_folder="./templates")

   
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Ensure this is correct
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable track modifications
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'prateekofficialinvo@gmail.com'  
    app.config['MAIL_PASSWORD'] = 'npkm cpiu hdqw qcix'  
    app.config['MAIL_DEFAULT_SENDER'] = 'prateekofficialinvo@gmail.com'  
    
    db.init_app(app)

    mail = Mail(app)
    init_sso(mail)


    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
   
    CORS(
        app,
        origins=["http://localhost:3001", "*"], 
        methods=["GET", "POST","DELETE","PUT"],
        allow_headers=["Content-Type"],
        supports_credentials=True,
    )

    
    with app.app_context():
        print("______________")
        db.create_all() 


    app.register_blueprint(endpoint)  

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
