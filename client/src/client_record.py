"""
Continuously capture images from a webcam and write to a Redis store.
Usage:
   python client_record.py [url] [width] [height]
"""
import os
import sys
import time
import coils
import cv2
import numpy as np
import redis

# Monitor the framerate at 1s, 5s, 10s intervals.
# fps = coils.RateTicker((1, 5, 10))

CAMERA_USERNAME = 'admin'
CAMERA_PASSWORD = 'aiar12345'

# undistort
DIM = (2688, 1520)
K = np.array([[1501.2595834770557, 0.0, 1370.6697823250217], [0.0, 1500.79553264583, 788.6583790280063], [0.0, 0.0, 1.0]])
D = np.array([[-0.1592635301272772], [0.19320207691352564], [-0.36744955632755505], [0.2280147761483244]])
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)

def undistort(img):
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img

class ClientRecord:
    def __init__(self, camera_host, camera_port):
        self.store = redis.Redis()
        self.camera_rtsp_path = 'rtsp://' + \
                CAMERA_USERNAME + ':' + \
                CAMERA_PASSWORD + '@' + \
                camera_host + ':' + \
                str(camera_port) + \
                '/h265/ch1/main/av_stream'


    def proceed(self):
        # Create video capture object, retrying until successful.
        max_sleep = 5.0
        cur_sleep = 0.1
        while True:
            cap = cv2.VideoCapture(self.camera_rtsp_path)
            if cap.isOpened():
                break
            print('not opened, sleeping {}s'.format(cur_sleep))
            time.sleep(cur_sleep)
            if cur_sleep < max_sleep:
                cur_sleep *= 2
                cur_sleep = min(cur_sleep, max_sleep)
                continue
            cur_sleep = 0.1

        while True:
            hello, image = cap.read()
            image = undistort(image)
            image = cv2.resize(image, (int(image.shape[1]/2), int(image.shape[0]/2)))
            if image is None:
                time.sleep(0.5)
                continue
            hello, image = cv2.imencode('.jpg', image)
            value = np.array(image).tostring()
            self.store.set('image', value)
            image_id = os.urandom(4)
            self.store.set('image_id', image_id)
            
            # Print the framerate.
            # text = '{:.2f}, {:.2f}, {:.2f} fps'.format(*fps.tick())
            # print(text)
