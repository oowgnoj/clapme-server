from datetime import datetime
from clapme.__init__ import db


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
