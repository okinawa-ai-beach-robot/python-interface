import os
from ..sensors.vrepcamerasim import VrepCameraSim
from ..manipulators.drive import DifferentialDrive
from ..manipulators.vrepmotorsim import VrepMotorSim
from ..manipulators.vreproarmm1sim import VrepRoArmM1Sim
from .robotinterface import RobotInterface
from ..config import config
from ..utils.vrepsimulation import vrep
from coppeliasim_zmqremoteapi_client import *

class VrepRobotSimV1(RobotInterface):
    def __init__(self, scene=None):
        super().__init__()

        # Simulation scenes are expected to be in ${BEACHBOT_HOME}/Simulation/xxx.ttt:
        self._base_folder_sim = str(config.BEACHBOT_HOME) + os.sep + "Simulation"


        # Simulator Setup:
        self._vrep_init(scene)

        # Camera Setup:
        self.cameradevices[RobotInterface.CAMERATYPE.FRONT] = VrepCameraSim(self._vrep_sim, "cam_front")
        try:
            self.cameradevices[RobotInterface.CAMERATYPE.GRIPPER] = VrepCameraSim(self._vrep_sim, "cam_gripper")
        except:
            pass

        # Motor Controller Setup:
        motor_left = VrepMotorSim("motor_left", self._vrep_sim)
        motor_right = VrepMotorSim("motor_right", self._vrep_sim)
        self.platform = DifferentialDrive(motor_left, motor_right)

        # Init Robot arm, gripper limits [q_open, q_close] must be adjusted to gripper hardware!
        self.arm = VrepRoArmM1Sim(self._vrep_sim, gripper_limits=[50,60])

    @vrep
    def _vrep_init(self, scene):
        # Open connection to simulator
        self._vrep_handle = RemoteAPIClient(verbose=False)
        self._vrep_sim = self._vrep_handle.require('sim')
        # Stop any running simulation before proceeding
        self._vrep_sim.stopSimulation(True)

        if scene is None:
            scene = "roarm_m1_locomotion_3finger.ttt"

        # Load and run simulation scene
        self._vrep_sim.loadScene(self._base_folder_sim+os.sep+scene)
        self._vrep_sim.startSimulation()

    def stop(self):
        print("TODO: Stop robot")
    
    
    