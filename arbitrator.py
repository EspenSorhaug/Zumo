class Arbitrator():

    def choose_action(self,behavior1,behavior2): #Method that compares the wights of all active behaviors and returns the Motor_recommendations of the winning behavior and the corresponding motor recommendations

        winning_behavior = None
        
        if behavior1.get_weight() > 0:
            winning_behavior = behavior1
        if behavior2.get_weight() > behavior2.get_weight():
            winning_behavior = behavior2
        
        """
        for behavior in bbcon.get_active_behaviors():
            weight = behavior.get_match_degree()*behavior.get_priority()
            if weight > winning_behavior_weight:
                winning_behavior = behavior
                winning_behavior_weight = weight
        """
        
        if winning_behavior == None:
            print("Arbitrator did not find any recommended behavior")
            return False

        return (winning_behavior.get_motor_recommendations(),winning_behavior.is_halt())
