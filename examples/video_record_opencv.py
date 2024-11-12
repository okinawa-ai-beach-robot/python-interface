
import beachbot
import time


viewer = beachbot.utils.ImageViewerMatplotlib



# This alternative image viewer does not work yet... TODO
# viewer = beachbot.utils.ImageViewerJetson

#cam1 = beachbot.sensors.JetsonCsiCameraOpenCV()
cam1 = beachbot.sensors.JetsonGstCameraNative()

capture_width, capture_height = cam1.get_size()
vidoewriter = beachbot.utils.VideoWriterOpenCV("filename_tmp.mp4", fps=10, capture_width=capture_width, capture_height=capture_height )

cam1.list_cameras()
print("My resolution is:", cam1.get_size())
time.sleep(1)


img1 = cam1.read()
w1 = viewer("test")
w1.show(img1)


try:
    for i in range(200):
        img1 = cam1.read()
        w1.show(img1)
        vidoewriter.add_frame(img1)
        time.sleep(0.1)
except KeyboardInterrupt as ex:
    pass

w1.close()
vidoewriter.close()
cam1.stop()

