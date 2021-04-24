from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, PasswordField, SelectField

from wtforms.validators import DataRequired, EqualTo, Length


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[])
    description = TextAreaField('Description')
    year = IntegerField('Year', validators=[])
    isbn = StringField('Isbn', validators=[])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = StringField('Password', validators=[])
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm = StringField('Confirm', validators=[])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    review = TextAreaField(
        "Review",
        [DataRequired(), Length(min=4, message="Your message is too short.")]
    )
    Rating = SelectField('rating', [DataRequired()],
                         choices=[
                             ('one', '1'),
                             ('two', '2'),
                             ('three', '3'),
                             ('four', '4'),
                             ('five', '5'),

                         ])
    submit = SubmitField('Submit')
