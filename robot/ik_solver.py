""" Module allows inverse kinematics to be calculated"""

import math


class IkSolver:
    """ Class allows to calculate inverse kinematics of the robotic arm with given parameters and specified length of robotic arm links.\n
    Inverse kinematics is being calculated using geometrical method.\n """

    def __init__(self, links: dict) -> None:
        """
        Initials parameters and dimensions of robotic arm. \n
        Example: link1:[length, min range, max range] \n
        links = {"link1": [118, -80, 80],\n
         "link2": [150, 5, 175],\n
         "link3": [150, - 115, 55],\n
         "link4": [54, -85, 85],\n
         "link5": [0, 0, 0]}\n
        If 3link robotic arm put 0 in link3 \n
        if 4 link robotic arm no empty links \n
         :param links: dictionary
        """
        # Dictionary
        self.links = links

        # Lengths of links
        self.link1 = links["link1"][0]
        self.link2 = links["link2"][0]
        self.link3 = links["link3"][0]
        self.link4 = links["link4"][0]
        self.link5 = links["link5"][0]

        # Range of links
        self.link1_min = links["link1"][1]
        self.link1_max = links["link1"][2]
        self.link2_min = links["link2"][1]
        self.link2_max = links["link2"][2]
        self.link3_min = links["link3"][1]
        self.link3_max = links["link3"][2]
        self.link4_min = links["link4"][1]
        self.link4_max = links["link4"][2]
        self.link5_min = links["link5"][1]
        self.link5_max = links["link5"][2]

        # Variables to find
        self.theta33 = None  # config 2
        self.theta22 = None  # config 2
        self.theta11 = None  # config 2
        self.theta3 = None  # config 1
        self.theta2 = None  # config 1
        self.theta1 = None  # config 1
        self.theta0 = None  # config 1 and 2

        IkSolver.ik_check_input_param(self)

    def ik_check_input_param(self):
        if not isinstance(self.link1, int) or not isinstance(self.link2, int) or not isinstance(
                self.link3, int) or not isinstance(
                self.link4, int) or not isinstance(self.link5, int):
            status = "Links dimensions must be integers"
            print(status)
            self.link1 = None
            self.link2 = None
            self.link3 = None
            self.link4 = None
            self.link5 = None
        else:
            if self.link1 < 0 or self.link2 < 0 or self.link3 < 0 or self.link4 < 0 or \
                    self.link5 < 0:
                status = "Links dimensions must be equal or greater then 0"
                print(status)
                self.link1 = None
                self.link2 = None
                self.link3 = None
                self.link4 = None
                self.link5 = None
            else:
                status = "Links dimensions ok"
                print(status)
                pass

    def ik_solver(self, px: int, py: int, pz: int, alfa: int):
        l0 = self.link1  # base height
        l1 = self.link2  # 1st links length
        l2 = self.link3  # 2nd links length
        l3 = self.link4  # "L" effector dimension
        l4 = self.link5  # "H" effector dimension

        alfa = math.radians(alfa)

        try:
            # XY plane - determination of theta0 and R
            if px != 0 and py != 0:
                theta0 = math.atan(py / px)
            elif px != 0 and py == 0:
                theta0 = math.radians(0)
            elif px == 0 and py > 0:
                theta0 = math.radians(90)
            elif px == 0 and py < 0:
                theta0 = math.radians(-90)
            elif px == 0 and py == 0:
                theta0 = math.radians(0)
            else:
                raise ValueError('Unexpected angel theta0')

            # Position Z,Y raised to power of 2
            px2 = px ** 2
            py2 = py ** 2
            # Calculate vector_r
            vector_r = math.sqrt(px2 + py2)
            # _____________________________________________________________________________________________________________
            # Effector ZR plane
            c = math.sqrt(l3 ** 2 + l4 ** 2)
            beta = math.atan(l4 / l3)
            z_effector = c * math.sin(alfa - beta)
            r_effector = c * math.cos(alfa - beta)

            # Designation of the Z, R end of the second link
            # Subtract the effector Z, R from the ZR of the system and reduce by the base height
            z_2nd_link = pz - l0 - z_effector
            r_2nd_link = vector_r - r_effector

            # ____________________________________________________________________________________________________________

            # ZR plane - determination of theta1 and theta2

            delta = r_2nd_link ** 2 + z_2nd_link ** 2

            if l2 != 0:
                temp_l = (delta - l1 ** 2 - l2 ** 2) / (2 * l1 * l2)
                theta2 = math.acos(temp_l)
                theta22 = (-1 * (math.acos(temp_l)))
            else:
                theta2 = 0
                theta22 = 0

            gamma1 = math.acos((delta + l1 ** 2 - l2 ** 2) / (2 * math.sqrt(delta) * l1))
            gamma2 = -1 * (math.acos((delta + l1 ** 2 - l2 ** 2) / (2 * math.sqrt(delta) * l1)))

            if r_2nd_link == 0:  # The point is on the Z axis of the system
                theta1 = math.radians(90) - gamma1
                theta11 = math.radians(90) - gamma2
            else:
                z_divide_r = z_2nd_link / r_2nd_link
                if z_divide_r >= 0:  # The point is located in the 1st quarter of the ZR coordinate system
                    theta1 = math.atan(z_2nd_link / r_2nd_link) - gamma1
                    theta11 = math.atan(z_2nd_link / r_2nd_link) - gamma2
                elif z_divide_r < 0:  # # the point is located in the 2nd quarter of the ZR coordinate system
                    theta1 = (math.radians(180) + math.atan(z_2nd_link / r_2nd_link)) - gamma1
                    theta11 = (math.radians(180) + math.atan(z_2nd_link / r_2nd_link)) - gamma2
                else:
                    raise ValueError('Unexpected angel theta1/theta11')

            # Determination of the angle of inclination of the 2nd link in relation to the ground plane
            z1 = l1 * math.sin(theta1)  # height in Z axis of joint R1, R2
            z11 = l1 * math.sin(theta11)

            if l2 != 0:
                beta = math.asin(
                    (z_2nd_link - z1) / l2)  # Angle of inclination of the 2nd link in relation to the ground plane
                beta2 = math.asin((z_2nd_link - z11) / l2)
            else:
                beta = theta1
                beta2 = theta11

            # Calculation of theta3
            theta3 = alfa - beta
            theta33 = alfa - beta2

            # Convert from radians to degrees
            self.theta0 = math.degrees(theta0)
            self.theta1 = math.degrees(theta1)
            self.theta2 = math.degrees(theta2)
            self.theta3 = math.degrees(theta3)
            self.theta11 = math.degrees(theta11)
            self.theta22 = math.degrees(theta22)
            self.theta33 = math.degrees(theta33)

            print(theta0)
            status = 'Calculations ended successfully'
            return status

        except ValueError:
            status = 'Error: Something went wrong'
            return status

        except:
            status = 'Error: The entered data is incorrect'
            return status

        finally:
            print('Inverse kinematics calculations ended')

    def ik_get_config1(self):
        if -80 <= self.theta0 <= 80 and 5 <= self.theta1 <= 175 and -115 <= self.theta2 <= 55 and -85 <= self.theta3 <= 85:
            status_config_1 = "Config_1: Success"
            config_1 = [round(self.theta0, 2), round(self.theta1, 2), round(self.theta2, 2), round(self.theta3, 2)]

        else:
            config_1 = [0.0, 0.0, 0.0, 0.0]
            status_config_1 = "Warning: Config_1: No results"

        return config_1, status_config_1

    def ik_get_config2(self):
        if -80 <= self.theta0 <= 80 and 5 <= self.theta11 <= 175 and -115 <= self.theta22 <= 55 and -85 <= self.theta33 <= 85:
            status_config_2 = "Config_2: Success"
            config_2 = [round(self.theta0, 2), round(self.theta11, 2), round(self.theta22, 2), round(self.theta33, 2)]

        else:
            status_config_2 = "Warning: Config_2: No results"
            config_2 = [0.0, 0.0, 0.0, 0.0]

        return config_2, status_config_2
