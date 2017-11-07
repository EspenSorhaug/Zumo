class Arbitrator:
    def __init__(self,bbcon):
        self.bbcon = bbcon

    #  Method for choosing recommended behavior
    def choose_action(self):
        winning_behavior = None

        for behavior in self.bbcon.get_active_behaviors():
            if winning_behavior == None:
                winning_behavior = behavior
            elif behavior.get_weight() > winning_behavior.get_weight():
                winning_behavior = behavior

        return winning_behavior.get_motor_recommendations()
