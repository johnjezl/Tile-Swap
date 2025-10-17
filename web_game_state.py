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
    """Manages game state for web interface with enhanced features."""

    def __init__(self):
        self.graph = None
        self.tile_manager = None
        self.move_count = 0
        self.initial_tiles = None
        self.optimal_moves = 0
        self.game_active = False
        self.move_history = []  # For undo/redo: list of (node1, node2) tuples
        self.redo_stack = []    # For redo functionality

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

        # Record move for undo
        self.move_history.append((node1, node2))
        # Clear redo stack when new move is made
        self.redo_stack = []

        self.tile_manager.swap_tiles(node1, node2)
        self.move_count += 1

        result = {
            'success': True,
            'move_count': self.move_count,
            'solved': self.tile_manager.is_solved(),
            'can_undo': len(self.move_history) > 0,
            'can_redo': len(self.redo_stack) > 0
        }

        if result['solved']:
            self.game_active = False
            result['optimal_moves'] = self.optimal_moves

        return result

    def undo_move(self):
        """
        Undo the last move.

        Returns:
            dict with 'success' boolean and updated state
        """
        if not self.move_history:
            return {'success': False, 'message': 'No moves to undo'}

        # Get last move and remove from history
        node1, node2 = self.move_history.pop()
        # Add to redo stack
        self.redo_stack.append((node1, node2))

        # Swap back
        self.tile_manager.swap_tiles(node1, node2)
        self.move_count = max(0, self.move_count - 1)

        return {
            'success': True,
            'move_count': self.move_count,
            'can_undo': len(self.move_history) > 0,
            'can_redo': len(self.redo_stack) > 0
        }

    def redo_move(self):
        """
        Redo a previously undone move.

        Returns:
            dict with 'success' boolean and updated state
        """
        if not self.redo_stack:
            return {'success': False, 'message': 'No moves to redo'}

        # Get move from redo stack
        node1, node2 = self.redo_stack.pop()
        # Add back to history
        self.move_history.append((node1, node2))

        # Swap tiles
        self.tile_manager.swap_tiles(node1, node2)
        self.move_count += 1

        result = {
            'success': True,
            'move_count': self.move_count,
            'solved': self.tile_manager.is_solved(),
            'can_undo': len(self.move_history) > 0,
            'can_redo': len(self.redo_stack) > 0
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
            'optimal_moves': self.optimal_moves,
            'can_undo': len(self.move_history) > 0,
            'can_redo': len(self.redo_stack) > 0
        }

    def save_game(self):
        """
        Export current game state for saving.

        Returns:
            dict with complete game state
        """
        if not self.graph:
            return None

        nodes = self.graph.get_nodes()
        edges = []
        for node in nodes:
            for neighbor in self.graph.get_neighbors(node):
                if node < neighbor:
                    edges.append([node, neighbor])

        return {
            'version': '1.0',
            'edges': edges,
            'tiles': {str(k): v for k, v in self.graph.tiles.items()},
            'initial_tiles': {str(k): v for k, v in self.initial_tiles.items()} if self.initial_tiles else {},
            'move_count': self.move_count,
            'optimal_moves': self.optimal_moves,
            'game_active': self.game_active,
            'move_history': self.move_history,
            'redo_stack': self.redo_stack
        }

    def load_game(self, save_data):
        """
        Restore game state from saved data.

        Args:
            save_data: dict from save_game()

        Returns:
            True if successful, False otherwise
        """
        try:
            # Recreate graph
            edges = [(e[0], e[1]) for e in save_data['edges']]
            if not self.create_graph_from_edges(edges):
                return False

            # Restore tiles
            tiles = {int(k): v for k, v in save_data['tiles'].items()}
            self.tile_manager.assign_tiles(tiles)

            # Restore game state
            self.initial_tiles = {int(k): v for k, v in save_data['initial_tiles'].items()}
            self.move_count = save_data['move_count']
            self.optimal_moves = save_data['optimal_moves']
            self.game_active = save_data['game_active']
            self.move_history = save_data.get('move_history', [])
            self.redo_stack = save_data.get('redo_stack', [])

            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    def reset_game(self):
        """Reset the game state."""
        self.graph = None
        self.tile_manager = None
        self.move_count = 0
        self.initial_tiles = None
        self.optimal_moves = 0
        self.game_active = False
        self.move_history = []
        self.redo_stack = []
