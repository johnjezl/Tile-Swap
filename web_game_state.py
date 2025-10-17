#!/usr/bin/env python3
"""
Web Game State Manager

Manages game state for the web interface, providing a clean API
for the Flask application to interact with the game logic.
"""

from graph import Graph
from graph_builder import GraphBuilder
from tile_manager import TileManager
from score_calculator import ScoreCalculator
import math


class WebGameState:
    """Manages game state for web interface."""

    def __init__(self):
        self.graph = None
        self.tile_manager = None
        self.move_count = 0
        self.initial_tiles = None
        self.optimal_moves = 0
        self.game_active = False

    def create_random_graph(self, num_nodes=6, num_edges=None):
        """Create a random connected graph."""
        if num_edges is None:
            min_edges = num_nodes - 1
            max_edges = num_nodes * (num_nodes - 1) // 2
            # Default to a moderately connected graph
            num_edges = min(min_edges + num_nodes, max_edges)

        self.graph = GraphBuilder.create_random_with_params(num_nodes, num_edges)
        self.tile_manager = TileManager(self.graph)
        return self.graph is not None

    def create_graph_from_edges(self, edges):
        """
        Create a graph from a list of edge tuples.

        Args:
            edges: List of tuples [(node1, node2), ...]

        Returns:
            True if successful, False otherwise
        """
        if not edges:
            return False

        self.graph = Graph()
        for node1, node2 in edges:
            if node1 != node2 and node1 > 0 and node2 > 0:
                self.graph.add_edge(node1, node2)

        if not self.graph.is_connected():
            return False

        self.tile_manager = TileManager(self.graph)
        return True

    def assign_tiles_randomly(self):
        """Randomly assign tiles and start the game."""
        if not self.tile_manager:
            return False

        self.tile_manager.assign_tiles_randomly()

        # Make sure not already solved
        if self.tile_manager.is_solved():
            self.tile_manager.assign_tiles_randomly()

        self.initial_tiles = self.tile_manager.get_initial_configuration()
        self.optimal_moves = ScoreCalculator.calculate_optimal_moves(self.initial_tiles)
        self.move_count = 0
        self.game_active = True
        return True

    def swap_tiles(self, node1, node2):
        """
        Attempt to swap tiles between two nodes.

        Returns:
            dict with 'success' boolean and optional 'message' string
        """
        if not self.game_active:
            return {'success': False, 'message': 'Game not active'}

        if not self.graph.has_node(node1) or not self.graph.has_node(node2):
            return {'success': False, 'message': 'Invalid nodes'}

        if not self.graph.are_connected(node1, node2):
            return {'success': False, 'message': 'Nodes are not connected'}

        self.tile_manager.swap_tiles(node1, node2)
        self.move_count += 1

        result = {
            'success': True,
            'move_count': self.move_count,
            'solved': self.tile_manager.is_solved()
        }

        if result['solved']:
            self.game_active = False
            result['optimal_moves'] = self.optimal_moves

        return result

    def get_game_state(self):
        """
        Get current game state as a dictionary for JSON serialization.

        Returns:
            dict with graph structure, tiles, and game status
        """
        if not self.graph:
            return {'active': False}

        # Build node positions for visualization (circular layout)
        nodes = self.graph.get_nodes()
        num_nodes = len(nodes)
        node_positions = {}

        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / num_nodes - math.pi / 2
            x = 0.5 + 0.4 * math.cos(angle)  # Normalized to [0.1, 0.9]
            y = 0.5 + 0.4 * math.sin(angle)
            node_positions[str(node)] = {'x': x, 'y': y}

        # Build edge list
        edges = []
        for node in nodes:
            for neighbor in self.graph.get_neighbors(node):
                if node < neighbor:  # Only add each edge once
                    edges.append([node, neighbor])

        # Build tile information
        tiles = {}
        for node in nodes:
            tile = self.graph.tiles.get(node, node)
            tiles[str(node)] = {
                'tile': tile,
                'matched': tile == node
            }

        return {
            'active': self.game_active,
            'nodes': nodes,
            'edges': edges,
            'node_positions': node_positions,
            'tiles': tiles,
            'move_count': self.move_count,
            'optimal_moves': self.optimal_moves
        }

    def reset_game(self):
        """Reset the game state."""
        self.graph = None
        self.tile_manager = None
        self.move_count = 0
        self.initial_tiles = None
        self.optimal_moves = 0
        self.game_active = False
