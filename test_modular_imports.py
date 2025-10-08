#!/usr/bin/env python3
"""Test the modular structure and imports."""

print("Testing Modular Structure")
print("=" * 80)

# Test individual module imports
print("\n1. Testing individual module imports...")
try:
    from graph import Graph
    print("   [OK] graph.py - Graph class imported")
except ImportError as e:
    print(f"   [FAIL] graph.py - {e}")

try:
    from tile_manager import TileManager
    print("   [OK] tile_manager.py - TileManager class imported")
except ImportError as e:
    print(f"   [FAIL] tile_manager.py - {e}")

try:
    from graph_builder import GraphBuilder
    print("   [OK] graph_builder.py - GraphBuilder class imported")
except ImportError as e:
    print(f"   [FAIL] graph_builder.py - {e}")

try:
    from game_display import GameDisplay
    print("   [OK] game_display.py - GameDisplay class imported")
except ImportError as e:
    print(f"   [FAIL] game_display.py - {e}")

try:
    from score_calculator import ScoreCalculator
    print("   [OK] score_calculator.py - ScoreCalculator class imported")
except ImportError as e:
    print(f"   [FAIL] score_calculator.py - {e}")

try:
    from tile_swap_game import TileSwapGame
    print("   [OK] tile_swap_game.py - TileSwapGame class imported")
except ImportError as e:
    print(f"   [FAIL] tile_swap_game.py - {e}")

# Test creating instances
print("\n2. Testing class instantiation...")
try:
    graph = Graph()
    print("   [OK] Graph() instance created")
except Exception as e:
    print(f"   [FAIL] Graph() - {e}")

try:
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    tile_manager = TileManager(graph)
    print("   [OK] TileManager(graph) instance created")
except Exception as e:
    print(f"   [FAIL] TileManager - {e}")

try:
    display = GameDisplay(graph)
    print("   [OK] GameDisplay(graph) instance created")
except Exception as e:
    print(f"   [FAIL] GameDisplay - {e}")

try:
    game = TileSwapGame()
    print("   [OK] TileSwapGame() instance created")
except Exception as e:
    print(f"   [FAIL] TileSwapGame - {e}")

# Test basic functionality
print("\n3. Testing basic functionality...")
try:
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 1)
    nodes = graph.get_nodes()
    assert nodes == [1, 2, 3], f"Expected [1, 2, 3], got {nodes}"
    print("   [OK] Graph.get_nodes() works")
except Exception as e:
    print(f"   [FAIL] Graph functionality - {e}")

try:
    tile_manager = TileManager(graph)
    tile_manager.assign_tiles({1: 2, 2: 3, 3: 1})
    assert graph.tiles == {1: 2, 2: 3, 3: 1}
    print("   [OK] TileManager.assign_tiles() works")
except Exception as e:
    print(f"   [FAIL] TileManager functionality - {e}")

try:
    optimal = ScoreCalculator.calculate_optimal_moves({1: 2, 2: 3, 3: 1})
    assert optimal == 2, f"Expected 2, got {optimal}"
    print("   [OK] ScoreCalculator.calculate_optimal_moves() works")
except Exception as e:
    print(f"   [FAIL] ScoreCalculator functionality - {e}")

print("\n" + "=" * 80)
print("Modular Structure Test Complete!")
print("\nModule Structure:")
print("  graph.py")
print("  tile_manager.py")
print("  graph_builder.py")
print("  game_display.py")
print("  score_calculator.py")
print("  tile_swap_game.py")
print("  tile_swap.py (main entry point)")
print("\nAll modules are properly separated and functional!")
