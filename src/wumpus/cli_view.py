import sys
from .game_controller import GameController
from .agent import Agent
from typing import Optional

class CLIView:
    def __init__(self, controller: GameController):
        self.controller = controller

    def display_menu(self):
        print("\n=== Wumpus World ===")
        print("Commands:")
        print("f - Move Forward")
        print("l - Turn Left")
        print("r - Turn Right")
        print("g - Grab Gold")
        print("s - Shoot Arrow")
        print("q - Quit")
        print("? - Show this menu")

    def get_user_action(self) -> Optional[int]:
        """Get action from user input, return None for invalid input"""
        action_map = {
            'f': Agent.FORWARD,
            'l': Agent.LEFT,
            'r': Agent.RIGHT,
            'g': Agent.GRAB,
            's': Agent.SHOOT
        }

        while True:
            try:
                cmd = input("Enter action: ").strip().lower()
                if cmd == 'q':
                    return None
                elif cmd == '?':
                    self.display_menu()
                    continue
                elif cmd in action_map:
                    action = action_map[cmd]
                    available = self.controller.get_available_actions()

                    if action in available:
                        return action
                    elif action == Agent.FORWARD:
                        # Check if forward is risky but possible
                        forward_pos = self._get_forward_position()
                        if forward_pos and not self.controller.agent.kb.is_safe(forward_pos):
                            # Risky move - ask for confirmation
                            confirm = input(f"Forward move to {forward_pos} is risky. Continue? (y/n): ").strip().lower()
                            if confirm == 'y':
                                return action
                            else:
                                continue
                        else:
                            print("Cannot move forward from current position.")
                    else:
                        print("That action is not currently available.")
                        print(f"Available actions: {self._format_actions(available)}")
                else:
                    print("Invalid command. Type '?' for help.")
            except KeyboardInterrupt:
                print("\nGame interrupted.")
                return None

    def _get_forward_position(self) -> Optional[tuple[int, int]]:
        """Get the position the agent would move to if going forward"""
        agent = self.controller.agent
        i, j = agent.pos
        if agent.orientation == Agent.TOP and i > 0:
            return (i-1, j)
        elif agent.orientation == Agent.BOTTOM and i < len(agent.world)-1:
            return (i+1, j)
        elif agent.orientation == Agent.LEFT and j > 0:
            return (i, j-1)
        elif agent.orientation == Agent.RIGHT and j < len(agent.world[0])-1:
            return (i, j+1)
        return None

    def _format_actions(self, actions: list[int]) -> str:
        action_names = {
            Agent.FORWARD: 'forward',
            Agent.LEFT: 'left',
            Agent.RIGHT: 'right',
            Agent.GRAB: 'grab',
            Agent.SHOOT: 'shoot'
        }
        return ', '.join(action_names.get(a, str(a)) for a in actions)

    def display_game_result(self, result: str):
        if result == 'win':
            print(f"\n🎉 Congratulations! You won with score: {self.controller.get_score()}")
        elif result == 'lose':
            print(f"\n💀 Game Over! Final score: {self.controller.get_score()}")
        else:
            print(f"\nGame ended. Final score: {self.controller.get_score()}")

    def run_game(self):
        self.display_menu()
        self.controller.start_game()

        while True:
            action = self.get_user_action()
            if action is None:
                break

            game_continues = self.controller.process_action(action)
            game_state = self.controller.get_game_state()

            if not game_continues:
                if game_state:
                    self.display_game_result(game_state)
                break