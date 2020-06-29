from flask import session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from ..models import db, Comment, User
from ..util.helper import to_dict

socketio = SocketIO()


def initialize_socket(app):
    return socketio.init_app(app, logger=True, engineio_logger=True, cors_allowed_origins="*")

# -*- coding: utf-8 -*-


@socketio.on('joined', namespace='/goal')
def joined(comment):
    """유저가 해당 goal 방으로 입장"""
    name = comment.get('name')
    # user_id = comment.get('user_id')
    goal_id = comment.get('goal_id')
    join_room(goal_id)
    emit('status', {'msg': comment.get('name') +
                    ' has entered the room.'}, room=goal_id)


@socketio.on('comment', namespace='/goal')
def post_comment(comment):
    """comment 작성시"""
    user_id = comment.get('user_id')
    goal_id = comment.get('goal_id')
    comment = comment.get('comment')

    user_info = User.query.filter_by(id=user_id).first()
    user_info = to_dict(
        user_info, ['id', 'email', 'username', 'profile_pic', 'profile'])

    new_comment = Comment(user_id=user_id, goal_id=goal_id,
                          contents=comment)
    db.session.add(new_comment)
    db.session.commit()

    emit('comment', {'goal_id': goal_id, 'comment': comment,
                     'user': user_info}, room=goal_id)


@socketio.on('left', namespace='/goal')
def left(comment):
    """방 나감. socket connection 끊기"""
    goal_id = comment.get('goal_id')
    leave_room(goal_id)


# goal/13 -> 각기 다른 방에서 socket 통신이 되어야한다

# namespace, room, connect(소켓 시작되는 느낌), disconnect
# namespace는 endpoint 느낌이다
# room 은.. 목표 2번방
#

# @socketio.on('join', namespace='/goal')
# def on_join(data):
#     room = session.get['goal_id']
#     print('room ', room)
#     join_room(room)
#     emit("response", {
#          'data': data['data'], 'username': 'my name is'}, room=room)


# @socketio.on('post-comment', namespace='/goal')
# def post_comment(comment):
#     room = session['room']
#     goal_id = session['goal_id']
#     username = session['username']
#     print(goal_id)
#     join_room(room)

#     emit('comment-posted', {
#         'data': comment
#     }, room=room)

# 1. 목표 방에 들어오면서 get 요청으로 초기 ui 용 데이터 받은 후
# 2. socket 커넥션 맺고 (: 자동으로 해주는 느낌)
# 3. socket 통신 (서버랑 클라이언트) room, namespace 접속
# 4. 클라이언트 emit (댓글 쓴다: post comment) →
# 5. on emit 되었을 때, DB 처리 같은거 하고, 그 다음에 서버 emit


# @socketio.on("request", namespace='/mynamespace')
# def post_goal(message):
#     print("request 들어옴")
#     emit("response", {
#          'data': message['data'], 'username': 'my name is'}, broadcast=False)

# emit(/goal, request, {body: {message: ____, room: 2}})


# 클라이언트 (3) ->
# 3번방 조인
# 명령어를 수행


# 클라이언트 (3) ->
# 명령어 수행할건데 3번방에 해

# @socketio.on("request", namespace = '/goal')
# def goal_request(message):
#     # room = request.get(room) '2'
#     message -> DB 저장하고 &
#     emit / send ("response", message: {}, room = room)


# namespace, 의 room 에 접속한다 (connect)
#

# @socketio.on('connect')
# def handle_message():
#     print('여기로 요청이 들어오긴함')
#     send('connected')


# @socketio.on('request')
# def handle_message(msg):
#     print('request 여기여기 요청이 들어오긴함')
#     send('send back')


# @socketio.on('json')
# def handle_json(json):
#     send(json, json=True)

# @socketio.on('my event')
# def handle_my_custom_event(json):
#     emit('my response', json)
