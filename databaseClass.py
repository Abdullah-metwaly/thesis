
class Interface:
    """A sample Interface class"""

    def __init__(self, ifInoctets, ifOutoctets, speed):
        self.ifInoctets = ifInoctets
        self.ifOutoctets = ifOutoctets
        self.speed = speed


    def __repr__(self):
        return "Interface('{}', '{}', {})".format(self.ifName, self.ifInoctets, self.ifOutoctets, self.speed)
