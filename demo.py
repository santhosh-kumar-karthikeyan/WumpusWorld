#!/usr/bin/env python3
"""
Demo script to show world generation and basic agent functionality
"""

from wumpus import Agent, WorldManager

def demo():
    print("=== Wumpus World Demo ===\n")

    # Create agent with seed for reproducible world
    agent = Agent(4, seed=42)

    print("Generated World (revealed for demo):")
    for i in range(4):
        row = ""
        for j in range(4):
            cell = agent.world[i][j]
            if cell.check_flag(agent.world_manager.world[0][0].__class__.WUMPUS):
                row += "W "
            elif cell.check_flag(agent.world_manager.world[0][0].__class__.PIT):
                row += "P "
            elif cell.check_flag(agent.world_manager.world[0][0].__class__.GOLD):
                row += "G "
            else:
                row += ". "
        print(row)
    print()

    print("Agent starts at (0,0)")
    print(f"Initial sensors: {agent.sense()}")
    print(f"Initial safe moves: {agent.get_safe_actions()}")
    print()

    # Simulate first move
    print("Agent turns right...")
    agent.make_move(agent.RIGHT)
    print(f"New orientation: {agent.orientation}")
    print(f"Score: {agent.score}")
    print()

    print("Agent moves forward...")
    agent.make_move(agent.FORWARD)
    print(f"New position: {agent.pos}")
    print(f"Sensors after move: {agent.sense()}")
    print(f"Score: {agent.score}")
    print()

    # Update knowledge
    agent.update_knowledge()
    print(f"Safe moves after inference: {agent.get_safe_actions()}")

if __name__ == '__main__':
    demo()