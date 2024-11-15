import beachbot
import math

epsilon = 1e-5

arm = beachbot.manipulators.RoArmM1(serial_port=None)


qs_poses = []

qs_poses.append(
    [
        (arm.LEN_B + arm.LEN_C + arm.LEN_D + arm.LEN_E),
        arm.LEN_H,
        arm.LEN_A - arm.LEN_F,
        180,
    ]
)
qs_poses.append(
    [
        (arm.LEN_B + arm.LEN_C + arm.LEN_D + arm.LEN_E) / 2,
        arm.LEN_H,
        arm.LEN_A - arm.LEN_F,
        180,
    ]
)
qs_poses.append(
    [
        (arm.LEN_B + arm.LEN_C + arm.LEN_D + arm.LEN_E) / 2,
        arm.LEN_H,
        arm.LEN_A - arm.LEN_F + 50,
        150,
    ]
)
qs_poses.append(
    [
        (arm.LEN_B + arm.LEN_C + arm.LEN_D + arm.LEN_E) / 2,
        arm.LEN_H,
        arm.LEN_A - arm.LEN_F,
        170,
    ]
)

for pos in qs_poses:
    print("Testing pose", pos)
    qs_estimate = arm.inv_kin(pos[:3], pos[3])
    pos_estimate = arm.fkin(qs_estimate)

    print("Position estimate is", pos_estimate)
    print("qs estimate is:", qs_estimate)
    for a, b in zip(pos[0:3], pos_estimate):
        if math.fabs(a - b) > epsilon:
            raise Exception("ikin and fkin exceed error threshold!")
    print("--- NEXT ---")

print("All ok :)")
