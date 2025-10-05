"""
Wumpus World - A complete AI agent implementation with logical inference
"""

from .agent import Agent
from .cell import Cell
from .worldmanager import WorldManager
from .knowledge_base import KnowledgeBase
from .game_controller import GameController
from .cli_view import CLIView
from .main import main

__version__ = "1.0.0"
__all__ = [
    "Agent",
    "Cell",
    "WorldManager",
    "KnowledgeBase",
    "GameController",
    "CLIView",
    "main"
]