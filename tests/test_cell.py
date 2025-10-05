import pytest
from wumpus.cell import Cell

class TestCell:
    def test_init(self):
        cell = Cell()
        assert isinstance(cell.flags, set)
        assert len(cell.flags) == 0

    def test_set_flag(self):
        cell = Cell()
        cell.set_flag(Cell.PIT)
        assert Cell.PIT in cell.flags

    def test_check_flag(self):
        cell = Cell()
        assert not cell.check_flag(Cell.PIT)
        cell.set_flag(Cell.PIT)
        assert cell.check_flag(Cell.PIT)