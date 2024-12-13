import time
import beachbot
from beachbot.robot.vreprobotsimv1 import VrepRobotSimV1


# confiog is 180 75 10 0 ...
# 2. joint readings -15 ... 105...-15.... cyclic!


arm1 = beachbot.manipulators.RoArmM1(gripper_limits=[50,60])
arm1.go_home()
arm1.set_max_torque(5, 0)

time.sleep(1.0)

robot = VrepRobotSimV1(scenefile="scene3_invkin.ttt") # scene3_invkin.ttt
simarm1 = robot.arm

arm1.go_home()
arm1.set_joints_enabled(True)

# time.sleep(2.0)
counter =0
try:
    while True:
        time.sleep(0.1)
        counter +=1
        # q,tau = arm1.get_joint_state()
        # print("q1:", q)
        # qsim = q[:5]
        # qsim[0]=-qsim[0]+180
        # qsim[1]=qsim[1]-30
        # simarm1.set_joint_targets(qsim)
        # print("qsim:", qsim)

        q,tau = simarm1.get_joint_state()
        qrobo = q[:5]
        qrobo[0]=-qrobo[0]+180
        qrobo[1]=-qrobo[1]+30
        qrobo[2]=-qrobo[2]
        qrobo[3]=-qrobo[3]
        qrobo[4]=50
        arm1.set_joint_targets(qrobo)
        print("qrobo:", qrobo)
        # print("ee")


        # q,tau = simarm1.get_joint_state()
        # qsim = q[:5]
        # qsim[0]=-qsim[0]+180

        if counter ==10:
            print("Current joint angles:\t", q)
            print("Current tourques:\t", tau)
            counter = 0
except KeyboardInterrupt:
    print('Bye Bye!')

