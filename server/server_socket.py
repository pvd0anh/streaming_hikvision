import sys
import cv2
import numpy as np

import socket
import struct

import time

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8006)

    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    
    s.bind((args.host, args.port))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')
    
    conn, addr = s.accept()
    
    data = b''
    payload_size = struct.calcsize("L")
    
    while True:
        # Retrieve message size
        while len(data) < payload_size:
            data += conn.recv(4096)
    
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
    
        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += conn.recv(4096)
    
        frame_data = data[:msg_size]
        data = data[msg_size:]
    
        # Extract frame
        frame = np.frombuffer(frame_data, np.int8)
        frame = cv2.imdecode(frame, 1)

        # Display
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()