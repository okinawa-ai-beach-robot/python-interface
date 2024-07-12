
import beachbot
import time


# There are two possible backend to read images from the camera devices
# cam1 = beachbot.sensors.UsbCameraOpenCV(width=640, height=480, fps=25, dev_id=1)
# cam1 = beachbot.sensors.JetsonCsiCameraOpenCV()
cam1 = beachbot.sensors.JetsonGstCameraNative()

# retrieve information on video stream:
capture_width, capture_height = cam1.get_size()

# Create video file writer, for now only one backend is implemented (opencv):
videowriter = beachbot.utils.VideoWriterOpenCV("filename_tmp.mp4", fps=10, capture_width=capture_width, capture_height=capture_height )

# just in case, wait to make sure that video device is ready
time.sleep(1)

# initiate threaded recording into video file
videowriter.start_recording(cam1)

# The following loop wait for a certain amount of time, while listening for keyboard events
try:
    for i in range(200):
        # Wait for a certain amount of time:
        time.sleep(0.1)
except KeyboardInterrupt as ex:
    pass

# Do not forget to close video devices and video writer objects, 
# - Camera access could be blocked if not closed correctly
# - The frames may only be written to the file during closing as they can be buffered im memory
videowriter.close()
cam1.stop()

