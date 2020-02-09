from datetime import datetime
from clapme.__init__ import db
print('-------------------------- 여기는 읽니???')


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
