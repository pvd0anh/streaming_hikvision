import os, sys, time
from flask import Flask, Blueprint, request, session, redirect, url_for, abort, render_template, Response
from flask_socketio import SocketIO, send, emit
import cv2
import numpy as np
import io
from PIL import Image
import base64

import grpc
import dl_server_pb2
import dl_server_pb2_grpc

from server import Receiving

PORT = 8006 if len(sys.argv) <= 1 else int(sys.argv[1])
HTTP_PORT = 8007 if len(sys.argv) <= 2 else int(sys.argv[2])

app = Flask(__name__)
app.config.update({
    'DEBUG' : False,
    'USE_RELOADER' : False,
    'LOG_OUTPUT' : True,
    'SECRET_KEY' : 'KzcyL>/e6P:e*Aqw"YI7y~;B$rt`Ub',
    'USERNAME' : ['admin'],
    'PASSWORD' : ['admin'],
})
socketio = SocketIO(app)
task_name = ''
bbox_str = ''

CHANNEL = grpc.insecure_channel('0.0.0.0:50051')
STUB = dl_server_pb2_grpc.DLServerStub(CHANNEL)

SOCK = Receiving(PORT)

def run(task_name):
    while True:
        try:
            start = time.time()
            frame = SOCK.get_frame()
            _, buffer = cv2.imencode('.jpg', frame)
            request = dl_server_pb2.DLImageTaskRequest(task_name='Pose estimator', image=buffer.tobytes(), bbox='')
            response = STUB.proceed_image_task(request)
            print(1/(time.time()-start))
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + response.image + b'\r\n\r\n')
        except Exception as e:
            print(e)
            pass

@app.route('/feed')
def feed():
    return Response(run('Pose estimator'), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_list_algorithm():
    options = [
        {'name' : 'Pose estimator', 'bb' : 0},
        {'name' : 'Counting time', 'bb' : 1,},
        {'name' : 'Player tracking', 'bb' : 1},
        {'name' : 'Draw player trajectory', 'bb' : 0},
        {'name' : 'Feet juggle counting', 'bb' : 0}
        # {'name' : 'Head juggle counting', 'bb' : 0}
    ]
    return options

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('home.html', options = get_list_algorithm(), task = task_name)


@app.route('/job', methods=['POST'])
def job():
    global task_name, bbox_str
    task_name = request.form['algorithm']
    print('Task:', task_name)
    if not session.get('logged_in'):
        abort(401)
    bbox_str = ''
    x = int(request.form['dataX'], 0)
    y = int(request.form['dataY'], 0)
    w = int(request.form['dataWidth'], 0)
    h = int(request.form['dataHeight'], 0)
    if x!=0 and y!=0 and w!=0 and h!=0:
        bbox = [x, y, x + w, y + h]
        bbox_str = ','.join(str(num) for num in bbox)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] == 'erman' and request.form['password'] == 'erman@aioz') or (request.form['username'] == 'admin' and request.form['password'] == 'admin'):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid password or password'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(msg):
    img = cv2.imdecode(np.frombuffer(msg, dtype=np.uint8), 1)
    _, buffer = cv2.imencode('.jpg', img)
    if task_name != '':
        request = dl_server_pb2.DLImageTaskRequest(task_name=task_name, image=buffer.tobytes(), bbox=bbox_str)
        response = STUB.proceed_image_task(request)
        img = cv2.imdecode(np.frombuffer(response.image, np.uint8), 1)
    arr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fp = io.BytesIO()
    img = Image.fromarray(arr)
    img.save(fp, format="JPEG")
    base64_str = base64.b64encode(fp.getvalue()).decode("utf-8")
    emit('message', base64_str)

if __name__ == '__main__':
    print("Server listening at http://localhost:%s" % HTTP_PORT)
    socketio.run(app, host='0.0.0.0', port = HTTP_PORT, debug = app.config['DEBUG'], \
        use_reloader = app.config['USE_RELOADER'], log_output = app.config['LOG_OUTPUT'])
    # socketio.run(app, host="0.0.0.0", port=HTTP_PORT, debug = app.config['DEBUG'], keyfile='privkey.pem', certfile='fullchain.pem', \
    #    use_reloader = app.config['USE_RELOADER'], log_output = app.config['LOG_OUTPUT'])
    