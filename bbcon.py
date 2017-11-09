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
from behavior import *
from arbitrator import Arbitrator
# test

class BBCON:
    def __init__(self):
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motob = Motob()
        self.arbitrator = Arbitrator(self)
        self.picture_taken = False
        
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
            
    def is_picture_taken(self):
        return self.picture_taken

    def run_one_timestep(self):
        print("RUN ONE TIME STEP")
        for sensob in self.sensobs:
            sensob.update()
        print("SENSOBS FINISHED")
        for behavior in self.behaviors:
            behavior.update()
        print("BEHAVIOUR FINISHED")
            #print("%s weight: %s" %(behavior.get_name(),behavior.get_weight()))
        motor_recommendations = self.arbitrator.choose_action()
        #print("Recommendations: %s",(motor_recommendations))
        self.motob.update(motor_recommendations)
        #sleep(0.5)
        #Halt_request

def main():
    # initialisering
    ZumoButton().wait_for_press()
    bbcon = BBCON()
    us = Ultrasonic()

    ir_sensob = Sensob(ReflectanceSensors(True))  # True betyr med auto-kalibrering
    usonic_sensob = Sensob(us)
    camera_sensob = Sensob(sensor=Camera(), sensor2=us)

    avoid_borders = Avoid_borders(ir_sensob, bbcon)
    walk_randomly = Walk_randomly(None, bbcon)
    clean = Clean(usonic_sensob,bbcon)
    approach = Approach(usonic_sensob,bbcon)
    take_photo = Take_photo(camera_sensob,bbcon)

    # setup
    bbcon.add_sensob(ir_sensob)        # legger til IR sensob
    bbcon.add_sensob(usonic_sensob)    # legger til Ultrasonic sensob
    #bbcon.add_sensob(camera_sensob)    # legger til Ultrasonic/camera sensob

    bbcon.add_behavior(avoid_borders)  # legger til avoid_borders
    bbcon.add_behavior(walk_randomly)  # legger til walk_randomly
    #bbcon.add_behavior(clean)          # legger til clean
    bbcon.add_behavior(approach)       # legger til approach
    bbcon.add_behavior(take_photo)     # legger til take_photo

    bbcon.activate_behavior(avoid_borders)
    bbcon.activate_behavior(walk_randomly)
    bbcon.activate_behavior(approach)
    #bbcon.activate_behavior(take_photo)

    while True:
        bbcon.run_one_timestep()


if __name__ == '__main__':
    main()

