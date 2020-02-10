from datetime import datetime
from clapme.__init__ import db
from .mixin.timestamp_mixin import TimestampMixin


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
