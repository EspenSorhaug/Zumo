from time import sleep
import random
import imager2 as IMR
from reflectance_sensors import ReflectanceSensors
from camera import Camera
from motors import Motors
from ultrasonic import Ultrasonic
from zumo_button import ZumoButton
from arbitrator import Arbitrator
from sensob import Sensob
from behavior import Take_photo
from behavior import AvoidBorders as Avoid_borders
from motob import Motob
from behavior import Walk_randomly
from arbitrator import Arbitrator


class BBCON:
    def __init__():
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motob = Motob()
        self.arbitrator = Arbitrator()
        
    def get_active_behaviors(self):
        return self.active_behaviors

    def add_behavior(self,behavior):
        self.behaviors.append(behavior)

    def add_sensob(self,sensob):
        self.sensobs.append(sensob)

    def activate_behavior(self,behavior):
        if behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self,behavior):
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    def run_one_timestep(self):
        for sensob in sensobs:
            sensob.update()
        motob.update()


def main():
    # initialisering
    bbcon = BBCON()

    ir_sensob = Sensob(ReflectanceSensors(True))  # True betyr med auto-kalibrering
    avoid_borders = Avoid_borders(ir_sensob, bbcon)
    walk_randomly = Walk_randomly(None, bbcon)

    # setup
    bbcon.add_sensob(ir_sensob)  # legger til IR sensob

    bbcon.add_behavior(avoid_borders)  # legger til avoid_borders
    bbcon.add_behavior(walk_randomly)  # legger til walk_randomly

    bbcon.activate_behavior(avoid_borders)
    bbcon.activate_behavior(walk_randomly)

    ZumoButton().wait_for_press()
    while True:
        bbcon.run_one_timestep()


if __name__ == '__main__':
    main()

