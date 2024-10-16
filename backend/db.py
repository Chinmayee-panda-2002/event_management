from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()
