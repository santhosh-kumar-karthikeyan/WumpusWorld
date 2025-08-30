from .cell import Cell
from .worldmanager import WorldManager
from .sensor import Sensor

class Agent:
    NORTH = TOP = 0
    EAST = RIGHT = 1
    SOUTH = BOTTOM = 2
    WEST = LEFT = 3
    FORWARD = 4
    GRAB = 5
    SHOOT = 6
    def __init__(self, n: int):
        self.world_manager = WorldManager(n)
        self.world: list[list[Cell]] = self.world_manager.get_world()
        self.pos: tuple[int,int] = WorldManager.STARTPOS
        self.has_arrow : bool = True
        self.orientation: int = Agent.RIGHT
        self.sensors: dict[int, bool] = {
            Cell.BREEZE : False,
            Cell.STENCH : False,
            Cell.BUMP : False,
            Cell.GLITTER : False,
            Cell.SCREAM : False
        }
    def make_move(self,move: int) -> None:
        if move != Agent.FORWARD:
            self.orientation = move
            return

        dx,dy = {
            Agent.LEFT : (  0 , -1),
            Agent.RIGHT: (  0 ,  1),
            Agent.TOP  : ( -1,   0),
            Agent.BOTTOM:(  1,   0)
        }.get(self.orientation, (0,0))
        
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
    
    def display_world(self):
        print(self.world)
    
    def sense(self):
        for flag in self.world_manager.get_pos(self.pos).flags:
            self.sensors[flag] = True        
    
    def solve_world(self, num_moves: int):
        #Loop until the agent runs out of moves or finds the gold
        while num_moves > 0 or not self.sensors[Cell.GLITTER]:
            self.sense()
            self.world_manager.get_pos(self.pos).set_flag(Cell.VISITED)
            if self.sensors[Cell.STENCH] or self.sensors[Cell.BREEZE]:
                self.make_move(self.LEFT)
                self.solve_world(num_moves - 1)
            