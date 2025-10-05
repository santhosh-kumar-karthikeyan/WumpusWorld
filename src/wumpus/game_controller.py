from .agent import Agent
from .worldmanager import WorldManager
from typing import Optional

class GameController:
    def __init__(self, n: int, seed: Optional[int] = None):
        self.agent = Agent(n, seed)
        self.game_state: Optional[str] = None

    def start_game(self):
        """Initialize the game"""
        self.agent.update_knowledge()
        self.display_world()

    def process_action(self, action: int) -> bool:
        """Process an action and return True if game continues"""
        if action == Agent.GRAB:
            self.agent.grab_gold()
        elif action == Agent.SHOOT:
            self.agent.shoot_arrow()
        else:
            self.agent.make_move(action)

        # Update knowledge after action
        self.agent.update_knowledge()

        # Check game end conditions
        self.game_state = self.agent.check_game_end()

        self.display_world()

        return self.game_state is None

    def get_available_actions(self) -> list[int]:
        """Get actions that are currently safe/possible"""
        actions = self.agent.get_safe_actions()

        # Add grab if there's gold here
        current_cell = self.agent.world_manager.get_pos(self.agent.pos)
        if current_cell.check_flag(self.agent.world_manager.world[0][0].__class__.GOLD):
            actions.append(Agent.GRAB)

        # Add shoot if conditions met
        if self.agent.kb.should_shoot(self.agent.pos, self.agent.orientation):
            actions.append(Agent.SHOOT)

        # Always allow forward if not at wall (even if risky)
        if self._can_move_forward():
            if Agent.FORWARD not in actions:
                actions.append(Agent.FORWARD)

        return actions

    def _can_move_forward(self) -> bool:
        """Check if forward movement is physically possible"""
        i, j = self.agent.pos
        if self.agent.orientation == Agent.TOP:
            return i > 0
        elif self.agent.orientation == Agent.BOTTOM:
            return i < len(self.agent.world) - 1
        elif self.agent.orientation == Agent.LEFT:
            return j > 0
        elif self.agent.orientation == Agent.RIGHT:
            return j < len(self.agent.world[0]) - 1
        return False

    def display_world(self):
        self.agent.display_world()

    def get_game_state(self) -> Optional[str]:
        return self.game_state

    def get_score(self) -> int:
        return self.agent.score