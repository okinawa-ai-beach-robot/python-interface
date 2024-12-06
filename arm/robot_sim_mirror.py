import time
import beachbot
from beachbot.robot.vreprobotsimv1 import VrepRobotSimV1


# confiog is 180 75 10 0 ...
# 2. joint readings -15 ... 105...-15.... cyclic!

arm1 = beachbot.manipulators.RoArmM1()

robot = VrepRobotSimV1()
simarm1 = robot.arm


arm1.set_joints_enabled(False)

counter =0
try:
    while True:
        time.sleep(0.1)
        counter +=1
        q,tau = arm1.get_joint_state()
        qsim = q[:5]
        qsim[0]=-qsim[0]+180
        qsim[1]=qsim[1]-30
        simarm1.set_joint_targets(qsim)

        if counter ==10:
            print("Current joint angles:\t", q)
            print("Current tourques:\t", tau)
            counter = 0
except KeyboardInterrupt:
    print('Bye Bye!')

