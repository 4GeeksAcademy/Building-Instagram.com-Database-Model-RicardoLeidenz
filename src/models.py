from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, Column

db = SQLAlchemy()

class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120),nullable=False)
    is_active = Column(Boolean(), nullable=False)

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
    when = Column(DateTime, nullable=False)
    where = Column(String(30), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "what": self.what,
            "when": self.when,
            "where": self.where
        }