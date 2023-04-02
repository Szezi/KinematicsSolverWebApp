from api.robotic_arm import RoboticArm


def calculate_ik(links, x, y, z, alpha):
    Robot_IK = RoboticArm(links)
    Robot_IK.ik_solver(x, y, z, alpha)
    config_1 = Robot_IK.ik_get_config1()
    config_2 = Robot_IK.ik_get_config2()
    return config_1, config_2


def calculate_fk(links, theta1, theta2, theta3, theta4):
    Robot_FK = RoboticArm(links)
    result_xyz = Robot_FK.fk_solve_auto(theta1, theta2, theta3, theta4)
    dh_table = Robot_FK.fk_dh(theta1, theta2, theta3, theta4)
    print(result_xyz, dh_table)
    return result_xyz, dh_table
