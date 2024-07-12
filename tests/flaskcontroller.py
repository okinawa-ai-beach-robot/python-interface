from flask import Flask, render_template, request
from beachbot.manipulators import Motor
import Jetson.GPIO as GPIO
import time
from jetson_utils import videoSource, videoOutput, Log
import threading

app = Flask(__name__)

pwm_pins = [32, 33]
gpio_pins = [7, 15, 29, 31]
motor_driver_error_pins = [18, 22, 24, 26]
_frequency_hz = 50

GPIO.setmode(GPIO.BOARD)

motor1 = Motor(
    "motor1",
    pwm_pins[0],
    gpio_pins[0],
    gpio_pins[1],
    _frequency_hz,
    motor_driver_error_pins[0],
    motor_driver_error_pins[1],
)
motor2 = Motor(
    "motor2",
    pwm_pins[1],
    gpio_pins[2],
    gpio_pins[3],
    _frequency_hz,
    motor_driver_error_pins[2],
    motor_driver_error_pins[3],
)

sleep_time = 0.1

# create video sources & outputs
input = videoSource("csi://0", options={"width": 1280, "height": 800, "framerate": 15})
output = videoOutput(
    "webrtc://@:1234/my_stream",
    [
        'options={"width": 1280, "height": 800, "framerate": 15}',
        "--headless",
        "--output-save=./video_tmp.mp4",
    ],
)


def cleanup():
    GPIO.cleanup()
    motor1.cleanup()
    motor2.cleanup()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stop", methods=["POST"])
def stop():
    # Call your function here, e.g.,
    motor1.change_speed(0)
    motor2.change_speed(0)
    return f"Speed changed to {0}"


@app.route("/left", methods=["POST"])
def left():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    motor1.change_speed(int(50))
    motor2.change_speed(int(speed))
    return f"Speed changed to {speed}"


@app.route("/right", methods=["POST"])
def right():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    motor1.change_speed(int(speed))
    motor2.change_speed(int(50))
    return f"Speed changed to {speed}"


@app.route("/forward", methods=["POST"])
def forward():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    motor1.change_speed(int(speed))
    motor2.change_speed(int(speed))
    return f"Speed changed to {speed}"


@app.route("/backward", methods=["POST"])
def backward():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    motor1.change_speed(-int(speed))
    motor2.change_speed(-int(speed))
    return f"Speed changed to {speed}"


def video_loop():

    # capture frames until EOS or user exits
    numFrames = 0
    while numFrames < 1000:
        # capture the next image
        img = input.Capture()

        if img is None:  # timeout
            continue

        if numFrames % 25 == 0 or numFrames < 15:
            Log.Verbose(
                f"video-viewer:  captured {numFrames} frames ({img.width} x {img.height})"
            )

        numFrames += 1

        # render the image
        output.Render(img)

        # update the title bar
        output.SetStatus(
            "Video Viewer | {:d}x{:d} | {:.1f} FPS".format(
                img.width, img.height, output.GetFrameRate()
            )
        )

        # exit on input/output EOS
        if not input.IsStreaming() or not output.IsStreaming():
            break


if __name__ == "__main__":

    x = threading.Thread(target=video_loop)
    x.start()
    app.run(host="0.0.0.0", port=5000)
