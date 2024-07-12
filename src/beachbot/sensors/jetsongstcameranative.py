import os, threading
import cv2
from .. import logger

try:
    from jetson_utils import videoSource, videoOutput
    from jetson_utils import cudaImage, cudaToNumpy
    import jetson_utils
except ModuleNotFoundError as ex:
    logger.warning(
        "Jetson utils not installed or not available! JetsonGstCameraNative not available!"
    )


class JetsonGstCameraNative:
    def __init__(self, width=1280, height=720, fps=15, dev_id=0) -> None:
        self._camera = videoSource("csi://" + str(dev_id), options={"width": width, "height": height, "framerate": fps, "numBuffers": 2, "flipMethod": "vertical-flip"})
        self.bgr_img = jetson_utils.cudaAllocMapped(width=width, height=height, format="bgr8")

    @staticmethod
    def list_cameras():
        print(os.popen("v4l2-ctl --list-devices").read())
        print(os.popen("v4l2-ctl --list-formats-ext").read())

    def read(self):
        cuda_img = self._camera.Capture()
        jetson_utils.cudaConvertColor(cuda_img, self.bgr_img)
        bgr_frame = jetson_utils.cudaToNumpy(self.bgr_img)
        jetson_utils.cudaDeviceSynchronize()
        self._frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)

        #self._frame = cudaToNumpy(cuda_img, isBGR=True)
        return self._frame

    def stop(self):
        self._camera.Close()

    def get_size(self):
        return (int(self._camera.GetWidth()), int(self._camera.GetHeight()))
