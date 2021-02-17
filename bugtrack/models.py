from datetime import datetime
from bugtrack import db, login_manager
from flask_login import UserMixin

""" 

File to create database models. Override __repr__ method for easier data representation.

Using login_manager for user session handling and loging in users.

Create models using

class Test(db.Model):

    write models according to SQLAlchemy docs

    def __repr__(self):
        return f"Test('{self.test}')

"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(16), unique=False, nullable=False)
    issues = db.relationship('Issue', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_title = db.Column(db.String(100), nullable=False)
    issue_content = db.Column(db.Text, nullable=False)
    file = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Issue('{self.id}', '{self.issue_title}', '{self.date}' )"

