from api.robotic_arm import RoboticArm


def calculate_ik(links: dict, x: int, y: int, z: int, alpha: int):
    """
    Calculate forward kinematics of robotic arm.
    :param links: dictionary of robotic links param
    :param x: x values
    :param y: y value
    :param z: z value
    :param alpha: alpha value
    :return: config1, config2
    """
    Robot_IK = RoboticArm(links)
    Robot_IK.ik_solver(x, y, z, alpha)
    config_1 = Robot_IK.ik_get_config1()
    config_2 = Robot_IK.ik_get_config2()
    return config_1, config_2


def calculate_fk(links: dict, theta1: float, theta2: float, theta3: float, theta4: float):
    """
        Calculate forward kinematics of robotic arm.
        :param links: dictionary of robotic links param
        :param theta1: theta1 value
        :param theta2: theta2 value
        :param theta3: theta3 value
        :param theta4: theta4 value
        :return: result_xyz, dh_table
        """
    Robot_FK = RoboticArm(links)
    result_xyz = Robot_FK.fk_solve_auto(theta1, theta2, theta3, theta4)
    dh_table = Robot_FK.fk_dh(theta1, theta2, theta3, theta4)
    print(result_xyz, dh_table)
    return result_xyz, dh_table
