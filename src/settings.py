# this will house all of the key binds for the user

# boss key
# up key
# down key
# left key
# right key
# pause/resume key

class Settings():

    keyCodes = {
        
    }

    def __init__(self):

        self.__settings = {
            "boss_key":  98,
            "up_key":    65362,
            "down_key":  65364,
            "left_key":  65361,
            "right_key": 65363,
            "pause_key": 32
        }

    def getKey(self, key_name: str) -> int:
        return self.__settings[key_name]
    
    def setKey(self, key_name: str, value: int) -> None:
        self.__settings[key_name] =  value

    def getKeyValues(self) -> list:
        return [item for item in self.__settings.items()] 