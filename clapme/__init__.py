from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from clapme.views import initialize_routes

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)
db = SQLAlchemy(app)

initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True)
