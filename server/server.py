"""
Receive frames from client, stream to web
Usage:
   python server.py [port]
"""

import socket
import numpy as np
import cv2
import struct
SIZE_BYTE = 4096

class Receiving():
    def __init__(self, SERVER_PORT):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', SERVER_PORT))
        self.server.listen(5)
        self.connection = None
        self.client_address = None

        print('Server listening on port', SERVER_PORT)
            
    def __del__(self):
        self.server.close()

    def get_frame(self):
        try:
            if not self.connection:
                self.connection, self.client_address = self.server.accept()
                print('Client connected: ', self.client_address)
            try:
                len_str = self.connection.recv(4)
                size = struct.unpack('!i', len_str)[0]
            except struct.error:
                print('Client disconnected: ', self.client_address)
                self.connection.close()
                self.connection = None
                self.client_address = None
                return None

            img_str = b''
            while size > 0:
                if size >= SIZE_BYTE:
                    data = self.connection.recv(SIZE_BYTE)
                else:
                    data = self.connection.recv(size)
                
                if not data:
                    break
                
                size -= len(data)
                img_str += data
            # ret, jpeg = cv2.imencode('.jpg', cv2.imdecode(np.frombuffer(img_str, np.uint8), 1))
            frame = np.frombuffer(img_str, np.uint8)
            frame = cv2.imdecode(frame, 1)
            return frame
        except Exception as e:
            print('Errors: ', e)
            pass
