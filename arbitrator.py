from bbcon import BBCON

class Arbitrator():

    def choose_action(self): #Method that compares the wights of all active behaviors and returns the Motor_recommendations of the winning behavior and the corresponding motor recommendations

        winning_behavior = None

        for behavior in BBCON.get_active_behaviors():
            if winning_behavior == None:
                winning_behavior = behavior
            elif behavior.get_weight() > winning_behavior.get_weight():
                winning_behavior = behavior

        return winning_behavior.get_motor_recommendations()
