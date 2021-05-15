# Project 1: Books
This project is adopted form Harvard's most popular class **CS50** Programming with Python and JavaScript [[1]](#1).
 ## helpful Commands
> venv\Scripts\activate
> 
> set FLASK_APP=application
> 
> set FLASK_ENV=development
# Objectives

1. Become more comfortable with Python.
2. Gain experience with Flask.
3. Learn to use SQL to interact with databases.

# Overview

this is a book review website. Users will be able to register for the website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. it  also makes use of a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via the website’s API.
# Getting Started
## PostgreSQL

For this project, you’ll need to set up a PostgreSQL database to use with the application. It’s possible to set up PostgreSQL locally on your own computer, but for this project, we’ll use a database hosted by Heroku, an online web hosting service.

1. Navigate to [https://www.heroku.com/], and create an account if you don’t already have one.
    On Heroku’s Dashboard, click “New” and choose “Create new app.”

2. Give your app a name, and click “Create app.”

3. On your app’s “Overview” page, click the “Configure Add-ons” button.
    
4. In the “Add-ons” section of the page, type in and select “Heroku Postgres.”
    
6. Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision.”
    
7. Now, click the “Heroku Postgres :: Database” link.
    
8. You should now be on your database’s overview page. Click on “Settings”, and then “View Credentials.” This is the information you’ll need to log into your database.

Alternatively, if you install PostgreSQL on your own computer, you should be able to run psql URI on the command line, where the URI is the link provided in the Heroku credentials list.

 # Python and Flask

1. First, make sure you install a copy of Python. For this course, you should be using Python version 3.6 or higher.
2. You’ll also need to install pip. If you downloaded Python from Python’s website, you likely already have pip installed (you can check by running pip in a terminal window). If you don’t have it installed, be sure to install it before moving on!

## To try running your first Flask application:

1. Clone the repository 

2. In a terminal window, navigate into the project directory.

3. Run 
    > pip3 install -r requirements.txt

    in your terminal window to make sure that all of the necessary Python packages (Flask and SQLAlchemy, for instance) are installed.

4. Set the environment variable FLASK_APP to be application.py. On a Mac or on Linux, the command to do this is 
   
 - this step is not necessary if app.py file exists and you can skip it

   > export FLASK_APP=application.py. 
   
    On Windows, the command is instead 
   > set FLASK_APP=application.py. 
   > 
   You may optionally want to set the environment variable FLASK_DEBUG to 1, which will activate Flask’s debugger and will automatically reload your web application whenever you save a change to a file.

5. Set the environment variable DATABASE_URL to be the URI of your database, which you should be able to see from the credentials page on Heroku.

6. Run flask run to start up your Flask application.
7. If you navigate to the / URL you should see a page appear with a search box

## Goodreads API

Goodreads is a popular book review website, and we’ll be using their API in this project to get access to their review data for individual books.

1. Go to [https://www.goodreads.com/api] and sign up for a Goodreads account if you don’t already have one.

2. Navigate to [https://www.goodreads.com/api/keys] and apply for an API key. For “Application name” and “Company name” feel free to just write “project1,” and no need to include an application URL, callback URL, or support URL.
3. You should then see your API key. (For this project, we’ll care only about the “key”, not the “secret”.)
4. You can now use that API key to make requests to the Goodreads API, documented here. In particular, Python code like the below


``` python
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "9781632168146"})
print(res.json())
```

where KEY is your API key, will give you the review and rating data for the book with the provided ISBN number. In particular, you might see something like this dictionary:

```json
{'books': [{
                'id': 29207858,
                'isbn': '1632168146',
                'isbn13': '9781632168146',
                'ratings_count': 0,
                'reviews_count': 1,
                'text_reviews_count': 0,
                'work_ratings_count': 26,
                'work_reviews_count': 113,
                'work_text_reviews_count': 10,
                'average_rating': '4.04'
            }]
}
```
Note that work_ratings_count here is the number of ratings that this particular book has received, and average_rating is the book’s average score out of 5.

# Functionalities

 Here are the requirements of this application:

1. **Registration**: Users should be able to register for your website, providing (at minimum) a username and password.

2. **Login**: Users, once registered, should be able to log in to your website with their username and password.

3. **Logout**: Logged in users should be able to log out of the site.

4. **Import**: Provided for you in this project is a file called books.csv, which is a spreadsheet in CSV format of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. In a Python file called import.py separate from the web application, there is a program that will take the books and import them into your PostgreSQL database. You will first need to create, the tables . Run this program by running python3 import.py to import the books into your database, and submit this program with the rest of your project code.

5. **Search**: in the default page you are taken to a page where you can search for a book. you can type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, the website displays a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, the search page find matches for those as well!

6. **Book Page**: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on the website.

7. **Review Submission**: On the book page, users are able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users can not submit multiple reviews for the same book.

8. **Goodreads Review Data**: On the book page,  the average rating and number of ratings the work has received from Goodreads is displayed (if available).

9. **API Access**: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, the website returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should is in the format:

```json
    {
        "title": "Memory",
        "author": "Doug Lloyd",
        "year": 2015,
        "isbn": "1632168146",
        "review_count": 28,
        "average_score": 5.0
    }
```

If the requested ISBN number isn’t in not in the database, the website returns a 404 error.

1. raw SQL commands is used (as via SQLAlchemy’s execute method) in order to make database queries. 
2.SQLAlchemy is not used in this version
3. The README.md, include a writeup describing the project,
4.all Python packages that need to be installed in order to run the web application, are added in the requirements.txt!

 the design, look, and feel of the website can be be changed in any way! And   additional features can be added to the website, 

# other informations

    1. this projects database includes one table to keep track of users, one table to keep track of books, and one table to keep track of reviews. 

    2.  TO “log a user in,the information is stored inside a session, which can store different values for different users. 
         In particular, each user has an id, and  that is the id stored in the session (e.g., in session["user_id"]) to keep track of which user is currently logged in.

## References
<a id="1">[1]</a> 
[https://cs50.harvard.edu/web/2020/#:~:text=Programming%20with%20Python%20and%20JavaScript