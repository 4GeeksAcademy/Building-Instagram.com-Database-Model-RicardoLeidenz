from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    # Atributes
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String(32), unique=True, nullable=False)
    password = Column(String(32), nullable=False)
    # Relationships
    posts = relationship('Post', backref='author')
    comments = relationship('Comment', backref='author')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'posts': self.posts,
            'comments': self.comments,
            'following': self.following

        }


class Post(db.Model):
    # Attributes
    id = Column(Integer, primary_key=True)
    # Foreign Keys
    user_id = Column(Integer, ForeignKey('user.id'))
    # Relationships
    comments = relationship('Comment', backref='posted_on')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'comments': self.comments
            # do not serialize the password, its a security breach
        }


class Comment(db.Model):
    # Attributes
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(120), nullable=False)
    # Foreign Keys
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'author_id': self.author_id,
            'post_id': self.post_id
        }


class Media(db.Model):
    # Attributes
    id = Column(Integer, primary_key=True)
    type = Column(String(120), nullable=False)
    url = Column(String(120), nullable=False)
    # Foreign Keys
    post_id = Column(Integer, ForeignKey('post.id'))

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'url': self.url,
            'post_id': self.post_id
        }