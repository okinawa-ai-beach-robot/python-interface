from beachbot.manipulators import RoArmM1
import time
import numpy as np

arm1 = RoArmM1(gripper_limits=[50,60])
arm1.set_joints_enabled(True)
arm1.refresh_robot_state()
arm1.go_home()

data = np.load("test_path.npz")

qs = data['qs']
taus = data['taus']
ts = data['ts']

print("tsteps*", ts)

print("Recoding entries:", qs.shape[0])
print("Recoding duration:", ts[-1])
# qs: joint angles
# taus: torques
# ts: timestamps
print("\n\nStart replay (replay based on record time stamps)...")
print("recording")
arm1.replay_trajectory(qs, ts)
print("Done!")

