from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# import os
# from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from forms import BookForm
# from models import Book, Review, User

app = Flask(__name__)
app.config['SECRET_KEY'] = '7ff61fae7049489'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
Env = 'prod'
if Env == 'dev':
    engine = create_engine("postgresql://postgres:54123@localhost:5432/books_review")
else:
    engine = create_engine(
        "postgres://dypeyfmtlsqzch:5c0ade7490e67d160ff0c82ac81d6be83da3dc3d21240a367cc349c1c650b978@ec2-54-74-14-109.eu-west-1.compute.amazonaws.com:5432/dbo1skik9jhquo")

db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project One: TDO"


books = []


@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookForm()
    if request.method == 'POST' and form.validate_on_submit():
        engine.execute("INSERT INTO books (title, author) VALUES (:title, :author);",
                       {"title": form.title.data, 'author': form.author.data})
        engine.commit()
        # data = Book(form.title.data, form.author.data, form.isbn.data, form.year.data, )

    return render_template('book.html', form=form)


@app.route("/api", methods=['GET', 'POST'])
def api_book():
    """Retrive info for the book."""
    try:
        books = db.execute("SELECT * FROM books")

        # columns = [column[0] for column in books.discription]

        book=books.fetchall()

    except():
        return jsonify({"error": "some error"}), 404
    print(books)
    print(book)
    if book is None:
        return jsonify({"error": "no book in database"}), 404

    results = []
    for row in book:
       results.append([x for x in row])  # or simply data.append(list(row))


    return {'results':
            results}


if __name__ == '__main__':
    app.run(debug=True)
