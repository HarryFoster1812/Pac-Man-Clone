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
            "boss_key":  [98, 'b'],
            "up_key":    [65362, 'Up'],
            "left_key":  [65361, 'Left'],
            "right_key": [65363, 'Right'],
            "down_key":  [65364, 'Down'],
            "pause_key": [32, 'Space']
        }
        self.cheat_keys = [108, # add a life      'l'
                           109, # reset ghosts    'm'
                           103, # release ghosts  'g'
                           104  # speed up pacman 'h'
                           ]

    def getKey(self, key_name: str) -> int:
        return self.__settings[key_name][0]
    
    def setKey(self, key_name: str, value: int, value_name:str) -> None:
        self.__settings[key_name] =  [value, value_name]

    def getKeyValues(self) -> list:
        return [item for item in self.__settings.items()] 
    
    def get_cheat_code_index(self, code):
        return self.cheat_keys.index(code)

    def key_exists(self, key_to_check) -> bool:
        if key_to_check in self.cheat_keys:
            return True
        
        for value in self.__settings.items():
            if value[1][0] == key_to_check:
                return True
            
        return False
        
    def serialise(self) -> dict:
        pass
