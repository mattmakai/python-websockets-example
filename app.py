from gevent import monkey
monkey.patch_all()

import redis
from flask import Flask, request, render_template
from flask.ext.socketio import SocketIO

app = Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

@app.route('/')
def main():
    c = db.get('user_count')
    return render_template("main.html", connected=c)


@app.route('/pymeetups/')
def pymeetups():
    return render_template("pymeetups.html")


@socketio.on('connect', namespace="/sfpy")
def ws_conn():
    c = db.incr('user_count')
    socketio.emit('msg', {'count': c}, namespace="/sfpy")


@socketio.on('disconnect', namespace="/sfpy")
def ws_disconn():
    c = db.decr('user_count')
    socketio.emit('msg', {'count': c}, namespace="/sfpy")


@socketio.on('city', namespace="/sfpy")
def ws_city(message):
    socketio.emit('city', {'city': message['city']}, namespace="/sfpy")


if __name__ == "__main__":
    socketio.run(app, port=5000)

