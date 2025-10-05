#!/usr/bin/env python3
"""
Wumpus World Game - CLI Application

A complete implementation of the Wumpus World problem with AI agent inference.
"""

import argparse
import sys
from .game_controller import GameController
from .cli_view import CLIView

def main():
    parser = argparse.ArgumentParser(
        description="Wumpus World Game - An AI agent navigates a dangerous world to find gold.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m wumpus.main          # Play with default 4x4 world
  python -m wumpus.main -n 6     # Play with 6x6 world
  python -m wumpus.main -s 42    # Play with seed 42 for reproducible world
  python -m wumpus.main --help   # Show this help
        """
    )

    parser.add_argument(
        '-n', '--size',
        type=int,
        default=4,
        help='Size of the world grid (default: 4)'
    )

    parser.add_argument(
        '-s', '--seed',
        type=int,
        help='Random seed for reproducible world generation'
    )

    args = parser.parse_args()

    if args.size < 3:
        print("Error: World size must be at least 3x3", file=sys.stderr)
        sys.exit(1)

    try:
        # Create MVC components
        controller = GameController(args.size, args.seed)
        view = CLIView(controller)

        # Start the game
        view.run_game()

    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()