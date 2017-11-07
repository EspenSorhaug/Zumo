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
# test

def Class BBCON:
    def __init__():
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motobs = []
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


