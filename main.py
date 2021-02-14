from flask import Flask, render_template, redirect, request, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from sqlalchemy.orm import relationship
from forms import NewMemoryForm, EditForm, LoginForm, RegisterForm, ChangePassword
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary import config as cloudinary_config

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memories.db'
db = SQLAlchemy(app)

cloudinary_config(cloud_name="dijrty8zh",
                     api_key="579177932436579",
                     api_secret="OwkzkS0r4DVN0Z68ahAfWDhar94")


# DB stuff

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    memories = relationship("Memory", back_populates="user")


class Memory(db.Model):
    __tablename__ = "memories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="memories")

    def __repr__(self):
        return '<Memory %r>' % self.title


db.create_all()



#security

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)

#Memory related routes

@app.route("/show")
@login_required
def show():
    
    try: 
        memories = Memory.query.filter_by(user_id=current_user.id).all()
    except sqlalchemy.exc.ArgumentError:
        memories = []
    return render_template("show.html", memories=memories, logged_in=current_user.is_authenticated)


@app.route("/add", methods=["POST", "GET"])
@login_required
def add():
    add_form = NewMemoryForm()
    if request.method == "POST" and add_form.validate_on_submit():
        img = add_form.img.data
        uploaded_img = cloudinary_upload(img)
        img_url, options = cloudinary_url(uploaded_img['public_id'], format="jpg", width="300", height="300")
        
        memory = Memory(
            title = add_form.title.data,
            description = add_form.description.data,
            img_url = img_url,
            user_id = current_user.id
        )
        db.session.add(memory)
        db.session.commit()

        return redirect(url_for("show"))

    return render_template("add.html", form=add_form, logged_in=current_user.is_authenticated)

@app.route("/edit/<id>", methods=["POST", "GET"])
@login_required
def edit(id):
    memory = Memory.query.filter_by(id=id).first()
    form = EditForm(description=memory.description)
    
    if request.method == "POST" and form.validate_on_submit():
        if form.img.data:
            img = form.img.data
            uploaded_img = cloudinary_upload(img)
            img_url, options = cloudinary_url(uploaded_img['public_id'], format="jpg", width="300", height="300")
            memory.img_url = img_url
        
        memory.description = form.description.data
        
        db.session.add(memory)
        db.session.commit()
        return redirect(url_for("show"))

    return render_template("edit.html", memory=memory, form=form, logged_in=current_user.is_authenticated)


@app.route("/delete/<id>")
@login_required
def delete(id):
    memory = Memory.query.filter_by(id=id).first()
    db.session.delete(memory)
    db.session.commit()
    return redirect(url_for("show"), logged_in=current_user.is_authenticated)


#User related routes

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("You are already registered with that email. Please log in.")
            return redirect(url_for("login"))
        user = User(
            name = form.name.data,
            email = form.email.data,
            password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("show"))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("show"))
            else:
                #flash incorrect pw
                flash("Incorrect password")
                return redirect(url_for("login"))
        else:
            #flash message: no registration with that email
            flash("You are not registered with that email. Please create an account.")
            return redirect(url_for("register"))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home", logged_in=False))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ChangePassword()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        if check_password_hash(user.password, form.old_password.data) and form.new_password.data == form.repeat_password.data:
            user.password = generate_password_hash(form.new_password.data, method="pbkdf2:sha256", salt_length=8)
            db.session.add(user)
            db.session.commit()
            #flash successful message
            flash("Password changed successfully.")
            return redirect(url_for("profile"))
    return render_template("userprofile.html", form=form, logged_in=current_user.is_authenticated)



if __name__ == "__main__":
    
    app.run(debug=True)