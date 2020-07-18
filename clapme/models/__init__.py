from __future__ import absolute_import
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from .enum import *


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
                         nullable=False)  # oauth 의 경우 id 를 username 으로 초기설정
    password = db.Column(db.String(30),
                         index=False,
                         unique=False,
                         nullable=False)
    profile = db.Column(db.Text,
                        index=False,
                        unique=False,
                        nullable=True)
    pic_url = db.Column(db.Text,
                        index=False,
                        unique=False,
                        nullable=True)  # null 일 경우 클라이언트에서 초기 이미지로 처리
    timezone = db.Column(db.String(80),
                         index=False,
                         unique=False,
                         nullable=True)
    admin = db.Column(db.Boolean,
                      index=False,
                      default=False,
                      unique=False,
                      nullable=False)
    created = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow)
    updated = db.Column(db.DateTime,
                        onupdate=datetime.utcnow)
    routines = db.relationship('Routine',
                               cascade="all,delete",
                               backref='user',
                               lazy=True)


class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        index=True,
                        nullable=False)
    title = db.Column(db.String(80),
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
    alarm = db.Column(db.Boolean,
                      index=False,
                      unique=False,
                      nullable=False,
                      default=True),
    time = db.Column(db.String(30),
                     unique=False,
                     nullable=True)
    description = db.Column(db.Text,
                            index=False,
                            unique=False,
                            nullable=True)
    category = db.Column(db.String(80),
                         index=True,
                         unique=False,
                         nullable=True)
    color_id = db.Column(db.Integer,
                         db.ForeignKey('color.id'),
                         nullable=False)
    created = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow)
    updated = db.Column(db.DateTime,
                        onupdate=datetime.utcnow)
    successes = db.relationship('Success',
                                cascade="all,delete",
                                backref='routine',
                                lazy=True)


class Success(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer,
                           db.ForeignKey('routine.id'),
                           nullable=False)
    date_str = db.Column(db.String(80),
                         index=True,
                         unique=False,
                         nullable=False)
    day = db.Column(db.String(80),
                    index=True,
                    unique=False,
                    nullable=False)
    created = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.utcnow)


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),
                      nullable=False)
    sub_title = db.Column(db.String(80),
                          nullable=True)
    contents = db.Column(db.Text,
                         nullable=True)
    pic_url = db.Column(db.Text,
                        nullable=True)
    routine_1 = db.Column(db.Text,
                          nullable=True)
    routine_2 = db.Column(db.Text,
                          nullable=True)
    routine_3 = db.Column(db.Text,
                          nullable=True)
    routine_4 = db.Column(db.Text,
                          nullable=True)
    routine_5 = db.Column(db.Text,
                          nullable=True)
    routine_6 = db.Column(db.Text,
                          nullable=True)
    routine_7 = db.Column(db.Text,
                          nullable=True)
    routine_8 = db.Column(db.Text,
                          nullable=True)
    routine_9 = db.Column(db.Text,
                          nullable=True)


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hex_code = db.Column(db.String(30),
                         index=False,
                         unique=False)
    routines = db.relationship('Routine',
                               cascade="all,delete",
                               backref='color',
                               lazy=True)
