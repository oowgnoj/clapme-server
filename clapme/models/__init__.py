from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def initialize_db(app):
    db.init_app(app)


class TimestampMixin(object):
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


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


class UserGoal(TimestampMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    goal_id = db.Column(db.Integer,
                        db.ForeignKey('goal.id'),
                        nullable=False)
    subscribe = db.Column(db.Boolean,
                          default=True,
                          nullable=False)
    isAccepted = db.Column(db.Boolean,
                           default=False,
                           nullable=False)


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


class Success(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    goal_id = db.Column(db.Integer,
                        db.ForeignKey('goal.id'),
                        nullable=False)
    created = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow)
    reactions = db.relationship('Reaction', backref='success', lazy=True)


class Reaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    comment_id = db.Column(db.Integer,
                           db.ForeignKey('comment.id'),
                           nullable=True)
    success_id = db.Column(db.Integer,
                           db.ForeignKey('success.id'),
                           nullable=True)
    type = db.Column(db.String(30),
                     unique=False,
                     nullable=False)
    created = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow)


class Comment(TimestampMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    goal_id = db.Column(db.Integer,
                        db.ForeignKey('goal.id'),
                        nullable=False)
    contents = db.Column(db.Text,
                         unique=False,
                         nullable=False)
    reactions = db.relationship('Reaction', backref='comment', lazy=True)
