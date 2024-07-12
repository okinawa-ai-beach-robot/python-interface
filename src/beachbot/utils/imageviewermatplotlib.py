# import uuid
# import cv2
import matplotlib.pyplot as plt


class ImageViewerMatplotlib:
    def __init__(self, title=None) -> None:
        # self._winname = str(uuid.uuid1())
        # cv2.namedWindow(self._winname)
        # if title is not None:
        #     cv2.setWindowTitle(self._winname, title)
        #     cv2.waitKey(0)
        self.fig = plt.figure()
        self.ax = plt.subplot(111)
        self.im = None

    def show(self, img):
        # cv2.imshow(self._winname,img)
        if self.im is None:
            self.im = self.ax.imshow(img)
        else:
            self.im.set_data(img)
        self.fig.canvas.draw()
        self.fig.show()

    # def getKey(self, timeout=1):
    #     return cv2.waitKey(timeout) & 0xFF

    def close(self):
        # cv2.destroyWindow(self._winname)
        plt.close(self.fig)

    @staticmethod
    def close_all():
        # cv2.destroyAllWindows()
        plt.close("all")
