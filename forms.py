from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

# Forms

class NewMemoryForm(FlaskForm):
    title = StringField(label="Memory Name", validators=[DataRequired()])
    description = StringField(label="Describe your Memory", validators=[DataRequired()])
    img_url = StringField(label="Image link that captures the essence", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditForm(FlaskForm):
    description = StringField(label="Describe your Memory", validators=[DataRequired()])
    img_url = StringField(label="Image link that captures the essence", validators=[DataRequired()])
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
