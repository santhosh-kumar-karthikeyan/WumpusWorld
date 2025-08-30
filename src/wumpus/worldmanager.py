from .cell import Cell
import numpy as np

class WorldManager:
    STARTPOS = (0,0)
    def __init__(self,n: int, random_state: float = 0.42):
        self.n = n
        self.world: list[list[Cell]] = []
        #populate map
        for _ in range(n):
            cells = [Cell() for i in range(n)]
            self.world.append(cells)
        
        self.setup(random_state)
        self.setup_perceptions()
    def setup(self,random_state: float = 0.42 ):
        num_pits = np.round(self.n * 0.2)
        available_positions = [(i,j) for i in range(self.n) for j in range(self.n)]
        available_positions.remove(WorldManager.STARTPOS)
        wumpus_pos = np.random.choice(available_positions)
        self.world[wumpus_pos[0]][wumpus_pos[1]].set_flag(Cell.WUMPUS)
        print("Wumpus placecd at: ", wumpus_pos)
        available_positions.remove(wumpus_pos)
        for i in range(num_pits):
            pit_pos = np.random.choice(available_positions)
            self.world[pit_pos[0]][pit_pos[1]].set_flag(Cell.PIT)
            print("Pit placed at: ",pit_pos)
            available_positions.remove(pit_pos)
        gold_pos = np.random.choice(available_positions)
        self.world[gold_pos[0]][gold_pos[1]].set_flag(Cell.GOLD)
        print("Gold placed at: ",gold_pos)
        available_positions.remove(gold_pos)
        
    def setup_perceptions(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.world[i][j].check_flag(Cell.WUMPUS):
                    self.set_adjacent_cells(i,j,Cell.STENCH)
                if self.world[i][j].check_flag(Cell.PIT):
                    self.set_adjacent_cells(i,j,Cell.BREEZE)
                
                    
    def set_adjacent_cells(self, i: int, j: int, flag: int):
        for cell in self.get_adjaent_cells(i,j):
            cell.set_flag(flag)
            
    def get_pos(self, pos: tuple[int,int]):
        if len(pos) != 2:
            return
        return self.world[pos[0]][pos[1]]
    
    def get_world(self):
        return self.world
    
    def get_adjaent_cells(self, pos: tuple[int, int]) -> list[Cell]:
        i, j = pos
        cells: list[Cell] = []
        if i > 0:
            cells.append(self.world[i - 1][j])
        if i < self.n - 1:
            cells.append(self.world[i + 1][j])
        if j > 0:
            cells.append(self.world[i][j - 1])
        if j < self.n - 1:
            cells.append(self.world[i][j + 1])
        return cells