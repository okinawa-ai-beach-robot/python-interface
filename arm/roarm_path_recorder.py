from beachbot.manipulators import RoArmM1
import time

arm1 = RoArmM1(gripper_limits=[50,60])
arm1.refresh_robot_state()
arm1.go_home()
print("Recording...")
qs, taus, ts = arm1.record_trajectory(wait_time_max=10, save_path="./test_path")
print("Recoding entries:", qs.shape[0])
print("Recoding duration:", ts[-1])
# qs: joint angles
# taus: torques
# ts: timestamps
print("\n\nStart replay (replay based on record time stamps)...")
input("Press Enter to continue...")
arm1.replay_trajectory(qs, ts)
print("Done!")
