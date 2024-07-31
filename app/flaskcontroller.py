import sys
import signal
from flask import Flask, render_template, request
from beachbot.manipulators import Motor, DifferentialDrive
import beachbot.sensors
from beachbot import logger
import Jetson.GPIO as GPIO
import time
from jetson_utils import videoSource, videoOutput

app = Flask(__name__)



# There are three possible backend to read images from the camera devices
# cam1 = beachbot.sensors.UsbCameraOpenCV(width=640, height=480, fps=25, dev_id=1)
# cam1 = beachbot.sensors.JetsonCsiCameraOpenCV()
cam1 = beachbot.sensors.JetsonGstCameraNative()
# retrieve information on video stream:
capture_width, capture_height = cam1.get_size()
# Create video file writer, for now only one backend is implemented (opencv):
videowriter = beachbot.utils.VideoWriterOpenCV(None, fps=10, capture_width=capture_width, capture_height=capture_height )
# initiate threaded recording into video file
videowriter.start_recording(cam1)

pwm_pins = [32, 33]
gpio_pins = [15, 7, 29, 31]
_frequency_hz = 5000

GPIO.setmode(GPIO.BOARD)

motor_left = Motor("motor_left", pwm_pins[0], gpio_pins[0], gpio_pins[1], _frequency_hz)
motor_right = Motor("motor_right", pwm_pins[1], gpio_pins[2], gpio_pins[3], _frequency_hz)

robot_drive = DifferentialDrive(motor_left,motor_right)

sleep_time = 0.1


def cleanup():
    print("Exit, cleaning up...")
    robot_drive.cleanup()
    motor_left.change_speed(0)
    motor_right.change_speed(0)
    motor_left.cleanup()
    motor_right.cleanup()
    videowriter.close()
    cam1.stop()
    try:
        GPIO.cleanup()
    except Exception as ex:
        logger.error("GPIO cleanup failed: " + str(ex))
    sys.exit(0)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stop", methods=["POST"])
def stop():
    # Call your function here, e.g.,
    robot_drive.set_target(0,0)
    return f"Speed changed to {0}"


@app.route("/left", methods=["POST"])
def left():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    robot_drive.set_target(int(speed),int(speed))
    print(f"Speed changed to left {speed}")
    return f"Speed changed to {speed}"


@app.route("/right", methods=["POST"])
def right():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    robot_drive.set_target(-int(speed),int(speed))
    print(f"Speed changed to right {speed}")
    return f"Speed changed to {speed}"


@app.route("/forward", methods=["POST"])
def forward():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    robot_drive.set_target(0,int(speed))
    print(f"Speed changed to forward {speed}")
    return f"Speed changed to {speed}"


@app.route("/backward", methods=["POST"])
def backward():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    robot_drive.set_target(0,-int(speed))
    print(f"Speed changed to backward {speed}")
    return f"Speed changed to {speed}"


def handler(signal, frame):
  print('CTRL-C pressed!')
  cleanup()
  sys.exit(0)
signal.signal(signal.SIGINT, handler)
#signal.pause()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
