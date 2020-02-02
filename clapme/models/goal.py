from datetime import datetime
from __init__ import db
from .mixin.timestamp_mixin import TimestampMixin


class Goal(TimestampMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),
                      index=False,
                      unique=False,
                      nullable=False)
    description = db.Column(db.String(100),
                            index=False,
                            unique=False,
                            nullable=True)
    interval = db.Column(db.String(30),
                         index=False,
                         unique=False,
                         nullable=False)
    times = db.Column(db.Integer,
                      index=False,
                      unique=False,
                      nullable=False)
    thumbnail = db.Column(db.String(100),
                          index=False,
                          unique=False,
                          nullable=True)  # null 일 경우 클라이언트에서 초기 이미지로 처리
    user_goals = db.relationship('UserGoal', backref='goal', lazy=True)
    successes = db.relationship('Success', backref='goal', lazy=True)
    comments = db.relationship('Comment', backref='goal', lazy=True)
