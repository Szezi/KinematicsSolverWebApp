from robot.fk_solver import FkSolver
from robot.ik_solver import IkSolver


class RoboticArm(FkSolver, IkSolver):
    def __int__(self, links: dict) -> None:
        FkSolver.__init__(self, links)
        IkSolver.__init__(self, links)

    def robotic_info_lengths(self):
        return self.link1, self.link2, self.link3, self.link4, self.link5

    def robotic_info_range(self):
        return [self.link1_min, self.link1_max], [self.link2_min, self.link2_max], [self.link3_min, self.link3_max], [self.link4_min, self.link4_max], [self.link5_min, self.link5_max]
