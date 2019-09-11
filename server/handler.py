
import numpy as np
import cv2
from PIL import Image
import gevent
import base64
import sys

CURRENT_VERSION = sys.version_info[0]
if CURRENT_VERSION < 3:
    import StringIO as io
else:
    import io

from jobs import *

TIME_WAIT_DEFAULT = 0.01

class ImageBaseHandler(object):
    """ image base handler """

    debug = False

    def __init__(self, cfg):
        """ init """
        self._cfg = {
            'show_in_opt': False,
            'show_out_opt': False,
            'receive_opt': False,
            'send_opt': False,
            'work_opt': False,
            'ws': None,  # websocket
        }
        self._channel = {
            'in': [],
            'out': [],
            # 'in': None,
            # 'out': None,
        }

    def update(self, cfg):
        """ update """
        self._cfg.update(cfg)

    def show_channel_in(self, wait=TIME_WAIT_DEFAULT):
        """ show channel in status """
        while True:
            if self._cfg['show_in_opt']:
                # if self._channel['in'] is not None:
                #     img = self._channel['in']
                #     cv2.imshow('in', img)
                #     cv2.waitKey(1)
                if len(self._channel['in']) > 0:
                    img = self._channel['in'][-1]
                    cv2.imshow('in', img)
                    cv2.waitKey(1)
            gevent.sleep(wait)

    def show_channel_out(self, wait=TIME_WAIT_DEFAULT):
        """ show channel out status """
        while True:
            if self._cfg['show_out_opt']:
                # if self._channel['out'] is not None:
                #     img = self._channel['out']
                #     cv2.imshow('out', img)
                #     cv2.waitKey(1)

                if len(self._channel['out']) > 0:
                    img = self._channel['out'][-1]
                    cv2.imshow('out', img)
                    cv2.waitKey(1)
            gevent.sleep(wait)

    def destory(self):
        """ destory """
        if self._cfg['receive_opt'] == True:
            self._cfg['receive_opt'] = False
            self._channel['in'] = []

        if self._cfg['send_opt'] == True:
            self._cfg['send_opt'] = False
            self._channel['out'] = []

        if self._cfg['show_in_opt'] == True or self._cfg['show_out_opt'] == True:
            self._cfg['show_in_opt'] = False
            self._cfg['show_out_opt'] = False
            cv2.destroyAllWindows('in')
            cv2.destroyAllWindows('out')

    def receive(self, wait=TIME_WAIT_DEFAULT):
        """ receive video stream from websocket """
        while True:
            if self._cfg['receive_opt']:
                try:
                    msg = self._cfg['ws'].receive()
                    #print('____Receive')
                    if CURRENT_VERSION < 3:
                        arr = np.array(Image.open(
                            io.StringIO(msg)), dtype=np.uint8)
                    else:
                        arr = cv2.imdecode(
                            np.frombuffer(msg, dtype=np.uint8), 1)
                    self._channel['in'].append(arr)
                    #print('Len IN: ', len(self._channel['in']))
                    # self._channel['in'] = arr
                except:
                    pass
            gevent.sleep(wait)

    def send(self, wait=TIME_WAIT_DEFAULT):
        """ send img to server """
        while True:
            if self._cfg['send_opt']:
                # if self._channel['out'] is not None:
                if len(self._channel['out']) > 0:
                    try:
                        # arr = self._channel['out']
                        #print('_____Send')
                        arr = self._channel['out'].pop()
                        #print('Len OUT: ', len(self._channel['out']))
                        if CURRENT_VERSION < 3:
                            fp = io.StringIO()
                            img = Image.fromarray(arr)
                            img.save(fp, format="JPEG")
                            base64_str = fp.getvalue().encode('base64')
                        else:
                            arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
                            fp = io.BytesIO()
                            img = Image.fromarray(arr)
                            img.save(fp, format="JPEG")
                            base64_str = base64.b64encode(
                                fp.getvalue()).decode("utf-8")
                        self._cfg['ws'].send(base64_str)
                        #print('\n\n')
                    except:
                        pass
            gevent.sleep(wait)

    def work(self, wait=TIME_WAIT_DEFAULT):
        """ base work """
        while True:
            if self._cfg['work_opt']:
                if len(self._channel['in']):
                    # img = self._channel['in']
                    # self._channel['out'] = img

                    img = self._channel['in'].pop()
                    self._channel['out'].append(img)
                    
            gevent.sleep(wait)

    def warning(self, wait=TIME_WAIT_DEFAULT, max_in=1000, max_out=1000):
        while True:
            self._cfg['receive_opt'] = False if len(
                self._channel['in']) >= max_in else True
            self._cfg['send_opt'] = False if len(
                self._channel['out']) >= max_out else True
            gevent.sleep(wait)

    def clean(self, wait=TIME_WAIT_DEFAULT, max_in=3, max_out=3):
        while True:
            if len(self._channel['in']) > max_in:
                self._channel['in'] = self._channel['in'][-max_in:]
                #print('Clean in', len(self._channel['in']))

            if len(self._channel['out']) > max_in:
                self._channel['out'] = self._channel['out'][-max_out:]
                #print('Clean out', len(self._channel['out']))
            gevent.sleep(wait)


class ImageJobHandler(ImageBaseHandler):
    """ image Job handler """

    def __init__(self, cfg={}):
        """ init """
        super(ImageJobHandler, self).__init__(cfg)
        self._cfg.update({
            'job': '',
            'bbox': ''
        })

        # self._jobs = [
        #     'Pose estimator', 'Counting time', 'Player tracking', 'Draw player trajectory', 'Feet juggle counting'
        # ]

        self._jobs = {
            'Pose estimator': PoseEstimator,
            'Counting time': SpeedMeasurement,
            'Player tracking': PlayerTracking,
            'Draw player trajectory': DrawPlayerTrajectory,
            'Feet juggle counting': FeetJuggleCounting,
            'Head juggle counting': HeadJuggleCounting,
        }

    def work(self, wait=TIME_WAIT_DEFAULT):
        """ base work """
        while True:
            if self._cfg['work_opt']:
                # if self._channel['in'] is not None:
                #     img = self._channel['in']
                #     if self._cfg['job'] in self._jobs:
                #         img = self._jobs[self._cfg['job']]().run(img, self._cfg['bbox'])
                #     self._channel['out'] = img
                if len(self._channel['in']):
                    img = self._channel['in'].pop()
                    #print('Len IN: ', len(self._channel['in']))
                    if self._cfg['job'] in self._jobs:
                        img = self._jobs[self._cfg['job']]().run(img, self._cfg['bbox'])
                    self._channel['out'].append(img)
                    #print('Len OUT: ', len(self._channel['out']))
            gevent.sleep(wait)

    def update(self, cfg):
        """ update """
        self._cfg.update(cfg)
