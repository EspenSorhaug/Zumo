class Arbitrator():

    def choose_action(self,behavior1,behavior2): #Method that compares the wights of all active behaviors and returns the Motor_recommendations of the winning behavior and the corresponding motor recommendations

        winning_behavior = None
        winning_behavior_weight = 0

        for behavior in bbcon.get_active_behaviors():
            weight = behavior.get_match_degree()*behavior.get_priority()
            if weight > winning_behavior_weight:
                winning_behavior = behavior
                winning_behavior_weight = weight
        
        if winning_behavior is None:
            print("Arbitrator did not find any recommended behavior")
            # Dont move
            return [['f', 0, 0]]

        return winning_behavior.get_motor_recommendations()
