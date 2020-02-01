from __init__ import db


from .goal import Goal
from .user import User


user_goal = db.Table('usergoals',
    db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column('goal_id', db.Integer, db.ForeignKey(Goal.id), primary_key=True),
    db.Column('subscribe', db.Boolean, default=True, nullable=False),
    db.Column('isAccpeted', db.Boolean, default=False, nullable=False,)
)

