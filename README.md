# Wumpus World

A complete implementation of the classic Wumpus World AI problem with logical inference, featuring an intelligent agent that navigates a dangerous grid world to find gold while avoiding pits and the wumpus.

## Features

- **Intelligent Agent**: Uses propositional logic and inference to determine safe cells
- **Complete Wumpus World**: All 5 senses (stench, breeze, glitter, bump, scream)
- **Strategic Shooting**: Agent only shoots when wumpus location is confirmed via inference
- **Scoring System**: Comprehensive reward/penalty system
- **Reproducible Worlds**: Seed-based world generation
- **MVC Architecture**: Clean separation of concerns
- **CLI Interface**: User-friendly command-line interface
- **Unit Tests**: Comprehensive test coverage
- **Modular Design**: Easily extensible and maintainable

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd WumpusWorld

# Install dependencies
pip install -e .
# Or with dev dependencies
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Play with default 4x4 world
wumpus

# Play with custom size
wumpus -n 6

# Play with reproducible seed
wumpus -s 42

# Show help
wumpus --help
```

### Game Commands

- `f` - Move Forward
- `l` - Turn Left
- `r` - Turn Right
- `g` - Grab Gold
- `s` - Shoot Arrow
- `q` - Quit
- `?` - Show help

## Game Rules

### Objective
- Find and grab the gold
- Return to start (optional in this implementation)
- Avoid dying from pits or wumpus

### World Elements
- **Agent (A)**: Starts at (0,0), can move and turn
- **Gold (G)**: Goal to collect
- **Wumpus (W/D)**: Deadly creature, killed by arrow
- **Pits (P)**: Bottomless pits
- **Visited (. )**: Explored safe cells
- **Unknown (? )**: Unexplored cells

### Senses
- **Stench**: Adjacent to wumpus
- **Breeze**: Adjacent to pit
- **Glitter**: On gold cell
- **Bump**: Hit a wall
- **Scream**: Wumpus died

### Scoring
- **+1000**: Grabbing gold
- **+500**: Killing wumpus
- **-1000**: Death (pit or wumpus)
- **-10**: Shooting arrow
- **-1**: Moving or turning
- **-1**: Bumping into wall

## Architecture

### MVC Pattern
- **Model**: `Agent`, `KnowledgeBase`, `WorldManager`, `Cell`
- **View**: `CLIView`
- **Controller**: `GameController`

### Key Components

#### Agent
- Manages agent state and actions
- Interfaces with knowledge base for decision making
- Handles scoring and game state

#### KnowledgeBase
- Implements logical inference
- Tracks possible/dangerous locations
- Determines safe actions

#### WorldManager
- Generates and manages the game world
- Places entities (wumpus, pits, gold)
- Provides world state access

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=wumpus --cov-report=html
```

### Code Quality

The codebase follows these principles:
- **DRY**: Don't Repeat Yourself
- **SOLID**: Single responsibility, Open-closed, etc.
- **Clean Code**: Readable, maintainable, extensible
- **Type Hints**: Full type annotation
- **Documentation**: Comprehensive docstrings

## Algorithm

### Inference System

The agent uses propositional logic to infer safe cells:

1. **Initial State**: Only start position is known safe
2. **Perception Update**: Update KB with current cell perceptions
3. **Location Inference**:
   - If stench, wumpus in adjacent cells
   - If breeze, pit in adjacent cells
   - If no perception, no dangers adjacent
4. **Safe Cell Determination**: Cells not in possible danger sets are safe
5. **Definite Locations**: When only one possible location remains

### Shooting Strategy

- Only shoot when wumpus location is certain (single definite location)
- Must be aligned (same row or column)
- Must be facing correct direction
- Only one arrow available

## Examples

### Sample Game Session

```
=== Wumpus World ===
Commands:
f - Move Forward
l - Turn Left
r - Turn Right
g - Grab Gold
s - Shoot Arrow
q - Quit
? - Show this menu

Score: 0
Position: (0, 0), Orientation: 1
Has Arrow: True, Has Gold: False
Wumpus Alive: True

? ? ? ?
? ? ? ?
? ? ? ?
A ? ? ?

Enter action: f

Score: -1
Position: (0, 1), Orientation: 1
Has Arrow: True, Has Gold: False
Wumpus Alive: True

. ? ? ?
. ? ? ?
. ? ? ?
. A ? ?

Available actions: left, right
Enter action: r
...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details