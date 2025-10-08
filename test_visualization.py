#!/usr/bin/env python3
"""Quick test of the graph visualization."""

import sys
sys.path.insert(0, r'h:\My Drive\CS 415 - Algorithm Analysis\Extra Credit App')

from graph_tile_game import Graph

# Create a simple test graph
print("Testing Graph Visualization")
print("=" * 60)

# Test 1: Small graph (4 nodes)
print("\nTest 1: Small Graph (4 nodes)")
graph = Graph()
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 1)
graph.add_edge(1, 3)

# Assign tiles
graph.tiles = {1: 3, 2: 1, 3: 4, 4: 2}

graph.display_graph_visual()

# Test 2: Smaller graph (3 nodes)
print("\n\nTest 2: Triangle Graph (3 nodes)")
graph2 = Graph()
graph2.add_edge(1, 2)
graph2.add_edge(2, 3)
graph2.add_edge(3, 1)

graph2.tiles = {1: 2, 2: 3, 3: 1}

graph2.display_graph_visual()

# Test 3: Larger graph (6 nodes)
print("\n\nTest 3: Hexagon Graph (6 nodes)")
graph3 = Graph()
for i in range(1, 7):
    graph3.add_edge(i, i % 6 + 1)

graph3.tiles = {1: 4, 2: 5, 3: 6, 4: 1, 5: 2, 6: 3}

graph3.display_graph_visual()

# Test 4: Large graph (15 nodes) - should use adjacency matrix
print("\n\nTest 4: Large Graph (15 nodes) - Adjacency Matrix")
graph4 = Graph()
for i in range(1, 16):
    graph4.add_edge(i, i % 15 + 1)
    if i % 3 == 0:
        graph4.add_edge(i, (i + 5) % 15 + 1)

graph4.tiles = {i: (i + 3) % 15 + 1 for i in range(1, 16)}

graph4.display_graph_visual()

print("\n\nVisualization tests complete!")
