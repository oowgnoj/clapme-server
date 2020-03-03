from __future__ import absolute_import
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def initialize_db(app):
    db.init_app(app)


class User(db.Model):

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
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user_goals = db.relationship(
        'UserGoal', cascade="all,delete", backref='user', lazy=True)
    successes = db.relationship(
        'Success', cascade="all,delete", backref='user', lazy=True)
    comments = db.relationship(
        'Comment', cascade="all,delete", backref='user', lazy=True)
    reactions = db.relationship(
        'Reaction', cascade="all,delete", backref='user', lazy=True)


class UserGoal(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    goal_id = db.Column(db.Integer,
                        db.ForeignKey('goal.id'),
                        nullable=False)
    is_owner = db.Column(db.Boolean,
                         default=False,
                         nullable=False)
    subscribe = db.Column(db.Boolean,
                          default=True,
                          nullable=False)
    isAccepted = db.Column(db.Boolean,
                           default=False,
                           nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Goal(db.Model):

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
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user_goals = db.relationship(
        'UserGoal', cascade="all,delete", backref='goal', lazy=True)
    routines = db.relationship(
        'Routine', cascade="all,delete", backref='goal', lazy=True)
    comments = db.relationship(
        'Comment', cascade="all,delete", backref='goal', lazy=True)


class Routine(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    goal_id = db.Column(db.Integer,
                        db.ForeignKey('goal.id'),
                        nullable=False)
    title = db.Column(db.String(30),
                      nullable=False)
    mon = db.Column(db.Boolean,
                    index=True,
                    unique=False,
                    nullable=False,
                    default=False)
    tue = db.Column(db.Boolean,
                    index=True,
                    unique=False,
                    nullable=False,
                    default=False)
    wed = db.Column(db.Boolean,
                    index=True,
                    unique=False,
                    nullable=False,
                    default=False)
    thu = db.Column(db.Boolean,
                    index=True,
                    unique=False,
                    nullable=False,
                    default=False)
    fri = db.Column(db.Boolean,
                    index=True,
                    unique=False,
                    nullable=False,
                    default=False)
    sat = db.Column(db.Boolean,
                    index=True,
                    unique=False,
                    nullable=False,
                    default=False)
    sun = db.Column(db.Boolean,
                    index=True,
                    unique=False,
                    nullable=False,
                    default=False)
    time_at = db.Column(db.Integer,
                        nullable=False)
    created = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow)
    successes = db.relationship(
        'Success', cascade="all,delete", backref='routine', lazy=True)


class Success(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    routine_id = db.Column(db.Integer,
                           db.ForeignKey('routine.id'),
                           nullable=False)
    created = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow)
    reactions = db.relationship(
        'Reaction', cascade="all,delete", backref='success', lazy=True)


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
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Comment(db.Model):

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
    reactions = db.relationship(
        'Reaction', cascade="all,delete", backref='comment', lazy=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
