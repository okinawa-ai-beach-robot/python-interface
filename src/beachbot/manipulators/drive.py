import time
import math

from beachbot.config import logger

try:
    import Jetson.GPIO as GPIO
except (ModuleNotFoundError, RuntimeError) as ex:
    logger.warning(
        "Jetson GPIO library not installed or not available! Motor interface may not be available!"
    )

import threading


def sign(x):
    return (x > 0) - (x < 0)



def bounded(val, mi=0, ma=1):
    return min(ma, max(val, mi))


class Motor:
    def __init__(
        self,
        name: str,
        pwm_pin: int,
        in1: int,
        in2: int,
        frequency_hz: int,
        lo1: int = None,
        lo2: int = None,
    ) -> None:
        """
        Initializes the Motor class.

        :param name: Name of the motor. Numbering just as 1 or 2 is fine. Used for logs
        :param pwm_pin: GPIO pin connected to the PWM control.
        :param in1: GPIO pin connected to IN1 on the motor driver.
        :param in2: GPIO pin connected to IN2 on the motor driver.
        :param frequency_hz: PWM frequency in hertz.
        :param lo1: Optional GPIO pin for LO1 (error signal from motor driver), should be between 0 and 40.
        :param lo2: Optional GPIO pin for LO2 (error signal from motor driver), should be between 0 and 40.
        """
        self.name: str = name
        self.pwm_pin: int = pwm_pin
        self.in1: int = in1
        self.in2: int = in2
        self.frequency_hz: int = frequency_hz
        self.lo1: int = lo1
        self.lo2: int = lo2
        self.duty_cycle_percent: int = (
            0  # Initialized to 0, and int can hold -100 to 100 inclusively
        )
        GPIO.setup([in1, in2], GPIO.OUT, initial=GPIO.LOW)
        # set pin as an output pin with optional initial state of LOW
        GPIO.setup(self.pwm_pin, GPIO.OUT, initial=GPIO.LOW)

        if lo1 is not None:
            GPIO.setup(lo1, GPIO.IN)
        if lo2 is not None:
            GPIO.setup(lo2, GPIO.IN)

        # p1 is a PWM object.
        self.pwm = GPIO.PWM(self.pwm_pin, self.frequency_hz)
        self.pwm.start(self.duty_cycle_percent)

        # Start the thread to poll LO1 and LO2 if they are provided
        if lo1 is not None and lo2 is not None:
            self.polling_thread = threading.Thread(target=self.poll_lo_pins)
            self.polling_thread.daemon = True
            self.polling_thread.start()

    def poll_lo_pins(self) -> None:
        """
        Polls the LO1 and LO2 pins and prints their status based on the truth table.
        """
        # Thermal shutdown counter. If above 5, throw runtime error
        thermal_shutdown_counter = 0
        while True:
            lo1_value = GPIO.input(self.lo1)
            lo2_value = GPIO.input(self.lo2)

            if lo1_value == GPIO.LOW and lo2_value == GPIO.LOW:
                status = "Detected over thermal (TSD)"
                thermal_shutdown_counter += 1
                if thermal_shutdown_counter > 5:
                    # Stop motor and throw runtime error to stop execution
                    self.turn_off()
                    raise RuntimeError(f"[{self.name}] Detected over thermal (TSD)")
            else:
                thermal_shutdown_counter = 0
                if lo1_value == GPIO.HIGH and lo2_value == GPIO.HIGH:
                    status = "Motor{ Normal status (Normal operation)"
                elif lo1_value == GPIO.HIGH and lo2_value == GPIO.LOW:
                    status = "Detected motor load open (OPD)"
                elif lo1_value == GPIO.LOW and lo2_value == GPIO.HIGH:
                    status = "Detected over current (ISD)"
                else:
                    status = "Unknown status"

            print(f"[{self.name}] LO1: {lo1_value}, LO2: {lo2_value}, Status: {status}")
            time.sleep(0.1)

    def change_speed(self, speed: int) -> None:
        """
        Change the motor speed.

        Args:
            speed (int): Speed of the motor, ranging from -100 to 100.
                         Negative values represent reverse motion,
                         positive values represent forward motion,
                         and zero stops the motor.
        """
        if not -100 <= speed <= 100:
            raise ValueError(
                f"Speed must be between -100 and 100 inclusive. Received: {speed}"
            )

        self.duty_cycle_percent = abs(speed)

        if speed > 0:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
        elif speed < 0:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
        else:
            # Brake: INx1 = LOW, INx2 = LOW
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)

        self.pwm.ChangeDutyCycle(self.duty_cycle_percent)

    def turn_off(self) -> None:
        self.change_speed(0)
        self.pwm.stop()

    def cleanup(self):
        self.turn_off()


class DifferentialDrive(threading.Thread):
    def __init__(self, motor_left, motor_right, update_freq=100) -> None:
        # Init superclass thread
        super().__init__()
        # Do not block on exit (TODO)
        self.daemon = True

        self.motor_left = motor_left
        self.motor_right = motor_right
        self.update_freq = update_freq
        self._is_running = False
        self.motor_left = motor_left
        self.motor_right = motor_right
        self.update_freq = update_freq
        self._is_running = False

        self._target_angular_vel = 0
        self._target_velocity = 0
        self._current_angular_vel = 0
        self._current_velocity = 0
        self._target_angular_vel = 0
        self._target_velocity = 0
        self._current_angular_vel = 0
        self._current_velocity = 0

        self._max_rate_of_change = 100
        self._max_rate_of_change = 100

        self._motor_left_speed = 0
        self._motor_right_speed = 0
        self._motor_left_speed = 0
        self._motor_right_speed = 0

        self.motor_left.change_speed(self._motor_left_speed)
        self.motor_right.change_speed(self._motor_right_speed)

        super().start()

    def cleanup(self):
        self._is_running = False
        time.sleep(1.0 / self.update_freq)
        self._is_running = False
        time.sleep(1.0 / self.update_freq)

    def run(self):
        self._is_running = True
        while self._is_running:
            t_start = time.time()
            # do work....

            # Update current angular and linear velocity
            dir_delta = self._target_angular_vel - self._current_angular_vel
            vel_delta = self._target_velocity - self._current_velocity

            dir_dir = sign(dir_delta)
            vel_dir = sign(vel_delta)

            dir_dot = dir_dir * min(
                self._max_rate_of_change / self.update_freq, abs(dir_delta)
            )
            vel_dot = vel_dir * min(
                self._max_rate_of_change / self.update_freq, abs(vel_delta)
            )
            dir_dot = dir_dir * min(
                self._max_rate_of_change / self.update_freq, abs(dir_delta)
            )
            vel_dot = vel_dir * min(
                self._max_rate_of_change / self.update_freq, abs(vel_delta)
            )

            self._current_angular_vel = bounded(
                self._current_angular_vel + dir_dot, -100, 100
            )
            self._current_velocity = bounded(
                self._current_velocity + vel_dot, -100, 100
            )
            self._current_angular_vel = bounded(
                self._current_angular_vel + dir_dot, -100, 100
            )
            self._current_velocity = bounded(
                self._current_velocity + vel_dot, -100, 100
            )

            # Estimate motor velocity based on angluar and linear velocity and update motors if changed:
            __motor_left_speed = bounded(
                self._current_velocity + 0.5 * self._current_angular_vel, -100, 100
            )
            __motor_right_speed = bounded(
                self._current_velocity - 0.5 * self._current_angular_vel, -100, 100
            )
            __motor_left_speed = bounded(
                self._current_velocity + 0.5 * self._current_angular_vel, -100, 100
            )
            __motor_right_speed = bounded(
                self._current_velocity - 0.5 * self._current_angular_vel, -100, 100
            )

            # +/-15 percent no motion ...
            __motor_left_speed = bounded(
                sign(__motor_left_speed) * 15 + __motor_left_speed, -100, 100
            )
            __motor_right_speed = bounded(
                sign(__motor_right_speed) * 15 + __motor_right_speed, -100, 100
            )
            # +/-15 percent no motion ...
            __motor_left_speed = bounded(
                sign(__motor_left_speed) * 15 + __motor_left_speed, -100, 100
            )
            __motor_right_speed = bounded(
                sign(__motor_right_speed) * 15 + __motor_right_speed, -100, 100
            )

            if self._motor_left_speed != int(__motor_left_speed):
                self._motor_left_speed = int(__motor_left_speed)
                self.motor_left.change_speed(self._motor_left_speed)

            if self._motor_right_speed != int(__motor_right_speed):
                self._motor_right_speed = int(__motor_right_speed)
                self.motor_right.change_speed(self._motor_right_speed)

            t_end = time.time()
            t_wait = (1.0 / self.update_freq) - (t_end - t_start)
            if t_wait > 0:
            t_wait = (1.0 / self.update_freq) - (t_end - t_start)
            if t_wait > 0:
                time.sleep(t_wait)
        # Cleanup, end control loop, stop motors :)
        # Cleanup, end control loop, stop motors :)
        self.motor_left.change_speed(0)
        self.motor_right.change_speed(0)

    def set_target(self, angular_vel, velocity):
        self._target_angular_vel = angular_vel
        self._target_velocity = velocity


class PIDController:
    def __init__(
        self, kp: float, ki: float, kd: float, setpoint_x: float, setpoint_y: float
    ):
        self.kp = kp
        # self.ki = ki
        # self.kd = kd
        self.setpoint_x = setpoint_x
        self.setpoint_y = setpoint_y
        # self.prev_error_x = 0
        # self.prev_error_y = 0
        # self.integral_x = 0
        # self.integral_y = 0

    def get_output(self, x: float, y: float) -> Tuple[int, int]:
        error_x = self.setpoint_x - x
        error_y = self.setpoint_y - y

        # self.integral_x += error_x
        # self.integral_y += error_y

        # derivative_x = error_x - self.prev_error_x
        # derivative_y = error_y - self.prev_error_y

        output_x = (
            self.kp * error_x
        )  # + self.ki * self.integral_x + self.kd * derivative_x
        output_y = (
            self.kp * error_y
        )  # + self.ki * self.integral_y + self.kd * derivative_y

        # self.prev_error_x = error_x
        # self.prev_error_y = error_y

        # Truncate output to -100 to 100
        output_x = max(min(output_x, 100), -100)
        output_y = max(min(output_y, 100), -100)

        return int(output_x), int(output_y)
