from .robotcontroller import RobotController, BoxDef
from ..robot import RobotInterface
from ..utils.controllercollection import PIDController


class ApproachDebris(RobotController):
    def __init__(self):
        super().__init__()

        self.ctrl = PIDController(setpoint_x=0.5, setpoint_y=0.25, kp=0.1)

    def update(self, robot: RobotInterface, detections: list[BoxDef]=None, debug=False):
        trash_to_follow : BoxDef = None

        if len(detections)>0:
            # Detected trash
            # Todo select best trash in case multiple detections, for now, take first one:
            trash_to_follow = detections[0]

        if trash_to_follow:
            # approach trash
            trash_x = trash_to_follow.left+trash_to_follow.w/2
            trash_y = 1.0 - (trash_to_follow.top+trash_to_follow.h/2) # 0 is bottom, 1 is top

            if debug:
                print("trash position:", trash_x, trash_y)

            dir_command = self.ctrl.get_output(trash_x, trash_y)
            if debug:
                print("dir_command:",dir_command)
            robot.set_target_velocity(-dir_command[0], -dir_command[1])



        else:
            # Do random movements to find a trash:
            pass
        
        