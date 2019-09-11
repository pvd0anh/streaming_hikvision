from threading import Thread

from src.client_record import ClientRecord
from src.client import Client

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cam_host', type=str, default='192.168.1.64')
    parser.add_argument('--cam_port', type=int, default=554)
    parser.add_argument('--server_host', type=str, default='118.69.65.157')
    parser.add_argument('--server_port', type=int, default=8006)

    args = parser.parse_args()

    client_record = ClientRecord(args.cam_host, args.cam_port)
    client = Client(args.server_host, args.server_port)

    Thread(target=client_record.proceed).start()
    Thread(target=client.proceed).start()

if __name__ == '__main__':
    main()