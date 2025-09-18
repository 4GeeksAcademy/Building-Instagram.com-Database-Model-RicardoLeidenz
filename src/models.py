from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    is_active = Column(Boolean(), nullable=False)
    posts = relationship('Post', backref='author', lazy=True)
    events_organized = relationship('Event', backref='who', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    image_url = Column(String(50), nullable=False)
    description = Column(String(120))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'description': self.description,
            'user_id': self.user_id
            # do not serialize the password, its a security breach
        }


class Event(db.Model):
    id = Column(Integer, primary_key=True)
    what = Column(String(15), nullable=False)
    where = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'what': self.what,
            'where': self.where,
            'user_id': self.user_id
        }
