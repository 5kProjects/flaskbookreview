from flask_sqlalchemy import SQLAlchemy

from config import dbs


class Book(dbs.Model):
    __tablename__ = 'books'
    id = dbs.Column(dbs.Integer, primary_key=True)  #0
    title = dbs.Column(dbs.String(200), nullable=False)
    author = dbs.Column(dbs.String, nullable=False)
    isbn = dbs.Column(dbs.String, nullable=True) #3
    # GenreId = dbs.Column(dbs.Integer, dbs.ForeignKey("Dinners.DinnerID"), nullable=False)
    year = dbs.Column(dbs.Integer)   #4
    average_reviews = dbs.Column(dbs.Float) #6
    review_count = dbs.Column(dbs.Integer) #5
    ratings_sum = dbs.Column(dbs.Integer) #7

    def __init__(self, ids, title, author, isbn, year, reviewCount=0, average=0, sum=0):
        self.author = author
        self.title = title
        self.isbn = isbn
        self.year = year
        if (ids != 0):
            self.id = ids
        self.review_count=reviewCount
        self.average_reviews=average
        self.ratings_sum=sum

    def __repr__(self):
        return f"Book({self.id},{self.title}, {self.isbn}, {self.author}, {self.year}, {self.review_count}, {self.ratings_sum}, {self.average_reviews})"

    def setReviewCount(self, count):
        self.review_count = count

    def sevReviewSum(self, total):
        self.ratings_sum = total

    def setAverageRating(self, rating):
        self.average_reviews = rating


class User(dbs.Model):
    __tablename__ = 'users'
    id = dbs.Column(dbs.Integer, primary_key=True)
    username = dbs.Column(dbs.String(200), nullable=False)
    password = dbs.Column(dbs.String, nullable=False)
    email = dbs.Column(dbs.String, nullable=False)

    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User({self.id},{self.username}, {self.email})"


class Review(dbs.Model):
    __tablename__ = 'reviews'
    id = dbs.Column(dbs.Integer, primary_key=True)
    user_id = dbs.Column(dbs.Integer, dbs.ForeignKey("users.id"), nullable=False)
    user_name = dbs.Column(dbs.String, nullable=True)
    book_id = dbs.Column(dbs.Integer, dbs.ForeignKey("books.id"), nullable=False)
    rating = dbs.Column(dbs.Integer, nullable=False)
    review = dbs.Column(dbs.String, nullable=True)
    date = dbs.Column(dbs.String(10), nullable=True)

    def __init__(self, ids, userid, book_id, rating, review, username):
        self.user_id = userid
        self.book_id = book_id
        self.review = review
        self.rating = rating
        self.user_name = username
        if (ids != 0):
            self.id = ids
