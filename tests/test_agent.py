import pytest
from wumpus.agent import Agent
from wumpus.cell import Cell

class TestAgent:
    def test_init(self):
        agent = Agent(4, seed=42)
        assert agent.pos == (0, 0)
        assert agent.orientation == Agent.RIGHT
        assert agent.has_arrow
        assert agent.alive
        assert not agent.has_gold
        assert agent.score == 0

    def test_make_move_turn(self):
        agent = Agent(4, seed=42)
        initial_orientation = agent.orientation
        agent.make_move(Agent.LEFT)
        assert agent.orientation == Agent.LEFT
        assert agent.score == -1  # Turning costs 1

    def test_make_move_forward(self):
        agent = Agent(4, seed=42)
        initial_pos = agent.pos
        agent.make_move(Agent.FORWARD)
        assert agent.pos != initial_pos
        assert agent.score == -1  # Moving costs 1

    def test_make_move_wall_bump(self):
        agent = Agent(4, seed=42)
        # Move to edge
        agent.pos = (0, 0)
        agent.orientation = Agent.TOP  # Try to move up from top edge
        result = agent.make_move(Agent.FORWARD)
        assert not result  # Should fail
        assert agent.pos == (0, 0)  # Position unchanged
        assert agent.sensors[Cell.BUMP]  # Bump sensor triggered
        assert agent.score == -1  # Bumping costs 1 point

    def test_sense(self):
        agent = Agent(4, seed=42)
        sensors = agent.sense()
        assert isinstance(sensors, dict)
        # Should have all sensor keys
        expected_keys = {Cell.BREEZE, Cell.STENCH, Cell.BUMP, Cell.GLITTER, Cell.SCREAM}
        assert set(sensors.keys()) == expected_keys

    def test_grab_gold(self):
        agent = Agent(4, seed=42)
        # Manually place gold at agent's position
        agent.world_manager.get_pos(agent.pos).set_flag(Cell.GOLD)
        result = agent.grab_gold()
        assert result
        assert agent.has_gold
        assert agent.score == 1000  # Gold gives 1000 points

    def test_check_game_end_win(self):
        agent = Agent(4, seed=42)
        agent.has_gold = True
        result = agent.check_game_end()
        assert result == 'win'

    def test_check_game_end_lose_wumpus(self):
        agent = Agent(4, seed=42)
        # Place wumpus at agent's position
        agent.world_manager.get_pos(agent.pos).set_flag(Cell.WUMPUS)
        result = agent.check_game_end()
        assert result == 'lose'
        assert not agent.alive
        assert agent.score == -1000  # Wumpus death costs 1000

    def test_check_game_end_lose_pit(self):
        agent = Agent(4, seed=42)
        # Place pit at agent's position
        agent.world_manager.get_pos(agent.pos).set_flag(Cell.PIT)
        result = agent.check_game_end()
        assert result == 'lose'
        assert not agent.alive
        assert agent.score == -1000  # Pit death costs 1000