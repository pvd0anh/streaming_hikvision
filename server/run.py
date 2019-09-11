import os, sys, time, argparse
import numpy as np
import base64
import cv2

from flask import Flask, Response
from server import Receiving
sys.path.append(os.getcwd())
import grpc
import dl_server_pb2
import dl_server_pb2_grpc


# parser = argparse.ArgumentParser()
# parser.add_argument('--host', type=str, default='0.0.0.0')
# parser.add_argument('--port', type=int, default=8006, help = "Socker Sever port")
# parser.add_argument('--http_port', type=int, default=8007, help = "Streamer Sever port)
# args = parser.parse_args()

PORT = 8006 if len(sys.argv) <= 1 else int(sys.argv[1])
HTTP_PORT = 8007 if len(sys.argv) <= 2 else int(sys.argv[2])

app = Flask(__name__)
app.config.update({
    'DEBUG' : Flask,
    'SECRET_KEY' : 'KzcyL>/e6P:e*Aqw"YI7y~;B$rt`Ub',
    'USERNAME' : ['admin'],
    'PASSWORD' : ['admin'],
})
current_task = None

SOCK = Receiving(PORT)
CHANNEL = grpc.insecure_channel('0.0.0.0:50051')
STUB = dl_server_pb2_grpc.DLServerStub(CHANNEL)

# def run(task_name):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#     for response in STUB.proceed_streaming_task(generate_requests(task_name)):
#         yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + response.image + b'\r\n\r\n')

# def generate_requests(task_name):
#     while True:
#         try:
#             start = time.time()
#             frame = SOCK.get_frame()
#             _, buffer = cv2.imencode('.jpg', frame)
#             yield dl_server_pb2.DLStreamingTaskRequest(task_name=task_name, image=buffer.tobytes())
#             print(1/(time.time()-start))
#         except Exception as e:
#             print(e)
#             pass

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

#####################################################################
from flask import Blueprint, request, session, redirect, url_for, abort, render_template, flash
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import gevent
from handler import *

main = Blueprint('main', __name__)
TIME_WAIT_DEFAULT = 0.01
job_handler = ImageJobHandler()
jobs = []
task_name = ''

def spawn_jobs(ws):
    global jobs, job_handler
    cfg = {
            'ws'            : ws,
            'show_in_opt'   : True,
            'show_out_opt'  : True,
            'receive_opt'   : True,
            'send_opt'      : True,
            'work_opt'      : True,
           }

    jobs = [
            # gevent.spawn(job_handler.show_channel_in,  TIME_WAIT_DEFAULT) if app.debug else None,
            # gevent.spawn(job_handler.show_channel_out, TIME_WAIT_DEFAULT) if app.debug else None,
            gevent.spawn(job_handler.receive,   TIME_WAIT_DEFAULT),
            gevent.spawn(job_handler.send,      TIME_WAIT_DEFAULT),
            gevent.spawn(job_handler.work,      TIME_WAIT_DEFAULT),
            gevent.spawn(job_handler.warning,   TIME_WAIT_DEFAULT),
            gevent.spawn(job_handler.clean,   TIME_WAIT_DEFAULT),
        ]

    job_handler.update(cfg)
    gevent.joinall([job for job in jobs if job not in [None]])


def switch_job(job, bbox):
    global jobs, job_handler
    cfg = { 'job' : job, 'bbox' : bbox }
    job_handler.update(cfg)


def kill_jobs():
    global jobs, job_handler
    cfg = {
        'ws'            : None,
        'show_in_opt'   : False,
        'show_out_opt'  : False,
        'receive_opt'   : False,
        'send_opt'      : False,
        'work_opt'      : False,
    }
    job_handler.update(cfg)
    [job.kill() for job in jobs if job not in [None]]
    job_handler.destory()

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
        return render_template('index.html', options = get_list_algorithm(), task = task_name)

@app.route('/ws')
def webhandler(wait=TIME_WAIT_DEFAULT):
    if request.environ.get('wsgi.websocket'):
        spawn_jobs(request.environ['wsgi.websocket'])
    return render_template('index.html')


@app.route('/job', methods=['POST'])
def job():
    global task_name
    task_name = request.form['algorithm']
    print('Task:', task_name)
    if not session.get('logged_in'):
        abort(401)
    # kill_jobs()
    bbox_str = ''
    x = int(request.form['dataX'], 0)
    y = int(request.form['dataY'], 0)
    w = int(request.form['dataWidth'], 0)
    h = int(request.form['dataHeight'], 0)
    if x!=0 and y!=0 and w!=0 and h!=0:
        bbox = [x, y, x + w, y + h]
        bbox_str = ','.join(str(num) for num in bbox)
    switch_job(task_name, bbox_str)
    flash('switch job was successfully posted')
    # return redirect(url_for('index'))
    return "1"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] == 'erman' and request.form['password'] == 'erman@aioz') or (request.form['username'] == 'admin' and request.form['password'] == 'admin'):
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
        else:
            error = 'Invalid password or password'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    kill_jobs()
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

#############################################################
if __name__ == '__main__':
    print("Flask server listening at http://localhost:%s" % HTTP_PORT)
    http_server = WSGIServer(('0.0.0.0',HTTP_PORT), app, handler_class = WebSocketHandler)
    """
        HTTPS
    """
    # http_server = WSGIServer(('0.0.0.0', HTTP_PORT), app, handler_class = WebSocketHandler, keyfile='privkey.pem', certfile='fullchain.pem')
    http_server.serve_forever()
    # app.run(debug=False, host=args.host, port=args.http_port)
