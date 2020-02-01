from __init__ import db

class Goal(db.Model):

    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30),
                         index=False,
                         unique=False,
                         nullable=False)
    description = db.Column(db.String(30),
                        index=False,
                        unique=False,
                        nullable=True)
    interval = db.Column(db.String(30),
                      index=False,
                      unique=False,
                      nullable=False)
    times = db.Column(db.Integer(),
                    index=False,
                    unique=False,
                    nullable=False)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)
    thumbnail = db.Column(db.String(100),
                      index=False,
                      default=False,
                      unique=False,
                      nullable=False)
