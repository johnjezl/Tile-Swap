# Tile Swap - Module Breakdown

## Quick Reference

| File | Class | Responsibility | Dependencies |
|------|-------|----------------|--------------|
| `tile_swap.py` | None (entry point) | Main entry point | `tile_swap_game` |
| `graph.py` | `Graph` | Graph data structure | `collections` |
| `tile_manager.py` | `TileManager` | Tile operations | `random` |
| `graph_builder.py` | `GraphBuilder` | Graph creation | `random`, `graph` |
| `game_display.py` | `GameDisplay` | Visualization | `math` |
| `score_calculator.py` | `ScoreCalculator` | Optimal scoring | None |
| `tile_swap_game.py` | `TileSwapGame` | Game controller | All above |

## Module Hierarchy

```
┌─────────────────┐
│  tile_swap.py   │  Entry Point
│   (main only)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ tile_swap_game.py   │  Game Controller
│  (TileSwapGame)     │
└──┬──┬──┬───────┬───┘
   │  │  │       │
   │  │  │       └─────────────────┐
   │  │  │                         │
   │  │  └──────────────┐          │
   │  │                 │          │
   │  └────────┐        │          │
   │           │        │          │
   ▼           ▼        ▼          ▼
┌──────┐  ┌─────────┐ ┌────────┐ ┌────────────┐
│graph │  │  tile_  │ │ game_  │ │   score_   │
│.py   │  │manager  │ │display │ │calculator  │
│      │  │ .py     │ │ .py    │ │ .py        │
└──────┘  └────┬────┘ └───┬────┘ └────────────┘
   ▲           │           │
   │           │           │
   └───────────┴───────────┘
        (uses Graph)

┌──────────────────┐
│ graph_builder.py │  Factory
│ (GraphBuilder)   │
└────────┬─────────┘
         │
         ▼
    ┌──────┐
    │graph │
    │.py   │
    └──────┘
```

## Import Chain

### Level 0 (No dependencies)
- `graph.py` - Only imports `collections.deque`
- `score_calculator.py` - Pure algorithm, no imports

### Level 1 (Depends on Level 0)
- `graph_builder.py` - Imports `graph.Graph`
- `tile_manager.py` - Receives `Graph` via composition
- `game_display.py` - Receives `Graph` via composition

### Level 2 (Depends on Level 1)
- `tile_swap_game.py` - Imports all Level 1 modules

### Level 3 (Entry point)
- `tile_swap.py` - Imports `tile_swap_game.TileSwapGame`

## Class Responsibilities

### Graph (graph.py)
**Responsibility:** Data structure
- Stores nodes and edges (adjacency list)
- Stores tile assignments
- Provides graph operations (neighbors, connectivity)

**Why separate:** Pure data structure, reusable in other projects

---

### TileManager (tile_manager.py)
**Responsibility:** Tile business logic
- Assign tiles (manual/random)
- Swap tiles
- Check solution state

**Why separate:** Separates tile logic from graph structure

---

### GraphBuilder (graph_builder.py)
**Responsibility:** Graph creation
- Manual entry
- File loading
- Random generation
- Validation (20-node cap, connectivity)

**Why separate:** Factory pattern, multiple creation methods

---

### GameDisplay (game_display.py)
**Responsibility:** Visualization and output
- Text graph structure
- Tile assignments
- Circular ASCII art
- Adjacency matrix
- Bresenham's line drawing

**Why separate:** Separates presentation from logic

---

### ScoreCalculator (score_calculator.py)
**Responsibility:** Scoring algorithm
- Calculate optimal moves
- Cycle decomposition algorithm

**Why separate:** Pure algorithm, no state, reusable

---

### TileSwapGame (tile_swap_game.py)
**Responsibility:** Game orchestration
- Coordinate all modules
- Manage game flow
- Handle user input
- Victory conditions

**Why separate:** Controller pattern, orchestrates other classes

---

### tile_swap.py (main entry)
**Responsibility:** Entry point only
- Create `TileSwapGame` instance
- Handle keyboard interrupt
- Start game

**Why separate:** Clean entry point, easy to import as module

## Communication Between Modules

### Direct Dependencies
```
TileSwapGame
    ├─> GraphBuilder.create_*() → returns Graph
    ├─> TileManager(graph)      → receives Graph
    ├─> GameDisplay(graph)      → receives Graph
    └─> ScoreCalculator.calculate_optimal_moves(tiles) → returns int
```

### Data Flow
```
1. GraphBuilder creates Graph
2. Graph passed to TileManager
3. Graph passed to GameDisplay
4. TileManager modifies Graph.tiles
5. GameDisplay reads Graph state
6. ScoreCalculator analyzes tile configuration
```

### No Circular Dependencies
- Clean one-way dependency flow
- Modules can be tested independently
- Easy to understand data flow

## Testing Each Module

### graph.py
```python
from graph import Graph

graph = Graph()
graph.add_edge(1, 2)
assert graph.has_node(1)
assert graph.are_connected(1, 2)
```

### tile_manager.py
```python
from graph import Graph
from tile_manager import TileManager

graph = Graph()
graph.add_edge(1, 2)
manager = TileManager(graph)
manager.assign_tiles({1: 2, 2: 1})
manager.swap_tiles(1, 2)
assert manager.is_solved()
```

### graph_builder.py
```python
from graph_builder import GraphBuilder

# Would need to mock input()
# Or test individual methods with test data
```

### game_display.py
```python
from graph import Graph
from game_display import GameDisplay

graph = Graph()
graph.add_edge(1, 2)
graph.tiles = {1: 2, 2: 1}
display = GameDisplay(graph)
display.display_visual_graph()
```

### score_calculator.py
```python
from score_calculator import ScoreCalculator

tiles = {1: 2, 2: 3, 3: 1}
optimal = ScoreCalculator.calculate_optimal_moves(tiles)
assert optimal == 2
```

### tile_swap_game.py
```python
from tile_swap_game import TileSwapGame

# Would need to mock user input
# Full integration test
```

## Advantages of This Structure

### 1. Single Responsibility
Each module does one thing well

### 2. Easy Testing
Test each module independently

### 3. Clear Interfaces
Well-defined methods between modules

### 4. Low Coupling
Modules don't know about each other's internals

### 5. High Cohesion
Related functionality grouped together

### 6. Reusability
Modules can be used in other projects

### 7. Maintainability
Changes isolated to specific modules

### 8. Scalability
Easy to add new features

## Adding New Features

### New Graph Creation Method
1. Add static method to `GraphBuilder`
2. No other files need changes

### New Display Mode
1. Add method to `GameDisplay`
2. Call from `TileSwapGame`

### New Scoring Algorithm
1. Add static method to `ScoreCalculator`
2. No other files need changes

### Save/Load Feature
1. Create new `game_state.py` module
2. Import in `TileSwapGame`
3. Other modules unchanged

## Summary

The modular structure provides:
- ✓ 7 focused modules instead of 1 monolithic file
- ✓ Clear separation of concerns
- ✓ No circular dependencies
- ✓ Easy to test
- ✓ Easy to extend
- ✓ Professional code organization
- ✓ Reusable components

Each module can be understood, tested, and modified independently!
