# Graph Visualization Feature

## Overview

The game now includes **text-based graph visualization** using only Python standard libraries (`math` for trigonometry calculations).

## Visualization Methods

### 1. Small Graphs (≤10 nodes)
- **Layout**: Circular arrangement with ASCII art connecting lines
- **Algorithm**: Bresenham's line algorithm for drawing edges
- **Display Format**: `[Node:Tile!]` where `!` means not matched, `=` means matched
- **Features**:
  - Nodes arranged in a circle for clear visibility
  - Lines drawn using `-`, `|`, and `\` characters
  - Real-time tile status updates

### 2. Large Graphs (>10 nodes)
- **Layout**: Adjacency matrix representation
- **Display Format**: Shows connections with `1` (connected) and `0` (not connected)
- **Features**:
  - Compact representation for many nodes
  - Shows tile assignments alongside matrix
  - Easy to verify connectivity

## Technical Implementation

### Standard Libraries Used
- `math`: For circular layout calculations (sin, cos, pi)
- No external dependencies required!

### Key Algorithms
1. **Circular Layout**: Nodes positioned using polar coordinates
2. **Bresenham's Line Algorithm**: Efficient line drawing on a character grid
3. **Collision Detection**: Prevents edge characters from overwriting node labels

## Example Outputs

### Triangle (3 nodes)
```
          [1:2!]
            ||
           |  |
          |    |
   [3:1!]-------[2:3!]
```

### Square with Diagonal (4 nodes)
```
          [1:3!]
            \|\
           \ | \
  [4:2!]     |    [2:1!]
           \ | \
            \|\
          [3:4!]
```

### Large Graph (15+ nodes)
Shows adjacency matrix with tile positions for easy reference.

## Benefits

1. **Visual Learning**: See graph structure at a glance
2. **Game Strategy**: Understand which swaps are possible
3. **Progress Tracking**: Watch tiles match up (! → =)
4. **No Dependencies**: Works everywhere Python runs
5. **Cross-Platform**: ASCII characters work on Windows, Mac, Linux

## Integration

The visualization is automatically called:
- At game start (shows initial state)
- After each tile swap (shows updated state)
- Uses appropriate method based on graph size

## Code Structure

```python
display_graph_visual()           # Main entry point
├── _display_small_graph()       # For ≤10 nodes
│   ├── Calculate positions
│   ├── Create 2D grid
│   ├── _draw_line()            # Bresenham's algorithm
│   └── Place nodes
└── _display_adjacency_matrix()  # For >10 nodes
```

All visualization code is in the `Graph` class in [graph_tile_game.py](graph_tile_game.py).
