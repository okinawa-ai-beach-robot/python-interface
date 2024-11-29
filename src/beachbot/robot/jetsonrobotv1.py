from ..sensors import JetsonCsiCameraOpenCV, UsbCameraOpenCV
from ..manipulators import DifferentialDrive, JetsonMotor, RoArmM1
from .robotinterface import RobotInterface

try:
    import Jetson.GPIO as GPIO
except Exception:
    pass




class JetsonRobotV1(RobotInterface):
    def __init__(self):
        super().__init__()
        # Camera Setup:
        self.cameradevices[RobotInterface.CAMERATYPE.FRONT] = JetsonCsiCameraOpenCV()
        self.cameradevices[RobotInterface.CAMERATYPE.GRIPPER] = UsbCameraOpenCV()

        # Motor Hardware Config:
        pwm_pins = [32, 33]
        gpio_pins = [15, 7, 29, 31]
        _frequency_hz = 5000
        GPIO.setmode(GPIO.BOARD)

        # Motor Controller Setup:
        motor_left = JetsonMotor("motor_left", pwm_pins[0], gpio_pins[0], gpio_pins[1], _frequency_hz)
        motor_right = JetsonMotor("motor_right", pwm_pins[1], gpio_pins[2], gpio_pins[3], _frequency_hz)
        self.platform = DifferentialDrive(motor_left, motor_right)

        # Init Robot arm, gripper limits [q_open, q_close] must be adjusted to gripper hardware!
        self.arm = RoArmM1(gripper_limits=[50,60])

    def stop(self):
        print("TODO: Stop robot")
    
    
    