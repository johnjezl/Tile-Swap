#!/usr/bin/env python3
"""Test that adjacency matrix displays after tile assignment."""

import sys
sys.path.insert(0, r'h:\My Drive\CS 415 - Algorithm Analysis\Extra Credit App')

from graph import Graph
from tile_manager import TileManager
from game_display import GameDisplay
from score_calculator import ScoreCalculator

print("Testing Adjacency Matrix Display After Tile Assignment")
print("=" * 80)

# Create a small graph
graph = Graph()
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 1)
graph.add_edge(1, 3)

tile_manager = TileManager(graph)
display = GameDisplay(graph)

print("\nStep 1: Graph created (5 edges, 4 nodes)")
print("\nStep 2: Assigning tiles randomly...")
tile_manager.assign_tiles_randomly()

print("\nStep 3: Displaying adjacency matrix...")
print("=" * 50)
print("TILE ASSIGNMENT COMPLETE")
print("=" * 50)
display.display_adjacency_matrix()

print("\n" + "=" * 80)
print("Test Complete!")
print("\nThe adjacency matrix is now shown after tile assignment,")
print("giving the player a reference before gameplay begins.")
