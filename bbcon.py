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
from motob import Motob
from time import sleep
from behavior import Take_photo
from behavior import AvoidBorders as Avoid_borders
from behavior import Walk_randomly
from arbitrator import Arbitrator
# test

class BBCON:
    def __init__(self):
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motob = []
        self.arbitrator = Arbitrator(self)
        
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

    def run_one_time_step(self):
        while True:
            for sensob in self.sensobs:
                sensob.update()
            for behavior in self.active_behaviors:
                behavior.update()
                print("%s weight: %s" %(behavior.get_name(),behavior.get_weight()))
            motor_recommendations = Arbitrator.choose_action()
            print("Recommendations: %s",(motor_recommendations))
            motob.update(motor_recommendations)
            sleep(0.5)
            #Halt_request

def main():
    # initialisering
    ZumoButton().wait_for_press()
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

    while True:
        bbcon.run_one_timestep()


if __name__ == '__main__':
    main()

