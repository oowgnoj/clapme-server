from flask import Flask, g
from flask_restful import Resource, Api
from flask_socketio import SocketIO, emit, send
from .models import initialize_db
from .views import initialize_routes
from .socket import *

app = Flask(__name__)
app.config.from_object('config')


api = Api(app)
initialize_routes(api)
initialize_socket(app)
initialize_db(app)


@app.route('/test')
def hello_world():
    return app.send_static_file('test.html')


# @socketio.on('connect', namespace='/mynamespace')
# def connect():
#     print("connect 들어옴")
#     emit("response", {'data': 'Connected', 'username': 'my name is'})


# @socketio.on('disconnect', namespace='/mynamespace')
# def disconnect():
#     print("Disconnected")


# @socketio.on("request", namespace='/mynamespace')
# def request(message):
#     print("request 들어옴")
#     emit("response", {
#          'data': message['data'], 'username': 'my name is'}, broadcast=False)


if __name__ == '__main__':
    socketio.run(app, debug=True)
