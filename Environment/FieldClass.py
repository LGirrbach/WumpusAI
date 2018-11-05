class Field:
    def __init__(self):
        self.stench = False
        self.breeze = False
        self.glitter = False

        self.pit = False
        self.wumpus = False

    def get_sensor(self):
        return self.stench, self.breeze, self.glitter

    def assign_pit(self):
        self.pit = True
        self.breeze = True

    def has_pit(self):
        return self.pit

    def assign_wumpus(self):
        self.wumpus = True
        self.stench = True

    def kill_wumpus(self):
        self.wumpus = False

    def has_wumpus(self):
        return self.wumpus

    def assign_glitter(self):
        self.glitter = True

    def take_gold(self):
        self.glitter = False

    def has_glitter(self):
        return self.glitter

    def assign_breeze(self):
        self.breeze = True

    def assign_stench(self):
        self.stench = True