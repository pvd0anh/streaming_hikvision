# A simple use of network camera to stream data using socket

## As server

```
python server/server_socket.py --host [SERVER HOST] --port [SERVER PORT]
```

Ex:
```
python3 server/server_socket.py --host 0.0.0.0 --port 8006
```

By default:

- `host`: 0.0.0.0
- `port`: 8006

## As client

```
python client/client_socket.py --cam_host [CAMERA HOST] --cam_port [CAMERA PORT] --server_host [SERVER HOST] --server_port [SERVER PORT]
```
Ex: 

```
python3 client/client_socket.py --cam_host 192.168.1.64 --cam_port 554 --server_host 0.0.0.0 --server_port 8006
```

By default:

- `cam_host`: 192.168.1.64
- `cam_port`: 554
- `server_port`: 0.0.0.0 (change if want to stream over internet)
- `server_port`: 8006

