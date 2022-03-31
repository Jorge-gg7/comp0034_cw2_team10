from werkzeug.security import generate_password_hash, check_password_hash

from flask_app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['user']

    def __repr__(self):
        return f"{self.id} {self.username} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

