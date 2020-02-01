from __init__ import db

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30),
                         index=False,
                         unique=True,
                         nullable=False)
    password = db.Column(db.String(30),
                        index=False,
                        unique=False,
                        nullable=False)
    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)
    profile = db.Column(db.Text,
                    index=False,
                    unique=False,
                    nullable=True)
    profile_pic = db.Column(db.String(100),
                      index=False,
                      default=False,
                      unique=False,
                      nullable=False)
    admin = db.Column(db.Boolean,
                      index=False,
                      default=False,
                      unique=False,
                      nullable=False)
    