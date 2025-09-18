from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    is_active = Column(Boolean(), nullable=False)
    events_organized = relationship('Event', backref='organizer', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }


class Event(db.Model):
    id = Column(Integer, primary_key=True)
    what = Column(String(15), nullable=False)
    where = Column(String(30), nullable=False)
    who = Column(Integer, ForeignKey("user.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "what": self.what,
            "where": self.where,
            "who": self.who
        }
