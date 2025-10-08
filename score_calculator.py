#!/usr/bin/env python3
"""
Score Calculator Module

Handles score and optimal solution calculations for Tile Swap.
"""


class ScoreCalculator:
    """Handles score and optimal solution calculations."""

    @staticmethod
    def calculate_optimal_moves(tile_configuration):
        """
        Calculate the minimum number of swaps needed to sort tiles.
        Uses cycle decomposition of the permutation.

        Args:
            tile_configuration: Dictionary mapping node -> tile number

        Returns:
            Minimum number of swaps needed
        """
        nodes = sorted(tile_configuration.keys())

        # Create a mapping of current position to target position
        current_positions = {}
        for node in nodes:
            tile = tile_configuration[node]
            current_positions[tile] = node

        visited = set()
        num_swaps = 0

        # Find cycles in the permutation
        for start_tile in nodes:
            if start_tile in visited:
                continue

            cycle_length = 0
            current_tile = start_tile

            while current_tile not in visited:
                visited.add(current_tile)
                cycle_length += 1
                current_position = current_positions[current_tile]
                current_tile = current_position

            # A cycle of length n requires n-1 swaps
            if cycle_length > 1:
                num_swaps += cycle_length - 1

        return num_swaps
