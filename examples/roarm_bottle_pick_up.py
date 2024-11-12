import numpy as np
from beachbot.manipulators import RoArmM1
import time

# Load the .npz file
data = np.load("pickup_path.npz")

# Access the arrays by their keys
qs_grab = data["qs"]
taus_grab = data["taus"]
ts_grab = data["ts"].tolist()

data = np.load("toss_path.npz")

# Access the arrays by their keys
qs_toss = data["qs"]
taus_toss = data["taus"]
ts_toss = data["ts"].tolist()

arm1 = RoArmM1()
arm1.refresh_robot_state()
arm1.go_home()
arm1.replay_trajectory(qs_grab, ts_grab)
time.sleep(1)
# close gripper
arm1.set_gripper(0.8)
time.sleep(1)
arm1.replay_trajectory(qs_toss, ts_toss)
time.sleep(1)

# open gripper
arm1.set_gripper(0.0)
time.sleep(1)
arm1.go_home()
print("Done!")
