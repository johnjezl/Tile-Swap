#!/usr/bin/env python3
"""
Tile Manager Module

Manages tile assignments and operations for Tile Swap.
"""

import random


class TileManager:
    """Manages tile assignments and operations."""

    def __init__(self, graph):
        self.graph = graph

    def assign_tiles(self, tile_assignment):
        """Assign tiles to nodes."""
        self.graph.tiles = tile_assignment.copy()

    def assign_tiles_manually(self):
        """Allow user to manually assign tiles to nodes."""
        print("\nManual Tile Assignment")
        print("Assign a tile number to each node.")

        nodes = self.graph.get_nodes()
        tile_assignment = {}
        available_tiles = set(nodes)

        for node in nodes:
            while True:
                tile_input = input(f"Assign tile to node {node} (available: {sorted(available_tiles)}): ").strip()

                if tile_input.lower() == 'q':
                    return False

                try:
                    tile = int(tile_input)
                    if tile not in available_tiles:
                        print(f"Tile {tile} is not available. Choose from {sorted(available_tiles)}")
                        continue

                    tile_assignment[node] = tile
                    available_tiles.remove(tile)
                    break

                except ValueError:
                    print("Invalid input. Please enter a tile number.")

        self.assign_tiles(tile_assignment)
        return True

    def assign_tiles_randomly(self):
        """Randomly assign tiles to nodes."""
        nodes = self.graph.get_nodes()
        tiles = nodes.copy()
        random.shuffle(tiles)

        tile_assignment = {}
        for i, node in enumerate(nodes):
            tile_assignment[node] = tiles[i]

        self.assign_tiles(tile_assignment)
        print("Tiles assigned randomly.")

    def swap_tiles(self, node1, node2):
        """Swap tiles between two nodes."""
        self.graph.tiles[node1], self.graph.tiles[node2] = self.graph.tiles[node2], self.graph.tiles[node1]

    def is_solved(self):
        """Check if all tiles match their node numbers."""
        for node in self.graph.get_nodes():
            if self.graph.tiles[node] != node:
                return False
        return True

    def get_initial_configuration(self):
        """Get a copy of the current tile configuration."""
        return self.graph.tiles.copy()
