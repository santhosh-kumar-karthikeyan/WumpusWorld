from typing import Set, Tuple, List, Optional
from .cell import Cell

class KnowledgeBase:
    # Direction constants (matching Agent)
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3
    FORWARD = 4
    def __init__(self, n: int):
        self.n = n
        self.visited: Set[Tuple[int, int]] = set()
        self.safe: Set[Tuple[int, int]] = {(0, 0)}  # Start position is safe
        self.possible_pits: Set[Tuple[int, int]] = set()
        self.possible_wumpus: Set[Tuple[int, int]] = set()
        self.definite_pits: Set[Tuple[int, int]] = set()
        self.definite_wumpus: Set[Tuple[int, int]] = set()
        self.breeze_cells: Set[Tuple[int, int]] = set()
        self.stench_cells: Set[Tuple[int, int]] = set()
        self.wumpus_alive = True
        self.arrow_used = False

        # Initialize possible locations (exclude start)
        for i in range(n):
            for j in range(n):
                if (i, j) != (0, 0):
                    self.possible_pits.add((i, j))
                    self.possible_wumpus.add((i, j))

    def update_knowledge(self, pos: Tuple[int, int], sensors: dict):
        self.visited.add(pos)

        if sensors[Cell.BREEZE]:
            self.breeze_cells.add(pos)
        if sensors[Cell.STENCH]:
            self.stench_cells.add(pos)

        # Update possible locations based on perceptions
        self._update_possible_locations(pos, sensors)

        # Infer definite locations
        self._infer_definite_locations()

    def _update_possible_locations(self, pos: Tuple[int, int], sensors: dict):
        adjacent = self._get_adjacent(pos)

        if sensors[Cell.BREEZE]:
            # If breeze, there must be a pit in adjacent cells
            # Remove non-adjacent from possible pits
            to_remove = set()
            for p in self.possible_pits:
                if p not in adjacent:
                    to_remove.add(p)
            self.possible_pits -= to_remove
        else:
            # No breeze, no pits in adjacent cells
            self.possible_pits -= set(adjacent)

        if sensors[Cell.STENCH] and self.wumpus_alive:
            # If stench, wumpus in adjacent
            to_remove = set()
            for w in self.possible_wumpus:
                if w not in adjacent:
                    to_remove.add(w)
            self.possible_wumpus -= to_remove
        elif not sensors[Cell.STENCH] and self.wumpus_alive:
            # No stench, no wumpus in adjacent
            self.possible_wumpus -= set(adjacent)

    def _infer_definite_locations(self):
        # If only one possible location for pit/wumpus, it's definite
        if len(self.possible_pits) == 1:
            pit_pos = next(iter(self.possible_pits))
            self.definite_pits.add(pit_pos)
            self.possible_pits.clear()

        if len(self.possible_wumpus) == 1 and self.wumpus_alive:
            wumpus_pos = next(iter(self.possible_wumpus))
            self.definite_wumpus.add(wumpus_pos)
            self.possible_wumpus.clear()

        # Update safe cells
        all_possible_dangers = self.possible_pits | self.possible_wumpus
        for i in range(self.n):
            for j in range(self.n):
                pos = (i, j)
                if pos not in self.visited and pos not in all_possible_dangers:
                    self.safe.add(pos)

    def is_safe(self, pos: Tuple[int, int]) -> bool:
        return pos in self.safe

    def get_safe_moves(self, pos: Tuple[int, int], orientation: int) -> List[int]:
        moves = []
        adjacent = self._get_adjacent(pos)

        # Check forward move
        forward_pos = self._get_forward_pos(pos, orientation)
        if forward_pos and self.is_safe(forward_pos):
            moves.append(self.FORWARD)

        # Check turns (always safe, just change orientation)
        moves.extend([self.LEFT, self.RIGHT])

        return moves

    def should_shoot(self, pos: Tuple[int, int], orientation: int) -> bool:
        if not self.wumpus_alive or self.arrow_used or len(self.definite_wumpus) != 1:
            return False

        wumpus_pos = next(iter(self.definite_wumpus))
        wumpus_i, wumpus_j = wumpus_pos
        agent_i, agent_j = pos

        # Must be in same row or column
        if agent_i != wumpus_i and agent_j != wumpus_j:
            return False

        # Must be facing the correct direction
        if agent_i == wumpus_i:  # Same row
            if agent_j < wumpus_j and orientation != self.RIGHT:
                return False
            if agent_j > wumpus_j and orientation != self.LEFT:
                return False
        else:  # Same column
            if agent_i < wumpus_i and orientation != self.BOTTOM:
                return False
            if agent_i > wumpus_i and orientation != self.TOP:
                return False

        return True

    def _get_adjacent(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        i, j = pos
        adjacent = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.n and 0 <= nj < self.n:
                adjacent.append((ni, nj))
        return adjacent

    def _get_forward_pos(self, pos: Tuple[int, int], orientation: int) -> Optional[Tuple[int, int]]:
        i, j = pos
        if orientation == self.TOP:
            return (i-1, j) if i > 0 else None
        elif orientation == self.BOTTOM:
            return (i+1, j) if i < self.n-1 else None
        elif orientation == self.LEFT:
            return (i, j-1) if j > 0 else None
        elif orientation == self.RIGHT:
            return (i, j+1) if j < self.n-1 else None
        return None

    def mark_wumpus_dead(self):
        self.wumpus_alive = False
        self.possible_wumpus.clear()
        self.definite_wumpus.clear()
        # Recalculate safe cells
        self._infer_definite_locations()

    def mark_arrow_used(self):
        self.arrow_used = True