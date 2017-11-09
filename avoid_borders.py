class Behavior():

    def __init__(self, sensob, bbcon):
        self.bbcon = bbcon
        self.sensob = sensob
        self.motor_recommendations = [] # list with tuples
        self.active_flag = True
        self.halt_request = False
        self.priority = 0
        self.match_degree = 0
        self.weight = 0

    # A test to see if the behavior should be deactivated
    def consider_deactivation(self):
        return False

    # A test to see if the behavior should be activated
    def consider_activation(self):
        return True

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


class AvoidBorders(Behavior):
    def __init__(self, sensob, bbcon):
        Behavior.__init__(self, sensob, bbcon)
        self.priority = 1

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
            self.sensob.update()
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
        print("sensob_values: ", sensob_values)
        values_sum = sum(sensob_values)

        # dersom sum av de 6 verdiene er under 3, økes matchdegree
        print("Sens_val: ",values_sum)
        if values_sum < 2:
            self.match_degree = 1
        else:
            self.match_degree = 0

        # anbefaler å rygge, og svinge mot venstre dersom møter kant
        self.motor_recommendations = [["b", .5, .2], ["l", .5, .1]]
        print()

"""
Sensob har
    sensor, value

    update()
    getValue()
    reset()
"""
