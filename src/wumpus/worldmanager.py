from .cell import Cell
import numpy as np
from typing import Optional

class WorldManager:
    STARTPOS = (0,0)
    def __init__(self, n: int, seed: Optional[int] = None):
        self.n = n
        self.world: list[list[Cell]] = []
        #populate map
        for _ in range(n):
            cells = [Cell() for i in range(n)]
            self.world.append(cells)

        self.setup(seed)
        self.setup_perceptions()
    def setup(self, seed: Optional[int] = None):
        if seed is not None:
            np.random.seed(seed)

        num_pits = int(np.round(self.n * 0.2))
        available_positions = [(i,j) for i in range(self.n) for j in range(self.n)]
        available_positions.remove(WorldManager.STARTPOS)

        # Place wumpus
        wumpus_idx = np.random.randint(len(available_positions))
        wumpus_pos = available_positions.pop(wumpus_idx)
        self.world[wumpus_pos[0]][wumpus_pos[1]].set_flag(Cell.WUMPUS)

        # Place pits
        for _ in range(num_pits):
            if not available_positions:
                break
            pit_idx = np.random.randint(len(available_positions))
            pit_pos = available_positions.pop(pit_idx)
            self.world[pit_pos[0]][pit_pos[1]].set_flag(Cell.PIT)

        # Place gold
        if available_positions:
            gold_idx = np.random.randint(len(available_positions))
            gold_pos = available_positions.pop(gold_idx)
            self.world[gold_pos[0]][gold_pos[1]].set_flag(Cell.GOLD)
        
    def setup_perceptions(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.world[i][j].check_flag(Cell.WUMPUS):
                    self.set_adjacent_cells(i,j,Cell.STENCH)
                if self.world[i][j].check_flag(Cell.PIT):
                    self.set_adjacent_cells(i,j,Cell.BREEZE)
                
                    
    def set_adjacent_cells(self, i: int, j: int, flag: int):
        for cell in self.get_adjacent_cells((i,j)):
            cell.set_flag(flag)
            
    def get_pos(self, pos: tuple[int,int]):
        if len(pos) != 2:
            return
        return self.world[pos[0]][pos[1]]
    
    def get_world(self):
        return self.world
    
    def get_adjacent_cells(self, pos: tuple[int, int]) -> list[Cell]:
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