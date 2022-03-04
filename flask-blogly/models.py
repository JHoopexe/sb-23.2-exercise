"""Models for Blogly."""

from email import contentmanager
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Users(db.Model):
    __tablename__ = 'users'
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(2083))

class Posts(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Text, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
