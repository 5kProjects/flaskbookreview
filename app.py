from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# import os
# from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from forms import BookForm
from models import Book, Review, User

app = Flask(__name__)
app.config['SECRET_KEY'] = '7ff61fae7049489'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:54123@localhost:5432/books_review'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database

engine = create_engine("postgresql://postgres:54123@localhost:5432/books_review")
db = scoped_session(sessionmaker(bind=engine))




@app.route("/")
def index():
    return "Project One: TDO"


books = []


@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookForm()
    if request.method == 'POST' and form.validate_on_submit():
        db.execute("INSERT INTO books (title, author) VALUES (:title, :author);",
                   {"title": form.title.data, 'author': form.author.data})
        db.commit()
        data = Book(form.title.data, form.author.data, form.isbn.data, form.year.data, )


    return render_template('book.html', form=form, book=book)





if __name__ =='__main__':
    with app.app_context():
        db.create_all()
        # main()/