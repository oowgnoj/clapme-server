from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/test'

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)
