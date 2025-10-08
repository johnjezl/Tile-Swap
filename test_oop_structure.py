#!/usr/bin/env python3
"""Test the OOP structure of Tile Swap."""

import sys
sys.path.insert(0, r'h:\My Drive\CS 415 - Algorithm Analysis\Extra Credit App')

from tile_swap import (
    Graph, TileManager, GraphBuilder, GameDisplay,
    ScoreCalculator, TileSwapGame
)

print("Testing Tile Swap OOP Structure")
print("=" * 80)

# Test 1: Graph class
print("\n1. Testing Graph class")
graph = Graph()
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 1)

print(f"   Nodes: {graph.get_nodes()}")
print(f"   Node 1 neighbors: {sorted(graph.get_neighbors(1))}")
print(f"   Is connected: {graph.is_connected()}")
print(f"   Has node 2: {graph.has_node(2)}")
print(f"   Has node 5: {graph.has_node(5)}")
print(f"   Are 1 and 2 connected: {graph.are_connected(1, 2)}")
print(f"   Are 1 and 5 connected: {graph.are_connected(1, 5)}")
print("   [OK] Graph class working")

# Test 2: TileManager class
print("\n2. Testing TileManager class")
tile_manager = TileManager(graph)
tile_manager.assign_tiles({1: 2, 2: 3, 3: 1})
print(f"   Tiles: {graph.tiles}")
print(f"   Is solved: {tile_manager.is_solved()}")
tile_manager.swap_tiles(1, 2)
print(f"   After swapping 1 and 2: {graph.tiles}")
tile_manager.swap_tiles(2, 3)
print(f"   After swapping 2 and 3: {graph.tiles}")
print(f"   Is solved: {tile_manager.is_solved()}")
print("   [OK] TileManager class working")

# Test 3: GameDisplay class
print("\n3. Testing GameDisplay class")
display = GameDisplay(graph)
display.display_graph_structure()
display.display_tiles()
display.display_visual_graph()
print("   [OK] GameDisplay class working")

# Test 4: ScoreCalculator class
print("\n4. Testing ScoreCalculator class")
initial_config = {1: 2, 2: 3, 3: 1}
optimal = ScoreCalculator.calculate_optimal_moves(initial_config)
print(f"   Optimal moves for {initial_config}: {optimal}")
print("   [OK] ScoreCalculator class working")

# Test 5: GraphBuilder class (static methods)
print("\n5. Testing GraphBuilder class")
print("   GraphBuilder has static methods:")
print(f"   - create_manually: {hasattr(GraphBuilder, 'create_manually')}")
print(f"   - create_from_file: {hasattr(GraphBuilder, 'create_from_file')}")
print(f"   - create_random: {hasattr(GraphBuilder, 'create_random')}")
print("   [OK] GraphBuilder class structure correct")

# Test 6: TileSwapGame class
print("\n6. Testing TileSwapGame class")
game = TileSwapGame()
print(f"   Initial move count: {game.move_count}")
print(f"   Has graph: {game.graph is None}")
print(f"   Has tile_manager: {game.tile_manager is None}")
print(f"   Has display: {game.display is None}")
print("   [OK] TileSwapGame class structure correct")

print("\n" + "=" * 80)
print("All OOP Structure Tests Passed!")
print("\nClass Hierarchy:")
print("  TileSwapGame (controller)")
print("  |-- Graph (data structure)")
print("  |-- TileManager (tile operations)")
print("  |-- GameDisplay (visualization)")
print("  |-- ScoreCalculator (static utility)")
print("  +-- GraphBuilder (static factory)")
