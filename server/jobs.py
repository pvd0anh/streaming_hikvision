
import cv2
import numpy as np

import grpc
import dl_server_pb2 as dl_server_pb2
import dl_server_pb2_grpc as dl_server_pb2_grpc

CHANNEL = grpc.insecure_channel('0.0.0.0:50051')
STUB = dl_server_pb2_grpc.DLServerStub(CHANNEL)

class ImageProc(object):
    def __init__(self):
        pass

    def __str__(self):
        pass

    def run(self):
        pass

class PoseEstimator(ImageProc):
    """ Pose estimator """

    def __init__(self):
        super(PoseEstimator, self).__init__()

    def __str__(self):
        return "Pose estimator"

    def run(self, img, bbox=''):
        _, buffer = cv2.imencode('.jpg', img)
        request = dl_server_pb2.DLImageTaskRequest(task_name=str(self), image=buffer.tobytes(), bbox=bbox)
        response = STUB.proceed_image_task(request)
        img = cv2.imdecode(np.frombuffer(response.image, np.uint8), 1)
        return img
    
class SpeedMeasurement(ImageProc):
    """ Counting time """

    def __init__(self):
        super(SpeedMeasurement, self).__init__()

    def __str__(self):
        return "Counting time"

    def run(self, img, bbox=''):
        _, buffer = cv2.imencode('.jpg', img)
        request = dl_server_pb2.DLImageTaskRequest(task_name=str(self), image=buffer.tobytes(), bbox=bbox)
        response = STUB.proceed_image_task(request)
        img = cv2.imdecode(np.frombuffer(response.image, np.uint8), 1)
        return img


class PlayerTracking(ImageProc):
    """ Player tracking """

    def __init__(self):
        super(PlayerTracking, self).__init__()

    def __str__(self):
        return "Player tracking"

    def run(self, img, bbox=''):
        _, buffer = cv2.imencode('.jpg', img)
        request = dl_server_pb2.DLImageTaskRequest(task_name=str(self), image=buffer.tobytes(), bbox=bbox)
        response = STUB.proceed_image_task(request)
        img = cv2.imdecode(np.frombuffer(response.image, np.uint8), 1)
        return img

class DrawPlayerTrajectory(ImageProc):
    """ Draw player trajectory """

    def __init__(self):
        super(DrawPlayerTrajectory, self).__init__()

    def __str__(self):
        return "Draw player trajectory"

    def run(self, img, bbox=''):
        _, buffer = cv2.imencode('.jpg', img)
        request = dl_server_pb2.DLImageTaskRequest(task_name=str(self), image=buffer.tobytes(), bbox=bbox)
        response = STUB.proceed_image_task(request)
        img = cv2.imdecode(np.frombuffer(response.image, np.uint8), 1)
        return img


class FeetJuggleCounting(ImageProc):
    """ Feet juggle counting"""

    def __init__(self):
        super(FeetJuggleCounting, self).__init__()

    def __str__(self):
        return "Feet juggle counting"

    def run(self, img, bbox=''):
        _, buffer = cv2.imencode('.jpg', img)
        request = dl_server_pb2.DLImageTaskRequest(task_name=str(self), image=buffer.tobytes(), bbox=bbox)
        response = STUB.proceed_image_task(request)
        img = cv2.imdecode(np.frombuffer(response.image, np.uint8), 1)
        return img


class HeadJuggleCounting(ImageProc):
    """ Head juggle counting """

    def __init__(self):
        super(HeadJuggleCounting, self).__init__()

    def __str__(self):
        return "Head juggle counting"

    def run(self, img, bbox=''):
        _, buffer = cv2.imencode('.jpg', img)
        request = dl_server_pb2.DLImageTaskRequest(task_name=str(self), image=buffer.tobytes(), bbox=bbox)
        response = STUB.proceed_image_task(request)
        img = cv2.imdecode(np.frombuffer(response.image, np.uint8), 1)
        return img