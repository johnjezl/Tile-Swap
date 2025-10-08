# Tile Swap - Project Files Index

## Main Game Files

### Primary (Use This)
- **`tile_swap.py`** ⭐
  - Fully object-oriented implementation
  - 6 well-defined classes
  - ~650 lines of clean, maintainable code
  - **Run with**: `python tile_swap.py`

### Legacy (Original Version)
- **`graph_tile_game.py`**
  - Original procedural implementation
  - Functional but harder to maintain
  - Kept for reference and comparison

## Documentation Files

### Main Documentation
- **`TILE_SWAP_README.md`** ⭐
  - Complete game documentation
  - How to play
  - Features list
  - OOP architecture explanation
  - Example gameplay

### Technical Documentation
- **`OOP_REFACTORING_SUMMARY.md`** ⭐
  - Detailed refactoring documentation
  - Class responsibilities
  - Design principles applied
  - Benefits of OOP approach
  - Before/after comparison

- **`MIGRATION_GUIDE.md`**
  - Function → Method mapping
  - Code comparison examples
  - Testing improvements
  - Recommendations for use

- **`VISUALIZATION.md`**
  - Graph visualization feature details
  - Technical implementation
  - Algorithms used (Bresenham's)
  - Display methods

### Legacy Documentation
- **`README.md`**
  - Original game documentation
  - Still relevant for basic understanding

## Sample Data
- **`sample_graph.txt`**
  - Example graph file format
  - 4-node graph with 5 edges
  - Can be loaded via option 2 in game

## Test Files

### OOP Structure Tests
- **`test_oop_structure.py`** ⭐
  - Tests all 6 classes
  - Validates class interactions
  - Demonstrates OOP design
  - **Run with**: `python test_oop_structure.py`

### Visualization Tests
- **`test_visualization.py`**
  - Tests circular layout (small graphs)
  - Tests adjacency matrix (large graphs)
  - Shows different graph sizes
  - **Run with**: `python test_visualization.py`

- **`test_alignment.py`**
  - Tests 2-digit alignment in matrices
  - Validates formatting
  - **Run with**: `python test_alignment.py`

- **`test_game_flow.py`**
  - Demonstrates display timing
  - Shows game flow sequence
  - **Run with**: `python test_game_flow.py`

## Index Files
- **`FILES_INDEX.md`** (this file)
  - Complete file listing
  - Purpose of each file
  - Usage instructions

## Quick Start Guide

### To Play the Game
```bash
python tile_swap.py
```

### To Run All Tests
```bash
python test_oop_structure.py
python test_visualization.py
python test_alignment.py
python test_game_flow.py
```

### To Read Documentation
1. Start with: `TILE_SWAP_README.md`
2. For OOP details: `OOP_REFACTORING_SUMMARY.md`
3. For migration: `MIGRATION_GUIDE.md`

## File Organization

```
Extra Credit App/
│
├── Main Game (choose one)
│   ├── tile_swap.py ⭐           # New OOP version
│   └── graph_tile_game.py        # Original version
│
├── Documentation
│   ├── TILE_SWAP_README.md ⭐    # Main docs
│   ├── OOP_REFACTORING_SUMMARY.md ⭐
│   ├── MIGRATION_GUIDE.md
│   ├── VISUALIZATION.md
│   ├── README.md                 # Original docs
│   └── FILES_INDEX.md            # This file
│
├── Sample Data
│   └── sample_graph.txt
│
└── Tests
    ├── test_oop_structure.py ⭐
    ├── test_visualization.py
    ├── test_alignment.py
    └── test_game_flow.py
```

## File Sizes (Approximate)

| File | Lines | Description |
|------|-------|-------------|
| `tile_swap.py` | 650 | Main OOP game |
| `graph_tile_game.py` | 650 | Original procedural |
| `TILE_SWAP_README.md` | 200 | Main documentation |
| `OOP_REFACTORING_SUMMARY.md` | 300 | OOP details |
| `MIGRATION_GUIDE.md` | 250 | Migration guide |
| `test_oop_structure.py` | 85 | OOP tests |
| Other tests | ~50 each | Various test files |

## What to Submit

### For Academic Extra Credit
**Recommended package:**
1. `tile_swap.py` (main file)
2. `TILE_SWAP_README.md` (documentation)
3. `OOP_REFACTORING_SUMMARY.md` (technical details)
4. `sample_graph.txt` (example data)
5. `test_oop_structure.py` (demonstrates testing)

### For Portfolio
**Complete package:**
- All files (shows iteration and thoroughness)
- Emphasize OOP version in description
- Reference documentation quality

### For Quick Demo
**Minimal package:**
1. `tile_swap.py`
2. `TILE_SWAP_README.md`
3. `sample_graph.txt`

## Version History

### v2.0 - Object-Oriented Refactor
- Full OOP restructure
- Renamed to "Tile Swap"
- 6 distinct classes
- Professional-grade code
- Comprehensive documentation

### v1.0 - Original Release
- Procedural implementation
- "Graph Tile Game" name
- All core features working
- Basic documentation

## Notes

- ⭐ = Recommended/Primary files
- Both game versions have identical functionality
- OOP version is superior for maintenance and extension
- All test files pass successfully
- Documentation is comprehensive and professional

## Contact/Credits

Game designed for CS 415 - Algorithm Analysis
Implementation demonstrates:
- Graph theory concepts
- Algorithm design (BFS, cycle decomposition, Bresenham's)
- Object-oriented programming
- Software engineering best practices
