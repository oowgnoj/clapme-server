from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# from flaskext.mysql import MySQL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/test' 

db = SQLAlchemy(app)

# from models import *
# db.create_all()


if __name__ =='__main__':
    app.run(debug=True)