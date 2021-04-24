from flask import Blueprint, request, session, render_template, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash


from app import app, db
from forms import LoginForm, SignupForm


auth = Blueprint('auth', __name__)

