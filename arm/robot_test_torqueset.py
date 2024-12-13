import time
import beachbot


# confiog is 180 75 10 0 ...
# 2. joint readings -15 ... 105...-15.... cyclic!

arm1 = beachbot.manipulators.RoArmM1(gripper_limits=[50,60])
arm1.go_home()
#arm1.set_gripper(0)

arm1.set_max_torque(1, 300)


#arm1.set_joints_enabled(False)

counter =0
try:
    while True:
        time.sleep(0.5)
        counter +=1
        print(arm1.get_joint_state())

except KeyboardInterrupt:
    print('Bye Bye!')

