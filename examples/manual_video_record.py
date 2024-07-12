
import beachbot
import time


# A reference to a image viewer can be used to display images:
viewer = beachbot.utils.ImageViewerMatplotlib


# There are two possible backend to read images from the camera devices
# cam1 = beachbot.sensors.UsbCameraOpenCV(width=640, height=480, fps=25, dev_id=1)
# cam1 = beachbot.sensors.JetsonCsiCameraOpenCV()
cam1 = beachbot.sensors.JetsonGstCameraNative()

# retrieve information on video stream:
capture_width, capture_height = cam1.get_size()

# Create video file writer, for now only one backend is implemented (opencv):
videowriter = beachbot.utils.VideoWriterOpenCV("filename_tmp.mp4", fps=10, capture_width=capture_width, capture_height=capture_height )

# just for fun: print list of video devices and current resolution to console:
cam1.list_cameras()
print("My resolution is:", cam1.get_size())

time.sleep(1)

# read first frame of camera:
img1 = cam1.read()

# Instantiate the image viewer class and display the first frame
w1 = viewer("Title")
w1.show(img1)


# The following loop reads frames from the camera and writes them to the video file:
try:
    for i in range(200):
        # read frame:
        img1 = cam1.read()
        # display camera image:
        w1.show(img1)
        # Write into file:
        videowriter.add_frame(img1)
        # Wait for a certain amount of time:
        time.sleep(0.1)
except KeyboardInterrupt as ex:
    pass

# Do not forget to close preview, video devices and video writer objects, 
# - Camera access could be blocked if not closed correctly
# - The frames may only be written to the file during closing as they can be buffered im memory
w1.close()
videowriter.close()
cam1.stop()

