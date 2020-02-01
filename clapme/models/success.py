from datetime import datetime
from __init__ import db


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
