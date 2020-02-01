from datetime import datetime
from __init__ import db
from .mixin.timestamp_mixin import TimestampMixin


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
