#!/usr/bin/env python3
from datetime import datetime

from nicegui import Client, app, ui

dt = datetime.now()

async def handle_connection(cl : Client):
    global dt
    dt = datetime.now()
    await cl.connected()
    res = await cl.run_javascript("[window.screen.width,window.screen.height]")

    print(dt, res)
def handle_start():
    global dt
    dt = datetime.now()
    print(dt, "start")
app.on_connect(handle_connection)
app.on_startup(handle_start)

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='settings').props('flat color=white')
    with ui.tabs() as tabs:
        print("taba")
        ui.tab('Status')
        ui.tab('Control')
        ui.tab('WIP')
    ui.space()
    ui.button( icon='error').props('flat color=white')

with ui.footer(value=False) as footer:
    ui.label('Beachbot robot, OIST x Community, Onna-son, Okinawa')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Configure:')
    with ui.card().classes('w-full'):
        lbl1 = ui.label('System:')
        ui.button('Shut Down', on_click=lambda: ui.label('Please Wait'))
        ui.separator()
        ui.switch("Arm")
        ui.switch("Object detector")
        ui.switch("Auto Locomotion")
        #ui.timer(1.0, lambda: ui.label('Tick!'), once=True)
    with ui.card().classes('w-full'):
        lbl1 = ui.label('AI:')
        ui.select(['Camera Base', 'Camera Gripper'], value='Camera Base', on_change=lambda x: ui.notify(x)).classes('w-full')
        ui.select(['YOLOv5, Dataset 1', 'WIP'], value='YOLOv5, Dataset 1', on_change=lambda x: ui.notify(x)).classes('w-full')



with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='Status').classes('w-full'):
    with ui.tab_panel('Status').style('width: 50%'):
        with ui.row().classes('w-full'):
            with ui.card().style('width: 45%'):
                ui.label('Camera system:')
                image = ui.interactive_image(source="https://picsum.photos/id/684/640/360",size=(512,512)).style('width: 100%')
                slider = ui.slider(min=0, max=100, value=50)
                ui.label().bind_text_from(slider, 'value', backward=lambda a: f'Object threshold: {a}')
                def up_img(obj : ui.interactive_image, pleft=0, ptop=0, w=25, h=25):
                    color = 'SkyBlue'
                    color = '#FF0000' 
                    obj.content += f'<rect x="{pleft}%" y="{ptop}%" ry="15" height="{h}%" width="{w}%" fill="none" stroke="{color}" stroke-width="4" />'

                ui.timer(1.0, lambda: up_img(image))
            with ui.card().style('width: 45%'):
                ui.label('HW Monitor:')
                ui.label("IP: [xx.xx.xx.xx]")
                ui.label("WiFi: [wifiname]")
                ui.label("Name: beachbot.local")
                ui.label("Battery: 12.xV, 105%")
                ui.label("CPU: 25%, 250C")
                ui.label("Solar: 123W")
        
    with ui.tab_panel('Control').style('width: 50%'):
        with ui.row().classes('w-full'):
            with ui.card().style('width: 45%'):
                ui.label('Locomotion:')
                ui.add_head_html('''
                <style>
                    .custom-joystick[data-joystick] div {
                        width: 400px;
                        height: 400px;
                    }
                </style>
                ''')
                #ui.timer(1.0, lambda: up_img(image))
                ui.joystick(color='blue', size="200",
                on_move=lambda e: coordinates.set_text(f"{e.x:.3f}, {e.y:.3f}"),
                on_end=lambda _: coordinates.set_text('0, 0')).classes('custom-joystick')
                coordinates = ui.label('0, 0')
            with ui.card().style('width: 45%'):
                ui.label('Arm:')
                with ui.row().classes('w-full items-center'):
                    ui.label('Status: Uninitialized')
                    ui.button('Initialize!', on_click=lambda: ui.notify('You clicked me!'))
                with ui.tabs().classes('w-full') as tabs:
                    tpos = ui.tab('Position')
                    tkin = ui.tab('Inv. Kin.')
                    tteach = ui.tab('Teaching')
                with ui.tab_panels(tabs, value=tpos).classes('w-full'):
                    with ui.tab_panel(tpos):
                        with ui.row().classes('w-full items-center'):
                            knobs = [ui.knob(0.5, show_value=True) for i in range(4)]
                    with ui.tab_panel(tkin):
                        ui.label('Second tab')
                    with ui.tab_panel(tteach):
                        ui.label('Joints are unlocked, please move robot by hand to new position.')     
                with ui.card().style('width: 100%'):
                    ui.label('Trajectory:')
                    ui.button('Add label', on_click=lambda: ui.label('Click!'))




    with ui.tab_panel('Record'):
        ui.label('Content of C')

ui.run(title="Beachbot", port=1234)
