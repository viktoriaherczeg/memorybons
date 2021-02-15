<<<<<<< HEAD
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length


# Forms

class NewMemoryForm(FlaskForm):
    title = StringField(label="Memory Name", validators=[DataRequired()])
    description = TextAreaField(label="Describe your Memory", validators=[DataRequired(), Length(max=255)])
    img = FileField(label="Image link that captures the essence", validators=[FileRequired()])
    submit = SubmitField("Submit")


class EditForm(FlaskForm):
    description = TextAreaField(label="Describe your Memory", validators=[DataRequired(), Length(max=255)])
    img = FileField(label="Image link that captures the essence")
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ChangePassword(FlaskForm):
    old_password = PasswordField(label="Old Password", validators=[DataRequired()])
    new_password = PasswordField(label="New Password", validators=[DataRequired()])
    repeat_password = PasswordField(label="Repeat Password", validators=[DataRequired()])
=======
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length


# Forms

class NewMemoryForm(FlaskForm):
    title = StringField(label="Memory Name", validators=[DataRequired()])
    description = TextAreaField(label="Describe your Memory", validators=[DataRequired(), Length(max=255)])
    img = FileField(label="Image link that captures the essence", validators=[FileRequired()])
    submit = SubmitField("Submit")


class EditForm(FlaskForm):
    description = TextAreaField(label="Describe your Memory", validators=[DataRequired(), Length(max=255)])
    img = FileField(label="Image link that captures the essence")
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ChangePassword(FlaskForm):
    old_password = PasswordField(label="Old Password", validators=[DataRequired()])
    new_password = PasswordField(label="New Password", validators=[DataRequired()])
    repeat_password = PasswordField(label="Repeat Password", validators=[DataRequired()])
>>>>>>> b9fa864d08cdfc8f3e302ffc4a6627cb94f96515
    submit = SubmitField("Submit")