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
    engine = create_engine("postgresql://postgres:54123@localhost:5432/books_review")
else:
    engine = create_engine(
        "postgres://dypeyfmtlsqzch:5c0ade7490e67d160ff0c82ac81d6be83da3dc3d21240a367cc349c1c650b978@ec2-54-74-14-109.eu-west-1.compute.amazonaws.com:5432/dbo1skik9jhquo")

db = scoped_session(sessionmaker(bind=engine))


dbs = SQLAlchemy(app)