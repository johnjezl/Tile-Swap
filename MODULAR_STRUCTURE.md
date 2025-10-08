# Tile Swap - Modular Structure

## Overview

The Tile Swap codebase has been refactored into a clean modular structure with each class in its own file. This provides better organization, easier maintenance, and improved code reusability.

## Module Structure

```
tile_swap/
├── tile_swap.py          # Main entry point (27 lines)
├── graph.py              # Graph data structure (63 lines)
├── tile_manager.py       # Tile operations (79 lines)
├── graph_builder.py      # Graph creation factory (206 lines)
├── game_display.py       # Visualization and UI (165 lines)
├── score_calculator.py   # Optimal solution calculator (56 lines)
└── tile_swap_game.py     # Game controller (209 lines)
```

## Module Details

### 1. tile_swap.py
**Purpose:** Main entry point for the application

**Contents:**
- `main()` function - Entry point with exception handling
- Imports `TileSwapGame` and runs the game

**Usage:**
```bash
python tile_swap.py
```

**Lines:** 27

---

### 2. graph.py
**Purpose:** Graph data structure

**Contents:**
- `Graph` class - Represents an undirected connected graph

**Key Methods:**
- `add_edge(node1, node2)` - Add edge between nodes
- `get_nodes()` - Return sorted list of nodes
- `get_neighbors(node)` - Return neighbors of a node
- `is_connected()` - Check graph connectivity (BFS)
- `has_node(node)` - Check if node exists
- `are_connected(node1, node2)` - Check if nodes are connected

**Dependencies:** `collections.deque`

**Lines:** 63

---

### 3. tile_manager.py
**Purpose:** Manages tile assignments and operations

**Contents:**
- `TileManager` class - Handles all tile-related operations

**Key Methods:**
- `assign_tiles(tile_assignment)` - Assign tiles to nodes
- `assign_tiles_manually()` - Interactive tile assignment
- `assign_tiles_randomly()` - Random tile assignment
- `swap_tiles(node1, node2)` - Swap tiles between nodes
- `is_solved()` - Check if puzzle is solved
- `get_initial_configuration()` - Get current tile state

**Dependencies:** `random`, `graph.Graph` (via composition)

**Lines:** 79

---

### 4. graph_builder.py
**Purpose:** Factory for creating graphs from various sources

**Contents:**
- `GraphBuilder` class - Static factory methods for graph creation

**Static Methods:**
- `create_manually()` - Interactive edge-by-edge creation
- `create_from_file()` - Load graph from text file
- `create_random()` - Generate random connected graph

**Features:**
- Input validation
- 20-node maximum enforcement
- Connectivity checking
- Error handling

**Dependencies:** `random`, `graph.Graph`

**Lines:** 206

---

### 5. game_display.py
**Purpose:** Handles all visualization and UI output

**Contents:**
- `GameDisplay` class - Manages all game display

**Key Methods:**
- `display_graph_structure()` - Text representation
- `display_tiles()` - Current tile assignments
- `display_visual_graph()` - Circular ASCII art layout
- `display_adjacency_matrix()` - Matrix representation
- `_display_circular_layout()` - Private: circular drawing
- `_draw_line(grid, x1, y1, x2, y2)` - Private: Bresenham's algorithm
- `_display_adjacency_matrix()` - Private: matrix drawing

**Algorithms:**
- Circular layout using polar coordinates
- Bresenham's line drawing algorithm
- 2-digit aligned matrix formatting

**Dependencies:** `math`, `graph.Graph` (via composition)

**Lines:** 165

---

### 6. score_calculator.py
**Purpose:** Computes optimal solutions and scoring

**Contents:**
- `ScoreCalculator` class - Static utility class

**Static Method:**
- `calculate_optimal_moves(tile_configuration)` - Calculate minimum swaps

**Algorithm:**
- Cycle decomposition of permutations
- A cycle of length n requires n-1 swaps
- Returns theoretical minimum number of swaps

**Dependencies:** None (pure algorithm)

**Lines:** 56

---

### 7. tile_swap_game.py
**Purpose:** Main game controller orchestrating all components

**Contents:**
- `TileSwapGame` class - Game controller

**Key Methods:**
- `setup_graph()` - Guide graph creation
- `setup_tiles()` - Guide tile assignment
- `play()` - Main game loop
- `run()` - Complete game session with replay
- `_process_move(user_input)` - Private: validate and process moves
- `_display_victory()` - Private: victory screen

**Dependencies:**
- `graph_builder.GraphBuilder`
- `tile_manager.TileManager`
- `game_display.GameDisplay`
- `score_calculator.ScoreCalculator`

**Lines:** 209

---

## Dependency Graph

```
tile_swap.py
    └── tile_swap_game.py
            ├── graph_builder.py
            │       └── graph.py
            ├── tile_manager.py
            │       └── graph.py (via composition)
            ├── game_display.py
            │       └── graph.py (via composition)
            └── score_calculator.py (no dependencies)
```

## Import Flow

```python
# tile_swap.py
from tile_swap_game import TileSwapGame

# tile_swap_game.py
from graph_builder import GraphBuilder
from tile_manager import TileManager
from game_display import GameDisplay
from score_calculator import ScoreCalculator

# graph_builder.py
from graph import Graph

# tile_manager.py
(receives Graph instance via composition)

# game_display.py
(receives Graph instance via composition)

# score_calculator.py
(static methods, no imports needed)

# graph.py
from collections import deque
```

## Benefits of Modular Structure

### 1. Maintainability
- Each module has a single, clear purpose
- Changes to one module don't affect others
- Easy to locate specific functionality

### 2. Testability
- Each module can be tested independently
- Mock objects can be injected easily
- Unit tests are straightforward to write

### 3. Reusability
- `Graph` class can be used in other projects
- `ScoreCalculator` is a standalone utility
- `GameDisplay` could be adapted for similar games

### 4. Readability
- Clear module names indicate purpose
- Smaller files are easier to understand
- Logical separation of concerns

### 5. Scalability
- Easy to add new graph creation methods
- Simple to add new display modes
- New scoring algorithms can be added independently

## Running the Game

### Standard Execution
```bash
python tile_swap.py
```

### Module Testing
```bash
python test_modular_imports.py
```

### Import in Another Program
```python
from tile_swap_game import TileSwapGame

game = TileSwapGame()
game.run()
```

## File Sizes

| Module | Lines | Purpose |
|--------|-------|---------|
| `tile_swap.py` | 27 | Entry point |
| `graph.py` | 63 | Data structure |
| `tile_manager.py` | 79 | Tile operations |
| `graph_builder.py` | 206 | Graph creation |
| `game_display.py` | 165 | Visualization |
| `score_calculator.py` | 56 | Scoring |
| `tile_swap_game.py` | 209 | Game control |
| **Total** | **805** | **Full game** |

## Backward Compatibility

The original monolithic `tile_swap.py` file still exists for reference but has been replaced with the modular version. The game functionality remains 100% identical.

## Design Patterns Used

1. **Factory Pattern** - `GraphBuilder` with static factory methods
2. **Composition** - `TileSwapGame` composes other classes
3. **Single Responsibility** - Each module has one purpose
4. **Separation of Concerns** - Logic, data, and display are separate
5. **Dependency Injection** - `Graph` instances passed to managers

## Future Enhancements

The modular structure makes it easy to add:
- New graph creation methods (JSON, XML, database)
- Alternative display modes (web interface, GUI)
- Different scoring algorithms
- Multiplayer support (separate game instances)
- Save/load game state
- Achievements and statistics tracking

## Testing

All modules have been tested:
- ✓ Individual imports
- ✓ Class instantiation
- ✓ Basic functionality
- ✓ Integration between modules
- ✓ Full game execution

Run `test_modular_imports.py` to verify the structure.

## Conclusion

The modular structure transforms Tile Swap from a single-file script into a professional, maintainable Python application. Each module is self-contained, well-documented, and follows OOP best practices.
