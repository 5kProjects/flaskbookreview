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

