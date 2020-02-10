from flask import Flask, g
from flask_restful import Resource, Api

from clapme.models import initialize_db
from clapme.views import initialize_routes

app = Flask(__name__)
app.config.from_object('clapme.config')

api = Api(app)
initialize_routes(api)
initialize_db(app)

if __name__ == '__main__':
    app.run(debug=True)
