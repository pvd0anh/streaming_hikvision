"""
Send frame to host server by socket
Usage:
   python client.py host port
"""
import time
import coils
import redis
import sys
import socket
import struct

MAX_FPS = 100
class RedisStore:
    def __init__(self, *args, **kwargs):
        """ Initialize the Redis store and framerate monitor. """
        self._store = redis.Redis()
        self._fps = coils.RateTicker((1, 5, 10))
        self._prev_image_id = None

    def get_image(self):
        while True:
            time.sleep(1./MAX_FPS)
            image_id = self._store.get('image_id')
            if image_id != self._prev_image_id:
                break
        self._prev_image_id = image_id
        image = self._store.get('image')
        # print('{} {:.2f}, {:.2f}, {:.2f} fps'.format(id(self), *self._fps.tick()))
        return image

class Client:
    def __init__(self, server_host, server_port):
        self.host = server_host
        self.port = server_port
        # initialize socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        # initialize redis store
        self.store = RedisStore()

    def proceed(self):
        while True:
            cur_sleep = 0
            try:
                time.sleep(cur_sleep)
                image_b64 = self.store.get_image()
                len_str = struct.pack('!i', len(image_b64))
                self.sock.sendall(len_str)
                self.sock.sendall(image_b64)
                cur_sleep = 0
            except Exception as e:
                print('Errors: ', e)
                cur_sleep += 0.1
                self.sock.connect((self.host,self.port))
                pass
    
