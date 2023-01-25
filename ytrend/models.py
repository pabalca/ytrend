import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())


class Stat(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    channel = db.Column(db.String)
    views = db.Column(db.Integer)
    videos = db.Column(db.Integer)
    subs = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Stat> {self.channel} {self.created_at}"


class Total(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    views = db.Column(db.Integer)
    videos = db.Column(db.Integer)
    subs = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Total> {self.created_at}"

