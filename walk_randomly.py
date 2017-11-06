from behavior import Behavior
import random

class Walk_randomly(Behavior):

    def __init__(self,sensob,bbcon):
        Behavior.__init__(self,sensob,bbcon)

    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return True

    def update(self):
        self.sense_and_act()

    def sense_and_act(self):

        directions = ['f','r','f','f']
        direct_int = random.randint(0,3)
        direction = directions[direct_int]
        duration = 0.1
        speed = 0.4

        self.motor_recommendations = [[direction,speed,duration]]


