"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Posts

app = Flask(__name__)
app.config['SECRET_KEY'] = "bunnyrabbit"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect("users")

@app.route("/users")
def users():
    users = Users.query.all()
    return render_template("base.html", users=users)

@app.route("/users/new")
def new_user():
    return render_template("create_user.html")

@app.route("/users/new", methods=["POST"])
def new_user_post():
    first = request.form["first"]
    last = request.form["last"]
    image = request.form["image"]

    if image == "":
        image = "https://d2cbg94ubxgsnp.cloudfront.net/Pictures/480x270/9/9/3/512993_shutterstock_715962319converted_920340.png"

    new_user = Users(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users")

@app.route("/users/<int:user_id>")
def user(user_id):
    user = Users.query.get(user_id)
    posts = Posts.query.all()
    return render_template("user.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    user = Users.query.get(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_post(user_id):
    user = Users.query.get(user_id)
    first = request.form["first"]
    last = request.form["last"]
    image = request.form["image"]

    user.first_name = first
    user.last_name = last
    user.image_url = image

    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id):
    Users.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def user_new_post(user_id):
    user = Users.query.get(user_id)
    return render_template("users_post_new.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def user_new_post_post(user_id):
    post = Posts(
        title = request.form["title"],
        content = request.form["content"],
        user_id = user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post(post_id):
    post = Posts.query.get(post_id)
    user = Users.query.get(post.user_id)
    return render_template("post.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit")
def post_edit(post_id):
    post = Posts.query.get(post_id)
    return render_template("post_edit.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def post_edit_post(post_id):
    post = Posts.query.get(post_id)
    
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete")
def post_delete(post_id):
    post = Posts.query.get(post_id)
    Posts.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{post.user_id}")
