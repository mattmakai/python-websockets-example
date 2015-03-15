from gevent import monkey
monkey.patch_all()

import redis
from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO

app = Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/pymeetups/')
    return render_template('pymeetups.html')


@socketio.on('connect', namespace='/dd')
def ws_conn():
    c = db.incr('connected')
    socketio.emit('msg', {'count': c}, namespace='/dd')


@socketio.on('disconnect', namespace='/dd')
def ws_disconn():
    c = db.decr('connected')
    socketio.emit('msg', {'count': c}, namespace='/dd')

@socketio.on('city', namespace='/dd')
    print(message['city'])

if __name__ == '__main__':
    socketio.run(app, port=5000)
