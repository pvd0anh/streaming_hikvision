# Important Settings

## Client

```
pip install numpy coils redis opencv-python
```

## Server

- Generate gRPC files

```bash
python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/dl_server.proto
```

# Demo

## Client

```
python client/run.py --cam_host [CAMERA HOST] --cam_port [CAMERA PORT] --server_host [SERVER HOST] --server_port [SERVER PORT]
```

By default:

- `cam_host`: 192.168.1.64
- `cam_port`: 554
- `server_port`: 118.69.65.157
- `server_port`: 8006

## Server

```
python server/run.py --host [SERVER HOST] --port [SERVER PORT] --http_host [HTTP SERVING PORT] --task [DL TASK]
```
By default:

- `host`: 0.0.0.0
- `port`: 8006
- `http_port`: 8007
- `task`: 'openpose'



# streaming_hikvision
