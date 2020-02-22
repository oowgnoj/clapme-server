from flask import Flask, g
from flask_restful import Resource, Api

from .models import initialize_db
from .views import initialize_routes

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)
initialize_routes(api)
initialize_db(app)

if __name__ == '__main__':
    app.run(debug=True)
