import requests

from pathlib import Path
from os import walk

import base64
import signal
import time

import cv2
import numpy as np


import sys
import signal
from beachbot.manipulators import Motor, DifferentialDrive
import beachbot.sensors
import beachbot.utils
from beachbot import logger
import Jetson.GPIO as GPIO
import time


from fastapi import Response

from nicegui import Client, app, core, run, ui
from nicegui import app, ui


tab_names = ["Control", "Live View", "Recordings"]


# There are three possible backend to read images from the camera devices
# cam1 = beachbot.sensors.UsbCameraOpenCV(width=640, height=480, fps=25, dev_id=1)
# cam1 = beachbot.sensors.JetsonCsiCameraOpenCV()
cam1 = beachbot.sensors.JetsonGstCameraNative()
# retrieve information on video stream:
capture_width, capture_height = cam1.get_size()
# Create video file writer, for now only one backend is implemented (opencv):
videowriter = None  # beachbot.utils.VideoWriterOpenCV(None, fps=10, capture_width=capture_width, capture_height=capture_height )


video_is_recording = False

pwm_pins = [32, 33]
gpio_pins = [15, 7, 29, 31]
_frequency_hz = 5000

GPIO.setmode(GPIO.BOARD)

motor_left = Motor("motor_left", pwm_pins[0], gpio_pins[0], gpio_pins[1], _frequency_hz)
motor_right = Motor(
    "motor_right", pwm_pins[1], gpio_pins[2], gpio_pins[3], _frequency_hz
)

robot_drive = DifferentialDrive(motor_left, motor_right)

sleep_time = 0.1


media = Path(beachbot.utils.VideoWriterOpenCV.get_base_path())
app.add_media_files("/my_videos", media)

# image placeholder in case no video device available:
black_1px = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII="
placeholder = Response(
    content=base64.b64decode(black_1px.encode("ascii")), media_type="image/png"
)


def toggle_recoding(doit):
    global video_is_recording, videowriter
    if doit and not video_is_recording:
        videowriter = beachbot.utils.VideoWriterOpenCV(
            None, fps=10, capture_width=capture_width, capture_height=capture_height
        )
        # initiate threaded recording into video file
        videowriter.start_recording(cam1)
        print("Start recording")
        video_is_recording = True
    elif not doit:
        if videowriter is not None:
            videowriter.close()
            print("Stop recording")
        video_is_recording = False


def joystick_move(data):
    coordinates.set_text(f"{data.x:.3f}, {data.y:.3f}")
    robot_drive.set_target(data.x * 100, data.y * 100)


def joystick_end():
    coordinates.set_text("0, 0")
    robot_drive.set_target(0, 0)


def sys_shutdown():
    print("Bye bye ...")
    beachbot.utils.shutdown()


def change_media(file):
    print("cange video:", "/my_videos/" + file)
    uivideo.set_source("/my_videos/" + file)


def tab_select_event():
    global live_update_timer, tab_names, video_image
    try:
        if tab_panel.value == tab_names[1]:
            if live_update_timer is None:
                live_update_timer = ui.timer(
                    interval=0.5,
                    callback=lambda: video_image.set_source(
                        f"/video/frame?{time.time()}"
                    ),
                )
        else:
            if live_update_timer is not None:
                live_update_timer.cancel()
                live_update_timer = None
        if tab_panel.value == tab_names[2]:
            print("reload files...")
            reload_files()
    except Exception as ex:
        print(ex)


def reload_files():
    global selector, media
    selector.clear()
    with selector:
        for dirpath, dirnames, filenames in walk(media):
            for fname in filenames:
                if fname.endswith(".mp4"):
                    ui.item(fname, on_click=lambda x=fname: change_media(x))


def convert(frame: np.ndarray) -> bytes:
    _frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    _, imencode_image = cv2.imencode(".jpg", _frame)
    return imencode_image.tobytes()


@app.get("/video/frame")
# Thanks to FastAPI's `app.get`` it is easy to create a web route which always provides the latest image from OpenCV.
async def grab_video_frame() -> Response:
    # The `video_capture.read` call is a blocking function.
    # So we run it in a separate thread (default executor) to avoid blocking the event loop.
    frame = await run.io_bound(cam1.read)
    if frame is None:
        return placeholder
    # `convert` is a CPU-intensive function, so we run it in a separate process to avoid blocking the event loop and GIL.
    jpeg = await run.cpu_bound(convert, frame)
    return Response(content=jpeg, media_type="image/jpeg")


# # For non-flickering image updates an interactive image is much better than `ui.image()`.
# video_image = ui.interactive_image().classes('w-full h-full')
# # A timer constantly updates the source of the image.
# # Because data from same paths are cached by the browser,
# # we must force an update by adding the current timestamp to the source.
# ui.timer(interval=0.1, callback=lambda: video_image.set_source(f'/video/frame?{time.time()}'))


with ui.tabs().classes("w-full") as tabs:
    # tabs.on('click', lambda s: reload_files())
    one = ui.tab(tab_names[0])
    two = ui.tab(tab_names[1])
    three = ui.tab(tab_names[2])
tab_panel = ui.tab_panels(tabs, value=two).classes("w-full")
tab_panel.on_value_change(tab_select_event)
with tab_panel:
    with ui.tab_panel(one):
        with ui.row():
            toggle1 = ui.toggle(
                {1: "Video Stop", 2: "Record"}, value=1
            ).on_value_change(lambda v: toggle_recoding(v.value == 2))
            with ui.dropdown_button("System", auto_close=True):
                ui.item("Exit Server", on_click=app.shutdown)
                ui.item("Shut Down", on_click=sys_shutdown)
        ui.label("Robot Control Panel")
        ui.add_head_html(
            """
<style>
    .custom-joystick[data-joystick] div {
        width: calc(90vmin);
        height: calc(90vmin);
    }
</style>
"""
        )
        ui.joystick(
            color="blue",
            size=350,
            on_move=lambda e: joystick_move(e),
            on_end=lambda _: joystick_end(),
        ).classes("custom-joystick")
        coordinates = ui.label("0, 0")

    with ui.tab_panel(two):
        video_image = ui.interactive_image().classes("w-full h-full")
    with ui.tab_panel(three):
        with ui.dropdown_button("Select File...", auto_close=True) as selector:
            pass
        ui.label("Media Viewer:")
        ui.label(beachbot.utils.VideoWriterOpenCV.get_base_path())
        uivideo = ui.video("/my_videos/clouds.mp4")

reload_files()

# TODO add, only timing when view is on preview!!!
live_update_timer = ui.timer(
    interval=0.5, callback=lambda: video_image.set_source(f"/video/frame?{time.time()}")
)


# media.mkdir(exist_ok=True)
# r = requests.get('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')
# (media  / 'clouds.mp4').write_bytes(r.content)


async def disconnect() -> None:
    """Disconnect all clients from current running server."""
    for client_id in Client.instances:
        await core.sio.disconnect(client_id)


def handle_sigint(signum, frame) -> None:
    # `disconnect` is async, so it must be called from the event loop; we use `ui.timer` to do so.
    ui.timer(0.1, disconnect, once=True)
    # Delay the default handler to allow the disconnect to complete.
    ui.timer(1, lambda: signal.default_int_handler(signum, frame), once=True)


async def cleanup() -> None:
    # This prevents ugly stack traces when auto-reloading on code change,
    # because otherwise disconnected clients try to reconnect to the newly started server.
    await disconnect()

    print("Exit, cleaning up...")
    joystick_end()
    robot_drive.cleanup()
    motor_left.change_speed(0)
    motor_right.change_speed(0)
    motor_left.cleanup()
    motor_right.cleanup()
    if videowriter is not None:
        videowriter.close()
    cam1.stop()
    try:
        GPIO.cleanup()
    except Exception as ex:
        logger.error("GPIO cleanup failed (bug in GPIO?)")
    # sys.exit(0)


app.on_shutdown(cleanup)
# We also need to disconnect clients when the app is stopped with Ctrl+C,
# because otherwise they will keep requesting images which lead to unfinished subprocesses blocking the shutdown.
signal.signal(signal.SIGINT, handle_sigint)


ui.run(reload=False, port=8080, show=False)
