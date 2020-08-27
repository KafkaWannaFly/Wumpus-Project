class Killer(object):
    def __init__(self, sprite, init_position, indication_letter):
        self.sprite = sprite
        self.position = init_position
        self.indication = indication_letter
        self.is_killable: bool = True
