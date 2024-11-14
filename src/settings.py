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
            "boss_key":  0,
            "up_key":    0,
            "down_key":  0,
            "left_key":  0,
            "right_key": 0,
            "pause_key": 0
        }

    def getKey(self, key_name: str) -> int:
        return self.__settings[key_name]
    
    def setKey(self, key_name: str, value: int) -> None:
        self.__settings[key_name] =  value

    def getKeyValues(self) -> list:
        return [item for item in self.__settings.items] 