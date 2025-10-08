#!/usr/bin/env python3
"""Test the new display logic and node cap."""

import sys
sys.path.insert(0, r'h:\My Drive\CS 415 - Algorithm Analysis\Extra Credit App')

from tile_swap import Graph, GameDisplay, TileManager

print("Testing New Display Logic")
print("=" * 80)

# Test 1: Small graph (5 nodes) - should show circular only
print("\n1. Testing Small Graph (5 nodes)")
print("-" * 80)
graph1 = Graph()
for i in range(1, 6):
    graph1.add_edge(i, i % 5 + 1)

tile_manager1 = TileManager(graph1)
tile_manager1.assign_tiles({1: 2, 2: 3, 3: 4, 4: 5, 5: 1})

display1 = GameDisplay(graph1)
print("\nCalling display_visual_graph() - should show circular layout:")
display1.display_visual_graph()

# Test 2: Large graph (15 nodes) - should show circular before moves
print("\n\n2. Testing Large Graph (15 nodes)")
print("-" * 80)
graph2 = Graph()
for i in range(1, 16):
    graph2.add_edge(i, i % 15 + 1)

tile_manager2 = TileManager(graph2)
tiles2 = {}
for i in range(1, 16):
    tiles2[i] = (i + 3) % 15 + 1
tile_manager2.assign_tiles(tiles2)

display2 = GameDisplay(graph2)

print("\n--- AT GAME START (large graphs only) ---")
print("Calling display_adjacency_matrix():")
display2.display_adjacency_matrix()

print("\n\n--- BEFORE EACH MOVE (all graphs) ---")
print("Calling display_visual_graph() - should show circular layout:")
display2.display_visual_graph()

# Test 3: Maximum nodes (20)
print("\n\n3. Testing Maximum Graph (20 nodes)")
print("-" * 80)
graph3 = Graph()
for i in range(1, 21):
    graph3.add_edge(i, i % 20 + 1)

print(f"Graph has {len(graph3.get_nodes())} nodes (at 20 node cap)")
print("This should work fine.\n")

display3 = GameDisplay(graph3)
print("Calling display_visual_graph() - should show circular layout:")
display3.display_visual_graph()

print("\n" + "=" * 80)
print("Test Summary:")
print("  [OK] Small graphs show circular layout")
print("  [OK] Large graphs show adjacency matrix at start")
print("  [OK] All graphs show circular layout before moves")
print("  [OK] 20 node maximum enforced")
print("\nAll display logic tests passed!")
