import cv2
import datetime, time
import threading


class VideoWriterOpenCV(threading.Thread):
    def __init__(self, filename=None, fps=10, capture_width=1920, capture_height=1080) -> None:
        if filename is None:
            filename  = datetime.now().strftime("%Y%m%d-%H%M%S")
        if "." not in filename:
            filename += ".mp4"


        fourcc = cv2.VideoWriter_fourcc(*'h264')
        #or 
        #fourcc = cv2.VideoWriter_fourcc(*'x264')
        #fourcc = cv2.VideoWriter_fourcc(*'avc1')
        #fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        #cfourcc = v2.VideoWriter_fourcc('M','J','P','G')
        ##sudo apt-get install ffmpeg x264 libx264-dev

        # adjust qiality with pipeline spec:
        # writer.open("appsrc ! videoconvert  !  avenc_mpeg4 bitrate=100000 ! mp4mux ! filesink location=video.mp4",CAP_GSTREAMER, 0, (double) 10, cv::Size(640, 480), true);

        self.vidfile = cv2.VideoWriter(filename, fourcc, fps, (capture_width,capture_height))
        self._fps = fps
        self._videosource = None

    def add_frame(self, frame):
        _frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.vidfile.write(_frame)

    def start_recording(self, videosource):
        self._stopped = False
        self._videosource = videosource
        super().start()

    def run(self):
        while not self._stopped:
            t_start = time.time()
            img = self._videosource.read()
            self.add_frame(img)
            t_end = time.time()
            t_wait = (1.0/self._fps)-(t_end-t_start)
            if t_wait>0:
                time.sleep(t_wait)


    def close(self):
        if self._stopped:
            self._stopped=True
            time.sleep(1.0/self._fps)
        self.vidfile.release()




