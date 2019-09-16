import sys
import cv2
import numpy as np

import socket
import struct

import argparse

CAMERA_USERNAME = 'admin'
CAMERA_PASSWORD = 'doanh@aioz'


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--cam_host', type=str, default='192.168.1.64')
    parser.add_argument('--cam_port', type=int, default=554)
    parser.add_argument('--server_host', type=str, default='0.0.0.0')
    parser.add_argument('--server_port', type=int, default=8006)

    args = parser.parse_args()

    camera_rtsp_path = 'rtsp://' + \
        CAMERA_USERNAME + ':' + \
        CAMERA_PASSWORD + '@' + \
        args.cam_host + ':' + \
        str(args.cam_port) + \
        '/h265/ch1/main/av_stream'
    cap = cv2.VideoCapture(camera_rtsp_path)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.server_host, args.server_port))

    count = 1
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    while True:
        ret, frame = cap.read()
        if ret:

            image = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,  scaleFactor = 1.2, minNeighbors = 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('frame', image)
            count += 1
            print("frame: ", count)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
