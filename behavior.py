import random
import imager2 as IMR


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
        self.name = "No-name"

    # A test to see if the behavior should be deactivated
    def consider_deactivation(self):
        pass

    def get_name(self):
        return self.name

    # A test to see if the behavior should be activated
    def consider_activation(self):
        pass

    def get_motor_recommendations(self):
        return self.motor_recommendations

    """
    Purpose: The main interface between the bbcon and the behavior.
    Actions: Update the activity status
             Call sense_and_act
             Update the behavior's weight
    """
    def update(self):
        pass

    #Getter for the behhavior's weight
    def get_weight(self):
        return self.weight
    

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
        self.weight = 0.1
        self.name = "Walk randomly"

    def consider_deactivation(self):
        return False

    def get_name(self):
        return self.name

    def consider_activation(self):
        return True

    def update(self):
        self.sense_and_act()

    def sense_and_act(self):

        directions = ['l','r','f','f']
        direct_int = random.randint(0,3)
        direction = directions[direct_int]
        duration = 0.1
        speed = 0.3

        if direction == 'l' or direction == 'r':
            duration = 0.2
        self.motor_recommendations = [[direction,speed,duration]]
        

        
class Avoid_borders(Behavior):
    def __init__(self, sensob, bbcon):
        Behavior.__init__(self, sensob, bbcon)
        self.priority = 1
        self.name = "Avoid borders"
    
    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return True

    def get_name(self):
        return self.name

    def update(self):
        """
        Purpose: The main interface between the bbcon and the behavior.
        Actions: Update the activity status
                 Call sense_and_act
                 Update the behavior's weight
        :return:
        """
        # sjekker om active_flag stemmer
        if self.active_flag:
            if self.consider_deactivation():
                self.active_flag = False
        else:
            if self.consider_activation():
                self.active_flag = True

        # dersom avoid_borders er blant de aktive behaviours
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.priority * self.match_degree


    def sense_and_act(self):
        """
        The core computations performed by the behavior that use sensob readings to produce motor recommendations
        Gathering the values of its sensobs (and possibly checking for relevant posts on the bbcon), and using this
        information to determine the motor recommendations, and possibly a halt request. Also setting the match_degree
        :return:
        """
        # henter ut verdier fra sensob, liste med 6 tall
        # Function should return a list of 6 reals between 0 and 1.0 indicating
        # the amount of reflectance picked up by each one.  A high reflectance (near 1) indicates a LIGHT surface, while
        # a value near 0 indicates a DARK surface.
        sensob_values = self.sensob.get_value()
        values_sum = sum(sensob_values)

        # dersom sum av de 6 verdiene er under 3, økes matchdegree


        border_found = []
        for i in range(sensob_values.__len__()):
            if sensob_values[i] < .7:
                border_found.append(i)

        if border_found.__contains__(0) or border_found.__contains__(1) and not border_found.__contains__([4,5]):
            self.motor_recommendations = [["b", .5, .4], ["r", .5, .6]]
            self.bbcon.picture_taken = False
            self.bbcon.reset = True
            self.match_degree = 1
        elif border_found.__contains__(4) or border_found.__contains__(5) and not border_found.__contains__([0,1]):
            self.motor_recommendations = [["b", .5, .4], ["l", .5, .6]]
            self.bbcon.picture_taken = False
            self.bbcon.reset = True
            self.match_degree = 1
        #else:
        #    # anbefaler å rygge, og svinge mot venstre dersom møter kant
        #    self.motor_recommendations = [["b", .5, .4], ["l", .5, .9]]

        elif values_sum < 2:
            self.match_degree = 1
            self.bbcon.picture_taken = False
            self.bbcon.reset = True
            self.motor_recommendations = [["b", .5, .4], ["l", .5, .9]]
        else:
            self.match_degree = 0
            self.motor_recommendations = [["b", .5, .4], ["l", .5, .9]]


    
class Clean(Behavior):
    
    def __init__(self, sensob, bbcon): # sensob = ultrasonic sensor object
        super().__init__(sensob, bbcon)
        self.priority = 0.8
        self.motor_recommendations = [['f', 0.5, 0.1]]

    def consider_activation(self):
        distance = self.sensob.get_value()
        if self.bbcon.is_picture_taken():
            return True
        else:
            return False

    def consider_deactivation(self):
        distance = self.sensob.get_value()
        if not self.bbcon.picture_taken and distance >10:
            return True
        else:
            return False

    def update(self):
        # Checking if the behavior should change to deactive or active, and changing the active_flag
        if self.active_flag:
            change = self.consider_deactivation()
            if change:
                self.active_flag = False
                self.match_degree = 0

        else:
            change = self.consider_activation()
            if change:
                self.active_flag = True
                self.match_degree = 1


        # Call sense_and_act and updating the weight IF this is an active behavior
        if self.active_flag:
            self.sense_and_act()
        self.weight = self.match_degree * self.priority


    def sense_and_act(self):
        self.motor_recommendation = [['f', 0.5, 0.1]]
        self.match_degree = 1
        

        
class Take_photo(Behavior):

    def __init__(self,sensob,bbcon):
        Behavior.__init__(self,sensob,bbcon)
        self.priority = 0.6
        self.match_degree = 1
        self.motor_recommendations = [["f",0,0.1]]
        self.photo_count = 0
        self.name = "Photograph"


    def consider_deactivation(self):
        if self.bbcon.picture_taken:
            self.sensob.reset()
            return True
        return False


    def consider_activation(self):
            if not self.bbcon.picture_taken and self.sensob.get_value()[1]<=10:
                self.match_degree = 1
                return True
            return False

    def set_active(self):
        self.active_flag = True

    def update(self):
        # Updates camera and saves image if mode is not stand by
        #Resets camera right away
        if self.consider_deactivation():
                self.active_flag = False
                self.bbcon.deactivate_behavior(self)
        elif self.consider_activation():
                self.set_active()
                self.bbcon.activate_behavior(self)

        if self.active_flag:
            self.sensob.update()
            self.sense_and_act()
            self.weight = self.priority * self.match_degree


    def sense_and_act(self):
        #When zumo is within 10cm of an object take_photo should have greater weight
        if not self.bbcon.picture_taken and self.active_flag:
            im = IMR.Imager(image=self.sensob.get_value()[0])
            print("TAKING PHOTO")
            im.dump_image('garbage'+str(self.photo_count)+'.jpeg')
            self.photo_count += 1
            self.bbcon.picture_taken = True
            self.motor_recommendations = [["f",0,0.1]]
            self.match_degree = 0




class Approach(Behavior):

    def __init__(self,sensob,bbcon):
        self.name = "Approach"
        Behavior.__init__(self,sensob,bbcon)
        self.priority = 0.5

    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return True

    """
    Purpose: The main interface between the bbcon and the behavior.
    Actions: Update the activity status
             Call sense_and_act
             Update the behavior's weight
    :return:
    """
    def update(self):
        # sjekker om active_flag stemmer
        if self.active_flag:
            if self.consider_deactivation():
                self.active_flag = False
        else:
            if self.consider_activation():
                self.active_flag = True

        #dersom approach er blant active behaviors
        if self.active_flag:
            self.sense_and_act()
            self.weight = self.priority * self.match_degree


    def sense_and_act(self):

        sensob_value = self.sensob.get_value()
        threshold = 20


        #When zumo is within 10cm of an object take_photo should have greater weight
        if sensob_value <= 10:
            self.match_degree = 0
            self.motor_recommendations = [["f",0,0.1]]
        #Sjekker om et objekt er mindre enn 20cm fra roboten,
        #deretter oker match_degree
        elif sensob_value < threshold:
            self.match_degree = sensob_value/threshold
            self.motor_recommendations = [["f", .3, .1]]
        else:
            self.match_degree = 0
