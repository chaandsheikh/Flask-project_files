
from studyeasy import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(50), nullable=False, default='profile.jpeg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'name: {self.name}, age: {self.age}, email: {self.email}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') ,nullable=False)

    def __repr__(self):
        return f'title: {self.title}, author: {self.author}'        

def add_user(form):
    name = form.name.data
    email = form.email.data
    age = form.age.data
    hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(name=name, email=email, age=age,password=hashed_pwd)
    db.session.add(user)
    db.session.commit()
    

    
