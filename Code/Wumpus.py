from Code.Killer import *


class Wumpus(Killer):
    def __init__(self, sprite, init_position, indication_letter):
        Killer.__init__(self, sprite, init_position, indication_letter)
        self.is_killable = True
