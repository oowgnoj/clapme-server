from datetime import datetime
from clapme.__init__ import db
from .mixin.timestamp_mixin import TimestampMixin


class User(TimestampMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    username = db.Column(db.String(30),
                         index=False,
                         unique=True,
                         nullable=False)
    password = db.Column(db.String(30),
                         index=False,
                         unique=False,
                         nullable=False)
    profile = db.Column(db.Text,
                        index=False,
                        unique=False,
                        nullable=True)
    profile_pic = db.Column(db.Text,
                            index=False,
                            unique=False,
                            nullable=True)  # null 일 경우 클라이언트에서 초기 이미지로 처리
    admin = db.Column(db.Boolean,
                      index=False,
                      default=False,
                      unique=False,
                      nullable=False)
    user_goals = db.relationship('UserGoal', backref='user', lazy=True)
    successes = db.relationship('Success', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    reactions = db.relationship('Reaction', backref='user', lazy=True)
