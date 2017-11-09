class Sensob:

    def __init__(self,sensor,sensor2=None):
        self.sensor = sensor # får sensor ved __init__() i BBCON
        self.sensor2 = sensor2
        self.value = None # Verdien hentes fra update()

    def update(self):
        # hent og endre rådata fra sensor
        self.sensor.update()
        if self.sensor2 is not None:
            self.sensor2.update()
        self.value = self.sensor.get_value() # TODO: Hvordan ønsker vi verdier representert?

    def get_value(self):
        if self.sensor2 is not None:
            return [self.sensor.get_value(),self.sensor2.get_value()]
        return self.sensor.get_value()

    def reset(self): self.value = None
