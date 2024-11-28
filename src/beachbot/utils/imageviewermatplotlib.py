import matplotlib.pyplot as plt




class ImageViewerMatplotlib:
    def __init__(self, title=None) -> None:
        self.fig = plt.figure()
        self.ax = plt.subplot(111)
        self.im = None

    def show(self, img):
        if self.im is None:
            self.im = self.ax.imshow(img)
        else:
            self.im.set_data(img)
        self.fig.canvas.draw()
        self.fig.show()
        self.fig.canvas.flush_events()

    # def getKey(self, timeout=1):
    #     return cv2.waitKey(timeout) & 0xFF

    def close(self):
        plt.close(self.fig)

    @staticmethod
    def close_all():
        plt.close("all")
