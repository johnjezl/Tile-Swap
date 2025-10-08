#!/usr/bin/env python3
"""Test what displays for graphs with >10 nodes."""

import sys
sys.path.insert(0, r'h:\My Drive\CS 415 - Algorithm Analysis\Extra Credit App')

from tile_swap import Graph, GameDisplay, TileManager

print("Testing Graph Display for >10 Nodes")
print("=" * 80)

# Create a graph with 12 nodes
graph = Graph()
for i in range(1, 13):
    graph.add_edge(i, i % 12 + 1)

# Assign tiles
tiles = {}
for i in range(1, 13):
    tiles[i] = (i + 3) % 12 + 1

tile_manager = TileManager(graph)
tile_manager.assign_tiles(tiles)

print(f"\nGraph has {len(graph.get_nodes())} nodes (>10 threshold)")
print("\nCalling display_visual_graph():")
print("-" * 80)

display = GameDisplay(graph)
display.display_visual_graph()

print("\n" + "=" * 80)
print("Test complete!")
print("\nExpected: Adjacency matrix should be displayed above")
print("If you see it, the code is working correctly.")
print("If you don't, there may be a display issue.")
