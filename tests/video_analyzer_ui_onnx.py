#!/usr/bin/env python3
import base64
import signal
import time
import os
import sys
from datetime import datetime
import time

import cv2
import numpy as np
from fastapi import Response

from nicegui import Client, app, core, run, ui

import beachbot




detect_timer =beachbot.utils.Timer()
read_timer = beachbot.utils.Timer()
preprocess_timer = beachbot.utils.Timer()




vid_file = beachbot.get_data_path()+os.path.sep+"video_beach_test.mp4"
model_file = beachbot.get_model_path()+os.path.sep+"beachbot_yolov5s_beach-cleaning-object-detection__v3-augmented_ver__2__yolov5pytorch_1280"+os.path.sep+"best.onnx"

ai_detect = beachbot.ai.Yolo5Onnx(model_file=model_file, use_accel=False)

# In case you don't have a webcam, this will provide a black placeholder image.
black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
placeholder = Response(content=base64.b64decode(black_1px.encode('ascii')), media_type='image/png')


# OpenCV is used to access the webcam.
#video_capture = cv2.VideoCapture(0)

video_capture = cv2.VideoCapture(vid_file)
# # get total number of frames
totalFrames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
# randomFrameNumber=random.randint(0, totalFrames)
# # set frame position
print("Open video")
video_capture.set(cv2.CAP_PROP_POS_FRAMES,0)
success, frame_bgr = video_capture.read()
frame = frame_bgr[..., ::-1]  # OpenCV image (BGR to RGB)
if not success:
    print("Video file could not be loaded:")
    sys.exit(-1)

img_width = frame.shape[1]
img_height = frame.shape[0]
print("Video loaded, resolution is", str(img_width)+"x"+str(img_height))

print("Load AI model")
class_threshold=0.25
confidence_threshold=0.2
frame = ai_detect.crop_and_scale_image(frame)
class_ids, confidences, boxes = ai_detect.apply_model_percent(frame, confidence_threshold=confidence_threshold, class_threshold=class_threshold)
print("[ result is: ", [class_ids, confidences, boxes], "]")

print("Prepare serer ...")


def convert(frame_bgr: np.ndarray) -> bytes:
    _, imencode_image = cv2.imencode('.jpg', frame_bgr)
    return imencode_image.tobytes()



def add_imgbox(pleft=0, ptop=0, w=0, h=0, clsstr=None):
    # color = 'SkyBlue'
    color = '#FF0000' 
    image.content += f'<rect x="{pleft*100}%" y="{ptop*100}%" ry="15" height="{h*100}%" width="{w*100}%" fill="none" stroke="{color}" stroke-width="4" />'
    if clsstr is not None:
        image.content += f'<text text-anchor="start" x="{pleft*100}%" y="{ptop*100}%" stroke="{color}" font-size="2em">{clsstr}</text>'
    
def rframe(fnum=0):
    video_capture.set(cv2.CAP_PROP_POS_FRAMES,int(fnum))
    
    with read_timer as t:
        succ, frame_bgr = video_capture.read()
        frame = frame_bgr[..., ::-1]  # OpenCV image (BGR to RGB)
        
    with preprocess_timer as t:
        frame = ai_detect.crop_and_scale_image(frame)

    confidence_threshold = slider_th.value/1000.0
    class_threshold = slider_clsth.value/1000.0

    with detect_timer as t:
        class_ids, confidences, boxes = ai_detect.apply_model_percent(frame, confidence_threshold=confidence_threshold, class_threshold=class_threshold)

    image.content = ""
    for classid, confidence, box in zip(class_ids, confidences, boxes):
        if confidence >= 0.01:
            add_imgbox(*box, ai_detect.list_classes[classid])
    #print(obj_res)
    return succ, frame_bgr

@app.get('/file/frame')
# Thanks to FastAPI's `app.get`` it is easy to create a web route which always provides the latest image from OpenCV.
async def grab_file_frame(fnum=0) -> Response:
    if video_capture is None or not video_capture.isOpened():
        return placeholder
    # The `video_capture.read` call is a blocking function.
    # So we run it in a separate thread (default executor) to avoid blocking the event loop.
    _, frame_bgr = await run.io_bound(lambda : rframe(fnum))
    if frame_bgr is None:
        return placeholder
    # `convert` is a CPU-intensive function, so we run it in a separate process to avoid blocking the event loop and GIL.
    jpeg = await run.cpu_bound(convert, frame_bgr)

    print("Read stat:", read_timer)
    print("Preprocess stat:", preprocess_timer)
    print("Detect stat:", detect_timer)
    
    return Response(content=jpeg, media_type='image/jpeg')


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
    # Release the webcam hardware so it can be used by other applications again.
    video_capture.release()

app.on_shutdown(cleanup)
# We also need to disconnect clients when the app is stopped with Ctrl+C,
# because otherwise they will keep requesting images which lead to unfinished subprocesses blocking the shutdown.
signal.signal(signal.SIGINT, handle_sigint)








async def handle_connection(cl : Client):
    await cl.connected()
    res = await cl.run_javascript("[window.screen.width,window.screen.height]")


def handle_start():
    dt = datetime.now()

app.on_connect(handle_connection)
app.on_startup(handle_start)

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='settings').props('flat color=white')
    ui.space()
    ui.button( icon='error').props('flat color=white')

with ui.footer(value=False) as footer:
    ui.label('Beachbot robot, OIST x Community, Onna-son, Okinawa')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Configure:')
    with ui.card().classes('w-full'):
        lbl1 = ui.label('System:')
        ui.button('Shut Down', on_click=lambda: os.app.shutdown())
        ui.separator()
        ui.switch("1")
        ui.switch("2")
        ui.switch("3")
        #ui.timer(1.0, lambda: ui.label('Tick!'), once=True)


with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')


with ui.row().classes('w-full'):
    with ui.card().style('max-width: 90%;'):
        def up_img(obj : ui.interactive_image, pleft=0, ptop=0, w=25, h=25, val=0):
            #color = 'SkyBlue'
            #color = '#FF0000' 
            #obj.content = f'<rect x="{pleft}%" y="{ptop}%" ry="15" height="{h}%" width="{w}%" fill="none" stroke="{color}" stroke-width="4" />'
            #obj.set_source(f'/video/frame?{time.time()}')
            obj.set_source(f'/file/frame?fnum={val}&t={time.time()}')
        ui.label('Video Analyzer:')
        image = ui.interactive_image(source="file/frame?fnum=0",size=(img_width,img_height)).style('width: 100%')
        slider = ui.slider(min=0, max=totalFrames, value=0, on_change=lambda x: up_img(image, val=x.value))
        ui.label().bind_text_from(slider, 'value', backward=lambda a: f'Frame {a} of {totalFrames}')
        slider_th = ui.slider(min=1, max=500, value=200, on_change=lambda x: up_img(image, val=slider.value))
        ui.label().bind_text_from(slider_th, 'value', backward=lambda a: f'Confidence threshold is {a/1000.0}')
        slider_clsth = ui.slider(min=1, max=500, value=250, on_change=lambda x: up_img(image, val=slider.value))
        ui.label().bind_text_from(slider_clsth, 'value', backward=lambda a: f'Class threshold is {a/1000.0}')


beachbot.utils.kill_by_port(4321)
ui.run(title="Beachbot Video Analyzer", port=4321)


