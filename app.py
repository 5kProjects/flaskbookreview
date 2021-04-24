from flask import Flask, render_template, request, jsonify, session, url_for, flash

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from forms import BookForm, ReviewForm, SignupForm
from helpers import login_required, getApiData
from models import Book, Review
from config import db, app


@app.route('/createBook', methods=['GET', 'POST'])
def create_book():
    form = BookForm()
    if request.method == 'POST' and form.validate_on_submit():
        db.execute("INSERT INTO books (title, author) VALUES (:title, :author);",
                   {"title": form.title.data, 'author': form.author.data})
        db.commit()
        # data = Book(form.title.data, form.author.data, form.isbn.data, form.year.data, )
    return render_template('book.html', form=form)


@app.route("/book/<string:isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):
    user = session.get("user_id")
    try:
        row = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()
    except Exception as e:
        return '<div> <a href="/signup">Error No book found Go back</a></div>'

    if row is None:
        flash("no book found", category="error")
        return '<div> <a href="/signup">Error No book found Go back</a></div>'
    print("row here", row)

    book = Book(row[0], row[1], row[2], row[3], row[4], reviewCount=row[5] or 0, average=row[6] or 0.0, sum=row[7] or 0)
    # book = Book(row[0], row[1], row[2], row[3], row[4])
    print("))))))))))) book", book.__repr__())
    reviews = []

    # a variable to check whether the user have a review or not
    newReview = False
    userHasRev = False
    userReview = None
    try:
        user_review = db.execute("SELECT * FROM reviews WHERE book_id=:book_id AND user_id=:user_id",
                                 {"book_id": book.id, "user_id": session["user_id"]}).fetchone()
        if (user_review):
            userReview = Review(user_review[0], user_review[1],
                                user_review[2], user_review[3],
                                user_review[4], user_review[4])
            reviews.append(userReview)
            # userHasRev = True
        print("---------->usrRev", user_review)
        revRow = db.execute("SELECT * FROM reviews WHERE book_id=:book_id ",
                            {"book_id": book.id}).fetchall()
        print("***revs", revRow)
        for r in revRow:
            rev = Review(r[0], r[1], r[2], r[3], r[4], r[5])
            reviews.append(rev)
        print("8888888", reviews)
    except Exception as e:
        flash('1 Error:{}'.format(e), category="error")
        flash('Review error ', category="error")
        return render_template("book.html", hasReview=userHasRev, reviews=reviews, book=vars(book), user=user,
                               userReview=userReview)


    print("pooooost")
    # ============================================= POST METHOD ===================
    if request.method == 'POST':
        print("============here")
        if not userHasRev:
            starRating = request.form.get('rating')
            comment = request.form.get('comment')
            review_rating = int(starRating)

            usrName = ""
            userId = 0
            try:
                userId= session["user_id"]
                usrName =session["usrname"]
            except Exception as e:
                print(e)
                usrName=""




            try:
                db.execute(
                    "INSERT INTO reviews (user_id, book_id, rating, review) VALUES (:user_id, :book_id, :rating, :review);",
                    {"user_id": userId, "book_id": book.id, "rating": review_rating, "review": comment})



                newCount = book.review_count + 1
                newSum = book.ratings_sum + review_rating
                newAverage = newSum / newCount

                db.execute(
                    "UPDATE books SET review_count=:count, ratings_sum=:sum, average_reviews=:average WHERE id=:isbn",
                    { "count": newCount, "sum": newSum, "average": newAverage, "isbn": book.isbn})

                db.commit()
                print("iiiiiiiiiiiiiiiiii")

                revew=Review(0, session["user_id"], book.id, review_rating, comment, usrName)
                reviews.insert(0,revew)

                book.review_count = newCount
                book.ratings_sum = newSum
                book.average_reviews = newAverage

                flash("review success", category="success")
                userHasRev = True
                newReview = True

                print("------------here2")
            except Exception as e:
                flash('Review not added ,   Error:{}, '.format(e), category="error")
                return render_template("book.html", user=user, book=vars(book), reviews=reviews, hasReview=userHasRev,

                                       isbn=book.isbn, userReview=userReview)
        if userHasRev and (not newReview):
            flash("review already exist", category="error")

    api_data = {}
    # api_data = getApiData(isbn)
    # if not api_data:
    #     api_data = {'subjects': ['subjects cannot be found']}
    if api_data is not None:
        book = vars(book)
        book.update(api_data)
    return render_template("book.html", book=book, reviews=reviews, hasReview=userHasRev, isbn=book["isbn"],
                            user=user, userReview=userReview)


@app.route("/", methods=["GET", "POST"])
# @login_required
def search():
    books = []
    user = session.get("user_id")
    if request.method == "GET":

        try:
            books = db.execute("SELECT * FROM books LIMIT 20")

        except Exception as e:
            flash("some thing wrong, Error:{}".format(e), category="error")
        return render_template("index.html", books=books, user=user)
    term = request.form.get("search_term", None)

    if term == None or term == "":
        flash("You must provide a term to search")
        return render_template("index.html", books=books, user=user)
    term = "%{}%".format(term)
    books = db.execute("SELECT * FROM books WHERE isbn LIKE :term OR title LIKE :term OR author LIKE :term;",
                       {"term": term}).fetchall()
    if not len(books):
        flash("There is no books")
    return render_template("index.html", books=books, user=user)


@app.route("/api/book/<string:isbn>", methods=['GET', 'POST'])
def api_book(isbn):
    try:
        curs = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()
        # columns = [column[0] for column in books.discription]
    except():
        return jsonify({"error": "some error"}), 404

    if curs is None:
        return jsonify({"error": "no book"}), 404
    book = Book(curs[0], curs[1], curs[2], curs[3], curs[4], )
    print("----------------", vars(book))
    dictBook = vars(book)
    return jsonify(
        {'id': book.id, 'author': book.author, 'title': book.title, "isbn": book.isbn, "releaseYear": book.year, "rating":book.average_reviews, "reviewCount":book.review_count}

    )


@app.route("/signup", methods=["GET", "POST"])
def register():
    """Register user"""
    # form = SignupForm()
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        bool, message = verifySignupFields(username, email, password, confirm)
        if not bool:
            flash(message, category='error')
            return render_template('signup.html', error=message)

        try:
            db.execute("INSERT INTO users (username, email, password) VALUES (:username,:email, :password);",
                       {"username": username, "email": email,
                        "password": generate_password_hash(password, 'sha256')})
            db.commit()
        except Exception as e:
            return render_template('signup.html', error="Error:{}".format(e))
        try:
            user = db.execute("SELECT id FROM users WHERE username = :username;",
                              {"username": username}).fetchone()

        except Exception as e:
            return render_template('signup.html', error="Error:{}".format(e))
        session['user_id'] = user[0]["id"]
        session['username'] = user[0]["username"]
        flash("userCreated", category='success')
        return redirect("/")
    else:

        return render_template("signup.html", )


def verifySignupFields(name, email, password, confirm):
    message = ""
    if password != confirm:
        message = "confirmation and password don't match"
        return [False, message]
        # Query database for username to check that not exist
    user = db.execute("SELECT * FROM users WHERE username = :username;",
                      {"username": name}).fetchone()
    if user:
        print("======>>>> user exist")
        message = "username already taken"
        return [False, message]
    return [True, message]


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print("==========>", username, password)

        try:
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              {"username": username}).fetchall()

            if len(rows) > 0 and check_password_hash(rows[0]["password"], password):
                flash('Logged in successfully!', category='success')
                session["user_id"] = rows[0]["id"]
                session["username"] = rows[0]["username"]

                return redirect("/")
            else:
                flash("invalid username or password", category='error')
                return render_template("login.html")
        except Exception as e:
            flash("Error:{}".format(e), category='error')
            return render_template("login.html")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout"""
    session.clear()
    flash('Logged out successfully!', category='success')
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
