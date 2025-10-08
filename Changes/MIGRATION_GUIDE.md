# Migration Guide: graph_tile_game.py → tile_swap.py

## Quick Reference

| Original (Procedural) | New (OOP) | Notes |
|----------------------|-----------|-------|
| `graph_tile_game.py` | `tile_swap.py` | Main file renamed |
| `Graph` class | `Graph` class | Enhanced with helper methods |
| `create_graph_manually()` | `GraphBuilder.create_manually()` | Static method |
| `create_graph_from_file()` | `GraphBuilder.create_from_file()` | Static method |
| `create_random_graph()` | `GraphBuilder.create_random()` | Static method |
| `assign_tiles_manually()` | `TileManager.assign_tiles_manually()` | Instance method |
| `assign_tiles_randomly()` | `TileManager.assign_tiles_randomly()` | Instance method |
| `calculate_optimal_moves()` | `ScoreCalculator.calculate_optimal_moves()` | Static method |
| `play_game()` | `TileSwapGame.play()` | Instance method |
| `main()` | `TileSwapGame.run()` | Instance method |
| Graph display in `Graph` | `GameDisplay` class | Separated concern |

## Function → Class Method Mapping

### Graph Creation
```python
# OLD
graph = create_graph_manually()
graph = create_graph_from_file()
graph = create_random_graph()

# NEW
graph = GraphBuilder.create_manually()
graph = GraphBuilder.create_from_file()
graph = GraphBuilder.create_random()
```

### Tile Operations
```python
# OLD
assign_tiles_manually(graph)
assign_tiles_randomly(graph)

# NEW
tile_manager = TileManager(graph)
tile_manager.assign_tiles_manually()
tile_manager.assign_tiles_randomly()
```

### Display
```python
# OLD
graph.display_graph()
graph.display_tiles()
graph.display_graph_visual()

# NEW
display = GameDisplay(graph)
display.display_graph_structure()
display.display_tiles()
display.display_visual_graph()
```

### Scoring
```python
# OLD
optimal = calculate_optimal_moves(initial_tiles)

# NEW
optimal = ScoreCalculator.calculate_optimal_moves(initial_tiles)
```

### Game Loop
```python
# OLD
def main():
    while True:
        graph = create_graph_manually()
        # ... setup code
        play_game(graph, initial_tiles)

# NEW
game = TileSwapGame()
game.run()  # Handles entire game flow
```

## Key Improvements

### 1. Separation of Concerns

**Before:**
```python
# All mixed together
def play_game(graph, initial_tiles):
    graph.display_graph()      # Display mixed in
    move_count = 0             # State management
    optimal = calculate_optimal_moves()  # Calculation
    # ... game loop
```

**After:**
```python
# Clear separation
class TileSwapGame:
    def play(self):
        self.display.display_visual_graph()  # Separate class
        self.move_count = 0                   # Managed state
        self.optimal_moves = ScoreCalculator.calculate_optimal_moves()
```

### 2. Better Encapsulation

**Before:**
```python
# Direct manipulation
graph.tiles[node1], graph.tiles[node2] = graph.tiles[node2], graph.tiles[node1]
if graph.tiles[node] == node:
    # ...
```

**After:**
```python
# Through manager
tile_manager.swap_tiles(node1, node2)
if tile_manager.is_solved():
    # ...
```

### 3. Static Factory Pattern

**Before:**
```python
# Separate functions
def create_graph_manually():
    # ...
def create_graph_from_file():
    # ...
```

**After:**
```python
# Grouped in class
class GraphBuilder:
    @staticmethod
    def create_manually():
        # ...
    @staticmethod
    def create_from_file():
        # ...
```

## What Stayed the Same

✓ All game functionality
✓ Graph algorithms (BFS, Bresenham's)
✓ Cycle decomposition for optimal moves
✓ ASCII art visualization
✓ File format compatibility
✓ User interface flow
✓ Input validation

## What Changed

- **Structure**: Procedural → Object-Oriented
- **Organization**: Functions → Classes with methods
- **Naming**: "Graph Tile Game" → "Tile Swap"
- **Testability**: Hard to test → Easy to test
- **Extensibility**: Monolithic → Modular

## Example: Complete Game Flow

### Original (Procedural)
```python
def main():
    while True:
        graph = None

        # Step 1: Create graph
        choice = input("Choice: ")
        if choice == '1':
            graph = create_graph_manually()
        # ... more choices

        # Step 2: Assign tiles
        choice = input("Choice: ")
        if choice == '1':
            assign_tiles_manually(graph)
        # ... more choices

        initial_tiles = graph.tiles.copy()

        # Step 3: Play
        play_game(graph, initial_tiles)

        # Replay?
        if input("Play again? ") != 'y':
            break

if __name__ == "__main__":
    main()
```

### Refactored (OOP)
```python
class TileSwapGame:
    def run(self):
        while True:
            if not self.setup_graph():
                return
            if not self.setup_tiles():
                continue
            self.play()
            if input("Play again? ") != 'y':
                return

    def setup_graph(self):
        # ... uses GraphBuilder

    def setup_tiles(self):
        # ... uses TileManager

    def play(self):
        # ... uses GameDisplay

game = TileSwapGame()
game.run()
```

## Testing Examples

### Original (Hard to Test)
```python
# Can't easily test without full game context
# Functions depend on global state and I/O
```

### OOP (Easy to Test)
```python
# Test individual components
def test_tile_manager():
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    manager = TileManager(graph)
    manager.assign_tiles({1: 2, 2: 3, 3: 1})

    assert not manager.is_solved()
    manager.swap_tiles(1, 2)
    manager.swap_tiles(2, 3)
    assert manager.is_solved()
```

## Recommendations

### For Academic Submission
Use **tile_swap.py** - demonstrates:
- OOP mastery
- Design patterns
- Code organization
- Professional practices

### For Understanding Both Approaches
Compare:
1. Read `graph_tile_game.py` (procedural)
2. Read `tile_swap.py` (OOP)
3. See how same functionality is organized differently

### For Future Development
Build on **tile_swap.py**:
- Easy to add features
- Easy to modify
- Easy to test
- Easy to collaborate

## Summary

The migration from `graph_tile_game.py` to `tile_swap.py` transforms a functional procedural program into a professional, object-oriented application. Both work identically from a user perspective, but the OOP version is superior for maintenance, testing, and extension.

**Use tile_swap.py for**: Production, submission, portfolio
**Keep graph_tile_game.py for**: Reference, comparison, learning
