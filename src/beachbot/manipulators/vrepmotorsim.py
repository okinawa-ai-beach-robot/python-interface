class VrepMotorSim():
    def __init__(self, vrep_sim, motor_name, max_velocity=10):
        self.vrep_sim = vrep_sim
        self._motor_name = motor_name
        self._max_velocity=max_velocity
        self._motor_id = self.vrep_sim.getObject("/"+motor_name)
        
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
        print("set speed:", self._motor_id,self._motor_name, self._max_velocity * speed / 100 )
        self.vrep_sim.setJointTargetVelocity(self._motor_id, self._max_velocity * speed / 100)
        