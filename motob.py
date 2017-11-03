from motors import Motors


class Motob:
    """
    The motor object (motob) manifests an interface between a behavior and one or more motors (a.k.a. actuators).
    It contains (at least) the following instance variables:
    1. motors - a list of the motors whose settings will be determined by the motob.
    2. value - a holder of the most recent motor recommendation sent to the motob.
    Its primary methods are:
    1. update - receive a new motor recommendation, load it into the value slot, and operationalize it.
    2. operationalize - convert a motor recommendation into one or more motor settings, which are sent to
    the corresponding motor(s)
    """
    def __init__(self):
        self.motor = Motors()
        self.value = None

    def update(self, recommendation):
        self.value = recommendation
        self.operationalize()

    def operationalize(self):
        """
        convert motor recommendation into motor setting
        send to motor
        format value: [direction, speed, duration]
        :return:
        """
        for element in self.value:
            if element[0] == "f":
                self.motor.forward(element[1], element[2])
            elif element[0] == "b":
                self.motor.backward(element[1], element[2])
            elif element[0] == "l":
                self.motor.left(element[1], element[2])
            elif element[0] == "r":
                self.motor.right(element[1], element[2])
