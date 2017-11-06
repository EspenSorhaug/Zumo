import random


class Behavior():

    def __init__(self, sensob, bbcon, priority = 0):
        self.bbcon = bbcon
        self.sensob = sensob
        self.motor_recommendations = [] # list with tuples
        self.active_flag = False
        self.halt_request = False
        self.priority = priority
        self.match_degree = 0
        self.weight = 0

    # A test to see if the behavior should be deactivated
    def consider_deactivation(self):
        pass

    # A test to see if the behavior should be activated
    def consider_activation(self):
        pass

    """
    Purpose: The main interface between the bbcon and the behavior.
    Actions: Update the activity status
             Call sense_and_act
             Update the behavior's weight
    """
    def update(self):
        pass


    """
    The core computations performed by the behavior that use sensob readings to produce motor recommendations
    Gathering the values of its sensobs (and possibly checking for relevant posts on the bbcon), and using this
    information to determine the motor recommendations, and possibly a halt request. Also setting the match_degree
    """
    def sense_and_act(self):
        pass


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
    
    
class Clean(Behavior):
    
    def __init__(self, sensob, bbcon): # sensob = ultrasonic sensor object
        super().__init__(sensob, bbcon)
        self.priority = 1

    def consider_activation(self):
        distance = self.sensob.get_value()
        if self.bbcon.is_taken_picture() and distance < 10:
            return True
        else:
            return False

    def consider_deactivation(self):
        distance = self.sensob.get_value()
        if distance > 10:
            return True
        else:
            return False

    def update(self):
        # Checking if the behavior should change to deactive or active, and changing the active_flag
        if self.active_flag:
            change = self.consider_deactivation()
            if change:
                self.active_flag = False

        else:
            change = self.consider_activation()
            if change:
                self.active_flag = True


        # Call sense_and_act and updating the weight IF this is an active behavior
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.match_degree * self.priority


    def sense_and_act(self):
        self.motor_recommendation = [['f', 0.5, 0.5]]
        self.match_degree = 1

