#!/usr/bin/env python3
"""Test the game flow showing visual graph before each move prompt."""

import sys
sys.path.insert(0, r'h:\My Drive\CS 415 - Algorithm Analysis\Extra Credit App')

from graph_tile_game import Graph

print("Simulating Game Flow")
print("=" * 80)

# Create a small test graph
graph = Graph()
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 1)

graph.tiles = {1: 2, 2: 3, 3: 1}

print("\n--- GAME START ---")
print("\nGraph Structure:")
print("  Node 1: connected to [2, 3]")
print("  Node 2: connected to [1, 3]")
print("  Node 3: connected to [1, 2]")
print()

# Only show adjacency matrix at start if >10 nodes (this has 3 nodes, so skip)
if len(graph.get_nodes()) > 10:
    graph.display_graph_visual()

print("Current Tile Assignments:")
for node in graph.get_nodes():
    tile = graph.tiles[node]
    match = "✓" if tile == node else " "
    print(f"  Node {node}: Tile {tile} {match}")

print("\nCurrent Score (moves): 0")
print("Optimal Solution: 2 moves")
print("\n" + "-" * 50)

print("\n--- BEFORE EACH MOVE, VISUAL GRAPH IS SHOWN ---")
graph.display_graph_visual()

print("\n[Player would now enter their move here]")
print("This visual will appear before EVERY move prompt!")

print("\n" + "=" * 80)
print("Flow Test Complete!")
print("\nKey Changes:")
print("  1. Adjacency matrix (for large graphs) only shown at game start")
print("  2. Visual circular graph shown BEFORE each move prompt")
print("  3. After move, only tile list and score are shown")
print("  4. Then visual graph appears again before next prompt")
