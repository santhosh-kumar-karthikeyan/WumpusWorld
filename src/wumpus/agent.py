from .cell import Cell
from .worldmanager import WorldManager
from .sensor import Sensor
from .knowledge_base import KnowledgeBase
from typing import Tuple, List, Optional

class Agent:
    NORTH = TOP = 0
    EAST = RIGHT = 1
    SOUTH = BOTTOM = 2
    WEST = LEFT = 3
    FORWARD = 4
    GRAB = 5
    SHOOT = 6

    def __init__(self, n: int, seed: Optional[int] = None):
        self.world_manager = WorldManager(n, seed)
        self.world: List[List[Cell]] = self.world_manager.get_world()
        self.pos: Tuple[int, int] = WorldManager.STARTPOS
        self.has_arrow: bool = True
        self.orientation: int = Agent.RIGHT
        self.kb = KnowledgeBase(n)
        self.score: int = 0
        self.alive: bool = True
        self.has_gold: bool = False
        self.sensors: dict[int, bool] = {
            Cell.BREEZE: False,
            Cell.STENCH: False,
            Cell.BUMP: False,
            Cell.GLITTER: False,
            Cell.SCREAM: False
        }

    def reset_sensors(self):
        for key in self.sensors:
            self.sensors[key] = False

    def sense(self) -> dict[int, bool]:
        self.reset_sensors()
        current_cell = self.world_manager.get_pos(self.pos)
        for flag in current_cell.flags:
            if flag in self.sensors:
                self.sensors[flag] = True
        return self.sensors.copy()

    def make_move(self, move: int) -> bool:
        """Returns True if move was successful, False if bumped into wall"""
        if move in [Agent.LEFT, Agent.RIGHT]:
            self.orientation = move
            self.score -= 1  # Turning costs 1 point
            return True
        elif move == Agent.FORWARD:
            dx, dy = {
                Agent.LEFT: (0, -1),
                Agent.RIGHT: (0, 1),
                Agent.TOP: (-1, 0),
                Agent.BOTTOM: (1, 0)
            }.get(self.orientation, (0, 0))

            new_pos = (self.pos[0] + dx, self.pos[1] + dy)
            if 0 <= new_pos[0] < len(self.world) and 0 <= new_pos[1] < len(self.world[0]):
                self.pos = new_pos
                self.score -= 1  # Moving costs 1 point
                return True
            else:
                self.sensors[Cell.BUMP] = True
                self.score -= 1  # Bumping costs 1 point
                return False
        return False

    def grab_gold(self):
        current_cell = self.world_manager.get_pos(self.pos)
        if current_cell.check_flag(Cell.GOLD):
            self.has_gold = True
            current_cell.flags.discard(Cell.GOLD)  # Remove gold from cell
            self.score += 1000  # Grabbing gold gives 1000 points
            return True
        return False

    def shoot_arrow(self) -> bool:
        """Returns True if wumpus was killed"""
        if not self.has_arrow or not self.kb.should_shoot(self.pos, self.orientation):
            return False

        self.has_arrow = False
        self.kb.mark_arrow_used()
        self.score -= 10  # Shooting costs 10 points

        # Check if wumpus is in the line of fire
        wumpus_pos = next(iter(self.kb.definite_wumpus))
        if self._is_in_line_of_fire(wumpus_pos):
            self.kb.mark_wumpus_dead()
            self.sensors[Cell.SCREAM] = True
            self.score += 500  # Killing wumpus gives 500 points
            return True
        return False

    def _is_in_line_of_fire(self, wumpus_pos: Tuple[int, int]) -> bool:
        agent_i, agent_j = self.pos
        wumpus_i, wumpus_j = wumpus_pos

        if agent_i == wumpus_i:  # Same row
            if self.orientation == Agent.RIGHT and agent_j < wumpus_j:
                return True
            if self.orientation == Agent.LEFT and agent_j > wumpus_j:
                return True
        elif agent_j == wumpus_j:  # Same column
            if self.orientation == Agent.BOTTOM and agent_i < wumpus_i:
                return True
            if self.orientation == Agent.TOP and agent_i > wumpus_i:
                return True
        return False

    def check_game_end(self) -> Optional[str]:
        """Returns 'win', 'lose', or None"""
        current_cell = self.world_manager.get_pos(self.pos)

        if current_cell.check_flag(Cell.WUMPUS) and self.kb.wumpus_alive:
            self.alive = False
            self.score -= 1000  # Dying from wumpus costs 1000 points
            return 'lose'

        if current_cell.check_flag(Cell.PIT):
            self.alive = False
            self.score -= 1000  # Falling into pit costs 1000 points
            return 'lose'

        if self.has_gold:
            return 'win'

        return None

    def update_knowledge(self):
        sensors = self.sense()
        self.kb.update_knowledge(self.pos, sensors)

    def get_safe_actions(self) -> List[int]:
        return self.kb.get_safe_moves(self.pos, self.orientation)

    def display_world(self):
        """Simple text-based display"""
        print(f"\nScore: {self.score}")
        print(f"Position: {self.pos}, Orientation: {self.orientation}")
        print(f"Has Arrow: {self.has_arrow}, Has Gold: {self.has_gold}")
        print(f"Wumpus Alive: {self.kb.wumpus_alive}")

        for i in range(len(self.world)):
            row = ""
            for j in range(len(self.world[i])):
                cell = self.world[i][j]
                if (i, j) == self.pos:
                    row += "A "  # Agent
                elif cell.check_flag(Cell.WUMPUS) and not self.kb.wumpus_alive:
                    row += "D "  # Dead wumpus
                elif cell.check_flag(Cell.GOLD):
                    row += "G "  # Gold
                elif cell.check_flag(Cell.PIT):
                    row += "P "  # Pit
                elif (i, j) in self.kb.visited:
                    row += ". "  # Visited safe cell
                else:
                    row += "? "  # Unknown
            print(row)
        print()
            