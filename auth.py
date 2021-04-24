from flask import request, session, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from app import app, db
from forms import LoginForm, SignupForm


@app.route("/signup", methods=["GET", "POST"])
def register():
    """Register user"""
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():

        # Query database for username to check that not exist
        user = db.execute("SELECT * FROM users WHERE username = :username;",
                          {"username": form.username.data}).fetchall()
        if user:
            return flash("username already taken", category='error')
        if form.password.data != form.confirm.data:
            return flash("confirmation and password don't match", category='error')
        else:
            row = db.execute("INSERT INTO users (username, password) VALUES (:username, :password);",
                             {"username": form.username.data, "password": generate_password_hash(form.password.data)})
            print(row)
            db.commit()
            # session["user_id"] = row[0]["id"]
            return redirect("/")
    else:
        return render_template("login.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    form = LoginForm()
    session.clear()

    if request.method == "POST" and form.validate_on_submit():

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": form.username.data}).fetchall()
        # Ensure username exists and password is correct
        if len(rows) == 1 and check_password_hash(rows[0]["password"], form.password.data):
            flash('Logged in successfully!', category='success')
            session["user_id"] = rows[0]["id"]
            return redirect("/")
        else:
            flash("invalid username or password", category='error')
    else:
        return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logout"""
    session.clear()
    flash('Logged out successfully!', category='success')
    return redirect("/")
