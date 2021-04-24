from flask import Flask, render_template, request, jsonify, session, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# import os
# from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from forms import BookForm, ReviewForm, SignupForm

# from models import Book, Review, User
from helpers import login_required, open_library_api

app = Flask(__name__)
app.config['SECRET_KEY'] = '7ff61fae7049489'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
Env = 'dev'
if Env == 'dev':
    engine = create_engine("postgresql://postgres:54123@localhost:5432/books_review")
else:
    engine = create_engine(
        "postgres://dypeyfmtlsqzch:5c0ade7490e67d160ff0c82ac81d6be83da3dc3d21240a367cc349c1c650b978@ec2-54-74-14-109.eu-west-1.compute.amazonaws.com:5432/dbo1skik9jhquo")

db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project One: TDO"


@app.route('/book', methods=['GET', 'POST'])
def create_book():
    form = BookForm()
    if request.method == 'POST' and form.validate_on_submit():
        engine.execute("INSERT INTO books (title, author) VALUES (:title, :author);",
                       {"title": form.title.data, 'author': form.author.data})
        engine.commit()
        # data = Book(form.title.data, form.author.data, form.isbn.data, form.year.data, )
    return render_template('book.html', form=form)




@app.route("/book/<string:isbn>", methods=["GET"])
# @login_required
def book(isbn):
    form=ReviewForm()
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()

    if book is None:
        return render_template("book.html", form = form)

    reviews = db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id=users.id WHERE book_id=:book_id ", {"book_id": book.id}).fetchall()

    current_user_review = db.execute("SELECT * FROM reviews WHERE book_id=:book_id AND user_id=:user_id", {"book_id": book.id, "user_id": session["user_id"]}).fetchone()

    book_extra = open_library_api(isbn)

    if book_extra is not None:
        book = dict(book)
        book.update(book_extra)
    return render_template("book.html", book=book, reviews=reviews, current_user_review=current_user_review, form= form)


@app.route("/review/<string:isbn>", methods=["POST"])
# @login_required
def review(isbn):
    """Save a user review."""
    form = ReviewForm()
    if request.method == 'POST' and form.validate_on_submit():

        review_rating = int(form.Rating.data)

        book = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()

        if book is None:
            return flash("ISBN not found on Database", category="error")

        user_review = db.execute("SELECT * FROM reviews WHERE book_id=:book_id AND user_id=:user_id;",
                                 {"book_id": book.id, "user_id": session["user_id"]}).fetchone()

        if user_review is not None:
            return flash("You've alreadey submitted a review", category="error")

        db.execute("INSERT INTO reviews (user_id, book_id, rating, review) VALUES (:user_id, :book_id, :rating, :review);",
                   {"user_id": session["user_id"], "book_id": book.id, "rating": review_rating, "review": form.review.data})
        db.commit()
        return redirect(url_for("book", isbn=isbn))


@app.route("/search", methods=["GET", "POST"])
# @login_required
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    term = request.form.get("value_searched", None)

    if term == None or term == "":
        flash("You must provide a term to search")
        return render_template("search.html")

    term = "%{}%".format(term)
    books = db.execute("SELECT * FROM books WHERE isbn LIKE :term OR title LIKE :term OR author LIKE :term;",
                       {"term": term}).fetchall()
    if not len(books):
        flash("There is no books")
    return render_template("search.html", books=books)



@app.route("/api/book/<string:isbn>", methods=['GET', 'POST'])
def api_book(isbn):
    try:
        books_curs = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()
        # columns = [column[0] for column in books.discription]
        book_col = books_curs.fetchone()
    except():
        return jsonify({"error": "some error"}), 404
    print(books_curs)
    print(book_col)
    if book_col is None:
        return jsonify({"error": "no book"}), 404

    results = []
    for row in book_col:
        results.append([x for x in row])  # or simply data.append(list(row))

    return {'results': results}


@app.route("/signup", methods=["GET", "POST"])
def register():
    """Register user"""
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        print("post")

        # Query database for username to check that not exist
        user = db.execute("SELECT * FROM users WHERE username = :username;",
                          {"username": form.username.data}).fetchall()
        if user:
            print("user exist")
            return flash("username already taken", category='error')
        if form.password.data != form.confirm.data:
            print("pwd dont match")
            return flash("confirmation and password don't match", category='error')
        else:
            row = db.execute("INSERT INTO users (username, password) VALUES (:username, :password);",
                             {"username": form.username.data, "password": generate_password_hash(form.password.data)})
            print(row)
            db.commit()
            # session["user_id"] = row[0]["id"]
            return redirect("/")
    else:
        print("get method")
        return render_template("signup.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
