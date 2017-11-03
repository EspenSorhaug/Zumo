import imager2 as IMR

class Behavior():

    def __init__(self, sensob, bbcon):
        self.bbcon = bbcon
        self.sensob = sensob
        self.motor_recommendations = [] # list with tuples
        self.active_flag = False
        self.halt_request = False
        self.priority = 0
        self.match_degree = 0
        self.weight = 0

    # A test to see if the behavior should be deactivated
    def consider_deactivation(self):
        return False

    # A test to see if the behavior should be activated
    def consider_activation(self):
        return False

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


class Take_photo(Behavior):


    def __init__(self,sensob,bbcon):
        Behavior.__init__(self,sensob,bbcon)
        self.priority = 1
        self.motor_recommendations = None
        self.photo_count = 0


    def consider_deactivation(self):
        if self.sensob.get_value() != None:
            self.sensob.reset()
            return True
        return False


    def consider_activation(self):
        return False # TODO: bbcon set active

    def set_active(self):
        self.active_flag = True

    def update(self):
        if self.active_flag == True:

            # Updates camera and saves image
            self.sensob.update()
            self.sense_and_act()
            #Resets camera right away
            if self.consider_deactivation():
                self.active_flag = False
        else:
            if self.consider_activation():
                self.active_flag = True
        self.weight = self.priority * self.match_degree


    def sense_and_act(self):
        if self.active_flag:
            im = IMR.Imager(image=self.sensob.get_value())
            im.dump_image('garbage'+str(self.photo_count)+'.jpeg')
            self.photo_count += 1
            self.match_degree = 0
        else:
            self.match_degree = 1
