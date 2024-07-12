import os, threading
import cv2


class UsbCameraOpenCV(threading.Thread):
    def __init__(self, width=640, height=480, fps=25, dev_id=1) -> None:
        # Init superclass thread
        super().__init__()
        # do not block on exit:
        self.daemon = True
        self._stopped = True
        self._frame = None

        self._lock = threading.Lock()

        self._cap = cv2.VideoCapture(dev_id)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self._cap.set(cv2.CAP_PROP_FPS, fps)

        if self._cap.isOpened():
            self._cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.ret_val, bgr_frame = self._cap.read()
            self._frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
            self._stopped = False
            super().start()

    @staticmethod
    def list_cameras():
        print(os.popen("v4l2-ctl --list-devices").read())
        print(os.popen("v4l2-ctl -d /dev/video1 --list-formats-ext").read())

    def run(self):
        while not self._stopped:
            self._ret, bgr_frame = self._cap.read()
            with self._lock:
                self._frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        self._cap.release()

    def read(self):
        with self._lock:
            img_cpy = self._frame.copy()
        return img_cpy

    def stop(self):
        self._stopped = True
        self._cap.release()

    def get_size(self):
        if self._frame.shape is not None:
            return (self._frame.shape[1], self._frame.shape[0])
        return (0, 0)
        # This does not reflect actual size: return (int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
