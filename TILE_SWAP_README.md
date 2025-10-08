# Tile Swap

**A Graph-Based Puzzle Game**

Tile Swap is a puzzle game where players create a connected graph and swap tiles between connected nodes until all tiles match their corresponding node numbers.

## Requirements

- Python 3.x (no additional libraries required)
- Works on Windows and macOS

## How to Run

```bash
python tile_swap.py
```

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
Legend: [Node:Tile=] (= means matched, ! means not matched)
```

**For larger graphs (>10 nodes)**: Displays an adjacency matrix with tile information (2-digit aligned formatting)

**Display timing**:
- Adjacency matrix (large graphs only): Shown once at game start
- Visual graph: Shown **before each move prompt** so you can see current state and plan your move
- After each move: Tile list and score are updated

## Object-Oriented Architecture

Tile Swap is built with a clean, fully object-oriented design:

### Core Classes

- **`Graph`**: Represents the undirected connected graph structure
  - Manages nodes, edges, and connectivity
  - Stores tile assignments

- **`TileManager`**: Handles all tile-related operations
  - Manual and random tile assignment
  - Tile swapping logic
  - Solution checking

- **`GraphBuilder`**: Factory class for graph creation
  - Static methods for manual, file-based, and random graph generation
  - Input validation and connectivity checking

- **`GameDisplay`**: Manages all visualization and UI
  - Text-based graph structure display
  - ASCII art circular layout (small graphs)
  - Adjacency matrix display (large graphs)
  - Tile status display

- **`ScoreCalculator`**: Computes optimal solutions
  - Cycle decomposition algorithm for permutations
  - Calculates minimum swaps needed

- **`TileSwapGame`**: Main game controller
  - Orchestrates game flow
  - Manages game state
  - Processes player moves
  - Victory conditions

### Design Principles

- **Separation of Concerns**: Each class has a single, well-defined responsibility
- **Encapsulation**: Internal state is protected and accessed through methods
- **Composition**: Game controller composes other classes rather than inheriting
- **Static Factory Methods**: GraphBuilder uses static methods for creation patterns

## Features

- ✓ Fully object-oriented architecture
- ✓ Three graph creation methods (manual, file, random)
- ✓ Ensures graph connectivity
- ✓ Two tile assignment methods (manual, random)
- ✓ **ASCII art graph visualization** (circular layout for small graphs, matrix for large)
- ✓ Move validation (only connected nodes)
- ✓ Real-time score tracking
- ✓ Optimal solution calculation using cycle decomposition
- ✓ Performance rating on completion
- ✓ Quit option at every step
- ✓ Clear visual feedback with matched tile indicators

## Algorithm Notes

The optimal solution is calculated using **cycle decomposition** of the permutation:
- Each cycle of length n requires n-1 swaps to resolve
- This gives the theoretical minimum number of swaps needed
- Note: The graph structure may make the optimal solution unreachable if not all swaps are possible

## Code Structure

```
tile_swap.py
├── Graph                  # Graph data structure
├── TileManager            # Tile operations
├── GraphBuilder           # Graph creation factory
├── GameDisplay            # Visualization and UI
├── ScoreCalculator        # Optimal solution calculator
├── TileSwapGame          # Main game controller
└── main()                 # Entry point
```

## Example Session

```
==================================================
TILE SWAP
A Graph-Based Puzzle Game
==================================================

STEP 1: Create Graph
1. Enter edges manually
2. Load from file
3. Generate random graph
q. Quit

Choice: 3
Enter number of nodes: 4
Enter number of edges (min 3, max 6), or press Enter for random:
Generated random graph with 4 nodes and 5 edges.

STEP 2: Assign Tiles
1. Assign tiles manually
2. Assign tiles randomly
q. Quit

Choice: 2
Tiles assigned randomly.

==================================================
TILE SWAP - GAME START
==================================================

[Visual graph appears before each move]

Current Score (moves): 0
Optimal Solution: 3 moves
```

Enjoy Tile Swap!
