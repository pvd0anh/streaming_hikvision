import sys
import cv2
import numpy as np

import socket
import struct

import argparse

CAMERA_USERNAME = 'admin'
CAMERA_PASSWORD = 'aiar12345'

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

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((args.server_host, args.server_port))
    
    while True:
        ret, frame = cap.read()
        if ret:
            # Serialize frame
            _, image_buffer = cv2.imencode('.jpg', frame)
            frame_data = image_buffer.tobytes()

            # Send message length first
            message_size = struct.pack("L", len(frame_data)) ### CHANGED

            # Then data
            client_socket.sendall(message_size + frame_data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
