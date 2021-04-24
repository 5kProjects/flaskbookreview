from flask_sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=True)
    # GenreId = db.Column(db.Integer, db.ForeignKey("Dinners.DinnerID"), nullable=False)
    year = db.Column(db.Integer)
    review_count = db.Column(db.Integer)
    average_reviews = db.Column(db.Float)

    def __init__(self, title, author, isbn, year):
        self.author = author
        self.title = title
        self.isbn = isbn
        self.year = year


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User({self.id},{self.username}, {self.email})"

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=True)
    date = db.Column(db.String(10), nullable=True)

    def __init__(self, userid, book_id, rating, review):
        self.user_id = userid
        self.book_id = book_id
        self.review = review
        self.rating = rating

