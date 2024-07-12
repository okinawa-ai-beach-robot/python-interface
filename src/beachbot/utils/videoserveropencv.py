import cv2
import datetime
import sys


class VideoServerOpenCV:
    def __init__(self, fps=10, capture_width=1920, capture_height=1080,  port=5001) -> None:
        
        #accel, orin does not support: gst_out = "appsrc ! video/x-raw, format=BGR ! queue ! videoconvert ! video/x-raw,format=BGRx ! nvvidconv ! nvv4l2h264enc ! h264parse ! rtph264pay pt=96 config-interval=1 ! udpsink host=127.0.0.1 port=" + str(port) + " "
        gst_out = "appsrc ! video/x-raw, format=BGR ! queue ! videoconvert ! video/x-raw,format=BGRx ! videoconvert ! x264enc ! h264parse ! rtph264pay pt=96 config-interval=1 ! udpsink host=192.168.55.100 port=" + str(port) + " sync=false" # sync=false -e
        #gst_out = "appsrc ! video/x-raw, format=BGR ! queue ! videoconvert ! video/x-raw, format=BGRx ! videoconvert ! x264enc ! video/x-h264, stream-format=byte-stream ! h264parse ! rtph264pay pt=96 config-interval=1 ! udpsink host=192.168.55.100 port=" + str(port) + " sync=false -e"
        
        #gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM), format=NV12, width=1920, height=1080' ! nvvidconv flip-method=2 ! nvv4l2h264enc insert-sps-pps=true ! h264parse ! rtph264pay pt=96 ! udpsink host=(IP or Domain from macOS) port="+str(port)+" sync=false -e
        vidserver = cv2.VideoWriter(gst_out, cv2.CAP_GSTREAMER, 0, float(fps), (int(capture_width), int(capture_height)))

        #vidserver = cv2.VideoWriter("appsrc ! video/x-raw, format=BGR ! queue ! videoconvert ! video/x-raw, format=BGRx ! nvvidconv ! omxh264enc ! video/x-h264, stream-format=byte-stream ! h264parse ! rtph264pay pt=96 config-interval=1 ! udpsink host=[TARGET IP/HOST] port=1234", cv2.CAP_GSTREAMER, 0, 25.0, (width,height))


        if not vidserver.isOpened():
            print("ERROR opening stream server!", file=sys.stderr)
            vidserver=None


        self.vidserver = vidserver

    def add_frame(self, frame):
        _frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.vidserver.write(_frame)

    def close(self):
        self.vidserver.release()




