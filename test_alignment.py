#!/usr/bin/env python3
"""Test adjacency matrix alignment with 2-digit formatting."""

import sys
sys.path.insert(0, r'h:\My Drive\CS 415 - Algorithm Analysis\Extra Credit App')

from graph_tile_game import Graph

# Test large graph to see adjacency matrix
print("Testing Adjacency Matrix Alignment (2-digit formatting)")
print("=" * 80)

graph = Graph()

# Create a graph with nodes 1-15 to test alignment
for i in range(1, 16):
    graph.add_edge(i, i % 15 + 1)
    if i % 3 == 0:
        graph.add_edge(i, (i + 5) % 15 + 1)

# Assign tiles - some single digit, some double digit
graph.tiles = {}
for i in range(1, 16):
    graph.tiles[i] = (i + 7) % 15 + 1

graph.display_graph_visual()

print("\n\nAlignment Test Complete!")
print("All node and tile numbers should align vertically in columns.")
