import pytest
from wumpus.knowledge_base import KnowledgeBase
from wumpus.cell import Cell
from wumpus.agent import Agent

class TestKnowledgeBase:
    def test_init(self):
        kb = KnowledgeBase(4)
        assert len(kb.visited) == 0
        assert (0, 0) in kb.safe
        assert kb.wumpus_alive
        assert not kb.arrow_used

    def test_update_knowledge_breeze(self):
        kb = KnowledgeBase(4)
        sensors = {Cell.BREEZE: True, Cell.STENCH: False, Cell.GLITTER: False, Cell.BUMP: False, Cell.SCREAM: False}
        kb.update_knowledge((0, 0), sensors)
        assert (0, 0) in kb.visited
        assert (0, 0) in kb.breeze_cells

    def test_update_knowledge_stench(self):
        kb = KnowledgeBase(4)
        sensors = {Cell.BREEZE: False, Cell.STENCH: True, Cell.GLITTER: False, Cell.BUMP: False, Cell.SCREAM: False}
        kb.update_knowledge((0, 0), sensors)
        assert (0, 0) in kb.stench_cells

    def test_is_safe(self):
        kb = KnowledgeBase(4)
        assert kb.is_safe((0, 0))  # Start position is safe
        assert not kb.is_safe((1, 1))  # Unknown positions are not safe initially

    def test_get_safe_moves(self):
        kb = KnowledgeBase(4)
        # Initially only turns are safe (can't move forward to unknown)
        moves = kb.get_safe_moves((0, 0), Agent.RIGHT)
        assert Agent.LEFT in moves
        assert Agent.RIGHT in moves
        # Forward might not be safe initially

    def test_mark_wumpus_dead(self):
        kb = KnowledgeBase(4)
        kb.mark_wumpus_dead()
        assert not kb.wumpus_alive
        assert len(kb.possible_wumpus) == 0
        assert len(kb.definite_wumpus) == 0

    def test_mark_arrow_used(self):
        kb = KnowledgeBase(4)
        kb.mark_arrow_used()
        assert kb.arrow_used