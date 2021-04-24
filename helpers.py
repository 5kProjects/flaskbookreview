import os
# import requests
import requests
from flask import redirect, session, render_template, request
from functools import wraps


def autolog(message):
    "Automatically log the current function details."
    import inspect, logging
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logging.debug("%s: %s in %s:%i" % (
        message,
        func.co_name,
        func.co_filename,
        func.co_firstlineno
    ))

def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def getApiData(isbn):

    try:
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={ "isbns": isbn})
        response.raise_for_status()
    except requests.RequestException:
        return None
    # Parse responde
    try:
        books = response.json()["books"]
        return {
            "isbn": books[0]["isbn"],
            "reviews_count": books[0]["reviews_count"],
            "average_rating": books[0]["average_rating"]
        }
    except (KeyError, TypeError, ValueError) as e:
        return None