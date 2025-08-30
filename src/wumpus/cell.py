class Cell:    
    #constants
    BREEZE = 0
    GLITTER = 1
    GOLD = 1
    OK = 2
    PIT = 3
    STENCH = 4
    VISITED = 5
    BUMP = 6
    SCREAM = 7
    WUMPUS = 8
    def __init__(self):
        self.flags : set[int] = set()
            
    def set_flag(self,flag : int):
        self.flags.add(flag)

    def check_flag(self,flag: int):
        if flag in self.flags:
            return True
        return False
    
        