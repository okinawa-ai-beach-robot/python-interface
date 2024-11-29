
from typing import Tuple

class PIDController:
    def __init__(self, setpoint_x: float, setpoint_y: float, kp: float, ki: float=0, kd: float=0):
        
        # target position
        self.setpoint_x = setpoint_x
        self.setpoint_y = setpoint_y
        
        # Proportional factor for error correction
        self.kp = kp

        ## optional, default: set to 0 
        ## ki -> integration of error
        ## kd -> deriviative of error
        # self.ki = ki
        # self.kd = kd

        ## variables to calculate integral (sum of previous errors) and deriviative (difference to previous error)
        # self.integral_x = 0
        # self.integral_y = 0
        self.prev_error_x = 0
        self.prev_error_y = 0

    def get_output(self, x: float, y: float, debug:bool = False) -> Tuple[int, int]:
        error_x = self.setpoint_x - x
        error_y = self.setpoint_y - y

        if debug:
            print("PID error:", error_x, error_y)

        # Calculate proportional error signal:
        output_x = self.kp * error_x
        output_y = self.kp * error_y

        if debug:
            print("PID output:", output_x, output_y)


        ## Optional: Calculate integration error
        # self.integral_x += error_x
        # self.integral_y += error_y
        # output_x += self.ki * self.integral_x
        # output_y += self.ki * self.integral_y

        ## Optional calculate deriviative error
        # derivative_x = error_x - self.prev_error_x
        # derivative_y = error_y - self.prev_error_y
        # output_x += self.kd * derivative_x
        # output_y += self.kd * derivative_y


        self.prev_error_x = error_x
        self.prev_error_y = error_y

        # Truncate output to -100 to 100
        output_x = max(min(output_x, 100), -100)
        output_y = max(min(output_y, 100), -100)

        return int(output_x), int(output_y)
