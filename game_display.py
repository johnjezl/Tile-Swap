#!/usr/bin/env python3
"""
Game Display Module

Handles all game display and visualization for Tile Swap.
"""

import math


class GameDisplay:
    """Handles all game display and visualization."""

    def __init__(self, graph):
        self.graph = graph

    def display_graph_structure(self):
        """Display the graph structure as text."""
        print("\nGraph Structure:")
        for node in self.graph.get_nodes():
            neighbors = sorted(self.graph.get_neighbors(node))
            print(f"  Node {node}: connected to {neighbors}")

    def display_tiles(self):
        """Display current tile assignments."""
        print("\nCurrent Tile Assignments:")
        for node in self.graph.get_nodes():
            tile = self.graph.tiles.get(node, '?')
            match = "✓" if tile == node else " "
            print(f"  Node {node}: Tile {tile} {match}")

    def display_visual_graph(self):
        """Display a visual representation of the graph with tiles (circular layout)."""
        nodes = self.graph.get_nodes()
        num_nodes = len(nodes)

        if num_nodes == 0:
            return

        # Always show circular layout
        self._display_circular_layout()

    def display_adjacency_matrix(self):
        """Display adjacency matrix (for reference at game start)."""
        self._display_adjacency_matrix()

    def _display_circular_layout(self):
        """Display small graphs using ASCII art in a circular layout."""
        nodes = self.graph.get_nodes()
        num_nodes = len(nodes)

        print("\nVisual Graph Representation:")
        print("=" * 60)

        radius = max(8, num_nodes * 2)
        center_x = radius + 5
        center_y = radius + 5

        # Calculate positions for each node
        node_positions = {}
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / num_nodes - math.pi / 2
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            node_positions[node] = (x, y)

        # Create a 2D grid for drawing
        grid_size = 2 * radius + 10
        grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

        # Draw edges first
        for node in nodes:
            x1, y1 = node_positions[node]
            for neighbor in self.graph.get_neighbors(node):
                if neighbor > node:
                    x2, y2 = node_positions[neighbor]
                    self._draw_line(grid, x1, y1, x2, y2)

        # Draw nodes on top of edges
        for node in nodes:
            x, y = node_positions[node]
            tile = self.graph.tiles.get(node, '?')
            match = '=' if tile == node else '!'

            node_str = f"[{node}:{tile}{match}]"

            start_x = x - len(node_str) // 2
            for i, char in enumerate(node_str):
                if 0 <= start_x + i < grid_size and 0 <= y < grid_size:
                    grid[y][start_x + i] = char

        # Print the grid
        for row in grid:
            print(''.join(row))

        print("=" * 60)
        print("Legend: [Node:Tile=] (= means matched, ! means not matched)")

    def _draw_line(self, grid, x1, y1, x2, y2):
        """Draw a line on the grid using Bresenham's algorithm."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= x1 < len(grid[0]) and 0 <= y1 < len(grid):
                if grid[y1][x1] == ' ':
                    if abs(dx) > abs(dy):
                        grid[y1][x1] = '-'
                    elif abs(dy) > abs(dx):
                        grid[y1][x1] = '|'
                    else:
                        grid[y1][x1] = '\\'

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def _display_adjacency_matrix(self):
        """Display adjacency matrix for larger graphs."""
        nodes = self.graph.get_nodes()

        print("\nAdjacency Matrix with Tiles:")
        print("=" * 80)

        # Header - fixed width for alignment
        print("       ", end="")
        for node in nodes:
            tile = self.graph.tiles.get(node, '?')
            match = '=' if tile == node else '!'
            print(f"{node:2d}:{tile:2} {match} ", end="")
        print()

        # Matrix
        for node1 in nodes:
            tile1 = self.graph.tiles.get(node1, '?')
            match1 = '=' if tile1 == node1 else '!'
            print(f"{node1:2d}:{tile1:2} {match1}  ", end="")

            for node2 in nodes:
                if node1 == node2:
                    print("  ·   ", end="")
                elif node2 in self.graph.get_neighbors(node1):
                    print("  1   ", end="")
                else:
                    print("  0   ", end="")
            print()

        print("=" * 80)
        print("Legend: Node:Tile= (= matched, ! not matched), 1=connected, 0=not connected")
