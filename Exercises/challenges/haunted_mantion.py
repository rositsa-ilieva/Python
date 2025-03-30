class HauntedMansion:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, attr_name):
        return "Booooo, only ghosts here!"

    def __setattr__(self, key, value):
        spooky_key = "spooky_" + key
        return object.__setattr__(self, spooky_key, value)
