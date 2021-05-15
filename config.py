import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '7ff61fae7049489'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False

# from dotenv import load_dotenv
#
# dotenv_path = join(dirname(__file__), '.env')  # Path to .env file
# load_dotenv(dotenv_path)
# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
# Configure session to use filesystem


Env = 'dev'
if Env == 'dev':
    engine = create_engine(os.getenv('LOCAL_POSTGRES_KEY'))
else:
    engine = create_engine(os.getenv('HEROKU_POSTGRES_KEY'))

db = scoped_session(sessionmaker(bind=engine))


dbs = SQLAlchemy(app)