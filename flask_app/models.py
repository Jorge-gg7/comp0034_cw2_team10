from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from flask_app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['user']
    # __tablename__ = "user"
    # id = db.Column(db.Integer, primary_key=True)
    # first_name = db.Column(db.Text, nullable=False)
    # last_name = db.Column(db.Text, nullable=False)
    # email = db.Column(db.Text, unique=True, nullable=False)
    # password = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.id} {self.username} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Post(db.Model):
    __table__ = db.Model.metadata.tables['post']
    # __tablename__ = "post"
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    # date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # content = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"