# Graph Tile Puzzle Game

A Python puzzle game where players create a connected graph and swap tiles between connected nodes until all tiles match their corresponding node numbers.

## Disclosures

This game was completely vibe coded usig Claude Code 2.0.1. The prompts used are included in the file 'CLAUDE CODE SESSION.md' 

## Requirements

### Command Line Interface
- Python 3.x (no additional libraries required)
- Works on Windows and macOS

### Web Interface (NEW!)
- Python 3.x
- Flask 3.0.0
- Works on all platforms with a modern web browser

## How to Run

### Command Line Interface

```bash
python graph_tile_game.py
```

### Web Interface (NEW!)

The game now includes a modern web interface with interactive graph visualization!

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Start the web server:
```bash
python web_app.py
```

3. Open your browser to: **http://localhost:5000**

**Web Interface Features:**
- Interactive canvas where you can click nodes to swap tiles
- Real-time visual feedback with color-coded nodes (green = matched, blue = unmatched)
- Click a node to select it (yellow outline), then click a connected node to swap
- Smooth animations and hover effects
- Responsive design that works on desktop and mobile
- All the same game logic as the command-line version

## Game Instructions

### Step 1: Create a Graph

Choose one of three methods to create your graph:

1. **Manual Entry**: Enter edges one by one in the format `node1 node2`
2. **Load from File**: Provide a text file with one edge per line (see `sample_graph.txt`)
3. **Random Generation**: Specify number of nodes and edges (or let the game choose randomly)

### Step 2: Assign Tiles

Choose how to assign tiles to nodes:

1. **Manual Assignment**: Assign each tile number to a node yourself
2. **Random Assignment**: Let the game randomly assign tiles

### Step 3: Play the Game

- Swap tiles between **connected nodes** by entering: `node1 node2`
- Your current score (number of moves) is displayed after each swap
- The optimal solution is shown at the start
- Goal: Match all tile numbers to their corresponding node numbers
- Enter `q` at any time to quit

### Winning

When all tiles match their nodes, you win! The game will show:

- Your final score (total moves)
- The optimal number of moves
- Performance rating

## File Format

For loading graphs from a file, use this format:

```

1 2
2 3
3 4
4 1
1 3

```

- One edge per line: `node1 node2`
- Lines starting with `#` are treated as comments
- Blank lines are ignored
- Node numbers must be positive integers

## Visual Graph Display

The game includes ASCII art visualization of your graph:

**For small graphs (≤10 nodes)**: Displays nodes in a circular layout with connecting edges
```

Visual Graph Representation:
============================================================

          [1:3!]
            \|\
           \ | \
          \  |  \
  [4:2!]     |    [2:1!]
          \  |  \
           \ | \
            \|\
          [3:4!]
============================================================
Legend: [Node:Tile=] (= matched, ! means not matched)

```

**For larger graphs (>10 nodes)**: Displays an adjacency matrix with tile information (2-digit aligned formatting)

**Display timing**:
- Adjacency matrix (large graphs only): Shown once at game start
- Visual graph: Shown **before each move prompt** so you can see current state and plan your move
- After each move: Tile list and score are updated

## Example Gameplay

```

Graph Structure:
  Node 1: connected to [2, 3, 4]
  Node 2: connected to [1, 3]
  Node 3: connected to [1, 2, 4]
  Node 4: connected to [1, 3]

Current Tile Assignments:
  Node 1: Tile 3
  Node 2: Tile 1
  Node 3: Tile 4
  Node 4: Tile 2

Current Score (moves): 0
Optimal Solution: 3 moves

Enter two connected nodes to swap their tiles (node1 node2): 1 2

Current Tile Assignments:
  Node 1: Tile 1 ✓
  Node 2: Tile 3
  Node 3: Tile 4
  Node 4: Tile 2

Current Score (moves): 1

```

## Features

### Core Game Features
- Three graph creation methods (manual, file, random)
- Ensures graph connectivity
- Two tile assignment methods (manual, random)
- Move validation (only connected nodes)
- Real-time score tracking
- Optimal solution calculation using cycle decomposition
- Performance rating on completion
- Clear visual feedback with matched tile indicators

### Command Line Interface
- **ASCII art graph visualization** (circular layout for small graphs, matrix for large)
- Quit option at every step
- Text-based interaction

### Web Interface
- **Interactive HTML5 canvas visualization** with circular graph layout
- Click-to-play interaction (no typing required)
- Color-coded nodes (green for matched, blue for unmatched)
- Hover effects and visual feedback
- Victory modal with performance analysis
- Modern, responsive design
- Session-based multiplayer support (different users get different game states)

## Modular Architecture

The codebase is designed with modularity in mind, making it easy to switch between interfaces or add new ones:

### Core Modules (Shared by both interfaces)
- **graph.py** - Graph data structure and connectivity logic
- **graph_builder.py** - Factory for creating graphs (manual, file, random)
- **tile_manager.py** - Tile assignment and swap operations
- **score_calculator.py** - Optimal solution calculation using cycle decomposition
- **game_display.py** - Display logic for command-line interface

### Command Line Interface
- **graph_tile_game.py** - Original monolithic version
- **tile_swap_game.py** - Modular game controller for CLI
- **tile_swap.py** - Entry point for modular CLI version

### Web Interface
- **web_game_state.py** - Game state manager for web (adapts core modules to web API)
- **web_app.py** - Flask application with REST API endpoints
- **templates/index.html** - HTML5 game interface
- **static/game.js** - Interactive canvas visualization and game logic
- **static/style.css** - Modern, responsive styling

The modular design means:
- Core game logic is reused between both interfaces
- Adding a new interface only requires creating an adapter (like `web_game_state.py`)
- Business logic is completely separated from presentation
- Easy to test, maintain, and extend

## Algorithm Notes

The optimal solution is calculated using **cycle decomposition** of the permutation:

- Each cycle of length n requires n-1 swaps to resolve
- This gives the theoretical minimum number of swaps needed
- Note: The graph structure may make the optimal solution unreachable if not all swaps are possible

Enjoy the puzzle!

#
