class Sensob:

    def __init__(self,sensor):
        self.sensor = sensor # får sensor ved __init__() i BBCON
        self.value = None # Verdien hentes fra update()

    def update(self):
        # hent og endre rådata fra sensor
        self.sensor.update() # TODO: Her eller i BBCON?
        self.value = self.sensor.get_value() # TODO: Hvordan ønsker vi verdier representert?

    def get_value(self): return self.value

    def reset(self): self.value = None
