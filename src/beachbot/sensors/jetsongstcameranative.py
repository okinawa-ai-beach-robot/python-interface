import os, threading
import cv2
from beachbot.config import logger

try:
    from jetson_utils import videoSource, videoOutput
    from jetson_utils import cudaImage, cudaToNumpy
    import jetson_utils
except ModuleNotFoundError as ex:
    logger.warning(
        "Jetson utils not installed or not available! JetsonGstCameraNative not available!"
    )


class JetsonGstCameraNative:
    def __init__(self, width=1280, height=720, fps=15, dev_id=0, autostart=True) -> None:

        self.bgr_img = jetson_utils.cudaAllocMapped(
            width=width, height=height, format="bgr8"
        )

        self._width=width
        self._height=height
        self._fps=fps
        self._dev_id=dev_id

        self._is_running=False
        if autostart:
            self.start()


    @staticmethod
    def list_cameras():
        print(os.popen("v4l2-ctl --list-devices").read())
        print(os.popen("v4l2-ctl --list-formats-ext").read())

    def start(self):
        self._camera = videoSource(
            "csi://" + str(self._dev_id),
            options={
                "width": self._width,
                "height": self._height,
                "framerate": self._fps,
                "numBuffers": 2,
                "flipMethod": "vertical-flip",
            },
        )
        self._is_running = True

    def read(self):
        try:
            cuda_img = self._camera.Capture()
            jetson_utils.cudaConvertColor(cuda_img, self.bgr_img)
            bgr_frame = jetson_utils.cudaToNumpy(self.bgr_img)
            jetson_utils.cudaDeviceSynchronize()
            self._frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        except:
            self._frame = None

        # self._frame = cudaToNumpy(cuda_img, isBGR=True)
        return self._frame

    def stop(self):
        if self.is_running(self):
            self._is_running = False
            self._camera.Close()

    def is_running(self):
        return self._is_running

    def get_size(self):
        return (int(self._camera.GetWidth()), int(self._camera.GetHeight()))
