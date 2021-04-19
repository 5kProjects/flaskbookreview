import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from forms import BookForm

app = Flask(__name__)
app.config['SECRET_KEY']='7ff61fae7049489'

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project One: TDO"

books = []
@app.route('/book', methods=['GET', 'POST'])
def book():
    form= BookForm()
    if (request.method == 'POST' and form.validate_on_submit()):
        books.append({'title': form.title.data, 'author': form.author.data})
        print("1--",books)
    print("2--",books)

    return render_template('book.html', form = form, books=books)
    