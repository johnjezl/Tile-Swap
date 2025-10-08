#!/usr/bin/env python3
"""
Graph Tile Puzzle Game

A puzzle game where players create a connected graph and swap tiles between
connected nodes until all tiles match their corresponding node numbers.
"""

import random
import sys
from collections import deque


class Graph:
    """Represents an undirected connected graph."""

    def __init__(self):
        self.adjacency_list = {}
        self.tiles = {}

    def add_edge(self, node1, node2):
        """Add an edge between two nodes."""
        if node1 not in self.adjacency_list:
            self.adjacency_list[node1] = set()
        if node2 not in self.adjacency_list:
            self.adjacency_list[node2] = set()

        self.adjacency_list[node1].add(node2)
        self.adjacency_list[node2].add(node1)

    def get_nodes(self):
        """Return sorted list of all nodes."""
        return sorted(self.adjacency_list.keys())

    def get_neighbors(self, node):
        """Return the neighbors of a node."""
        return self.adjacency_list.get(node, set())

    def is_connected(self):
        """Check if the graph is connected using BFS."""
        if not self.adjacency_list:
            return False

        nodes = list(self.adjacency_list.keys())
        start_node = nodes[0]
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)

        while queue:
            current = queue.popleft()
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == len(nodes)

    def assign_tiles(self, tile_assignment):
        """Assign tiles to nodes."""
        self.tiles = tile_assignment.copy()

    def swap_tiles(self, node1, node2):
        """Swap tiles between two nodes."""
        self.tiles[node1], self.tiles[node2] = self.tiles[node2], self.tiles[node1]

    def is_solved(self):
        """Check if all tiles match their node numbers."""
        for node in self.get_nodes():
            if self.tiles[node] != node:
                return False
        return True

    def display_graph(self):
        """Display the graph structure."""
        print("\nGraph Structure:")
        for node in self.get_nodes():
            neighbors = sorted(self.get_neighbors(node))
            print(f"  Node {node}: connected to {neighbors}")

    def display_graph_visual(self):
        """Display a visual representation of the graph with tiles."""
        nodes = self.get_nodes()
        num_nodes = len(nodes)

        if num_nodes == 0:
            return

        # For small graphs (<=10 nodes), create a nice visual layout
        if num_nodes <= 10:
            self._display_small_graph()
        else:
            # For larger graphs, use adjacency matrix
            self._display_adjacency_matrix()

    def _display_small_graph(self):
        """Display small graphs using ASCII art in a circular layout."""
        nodes = self.get_nodes()
        num_nodes = len(nodes)

        print("\nVisual Graph Representation:")
        print("=" * 60)

        # Arrange nodes in a circular pattern for nice visualization
        import math

        radius = max(8, num_nodes * 2)
        center_x = radius + 5
        center_y = radius + 5

        # Calculate positions for each node
        node_positions = {}
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / num_nodes - math.pi / 2  # Start from top
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            node_positions[node] = (x, y)

        # Create a 2D grid for drawing
        grid_size = 2 * radius + 10
        grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

        # Draw edges first
        for node in nodes:
            x1, y1 = node_positions[node]
            for neighbor in self.get_neighbors(node):
                if neighbor > node:  # Draw each edge only once
                    x2, y2 = node_positions[neighbor]
                    self._draw_line(grid, x1, y1, x2, y2)

        # Draw nodes on top of edges
        for node in nodes:
            x, y = node_positions[node]
            tile = self.tiles.get(node, '?')
            match = '=' if tile == node else '!'

            # Node representation: [N:T] where N=node, T=tile
            node_str = f"[{node}:{tile}{match}]"

            # Place the node string
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
            # Don't overwrite nodes (characters other than space)
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
        nodes = self.get_nodes()

        print("\nAdjacency Matrix with Tiles:")
        print("=" * 80)

        # Header - fixed width for alignment
        print("       ", end="")
        for node in nodes:
            tile = self.tiles.get(node, '?')
            match = '=' if tile == node else '!'
            print(f"{node:2d}:{tile:2} {match} ", end="")
        print()

        # Matrix
        for node1 in nodes:
            tile1 = self.tiles.get(node1, '?')
            match1 = '=' if tile1 == node1 else '!'
            print(f"{node1:2d}:{tile1:2} {match1}  ", end="")

            for node2 in nodes:
                if node1 == node2:
                    print("  ·   ", end="")
                elif node2 in self.get_neighbors(node1):
                    print("  1   ", end="")
                else:
                    print("  0   ", end="")
            print()

        print("=" * 80)
        print("Legend: Node:Tile= (= matched, ! not matched), 1=connected, 0=not connected")

    def display_tiles(self):
        """Display current tile assignments."""
        print("\nCurrent Tile Assignments:")
        for node in self.get_nodes():
            tile = self.tiles.get(node, '?')
            match = "✓" if tile == node else " "
            print(f"  Node {node}: Tile {tile} {match}")


def create_graph_manually():
    """Allow user to create a graph by entering edges manually."""
    print("\nEnter edges in the format: node1 node2")
    print("Enter 'done' when finished.")

    graph = Graph()

    while True:
        user_input = input("Edge (node1 node2) or 'done': ").strip()

        if user_input.lower() == 'q':
            return None

        if user_input.lower() == 'done':
            break

        parts = user_input.split()
        if len(parts) != 2:
            print("Invalid format. Please enter two node numbers separated by space.")
            continue

        try:
            node1 = int(parts[0])
            node2 = int(parts[1])

            if node1 < 1 or node2 < 1:
                print("Node numbers must be positive integers.")
                continue

            if node1 == node2:
                print("Cannot create a self-loop.")
                continue

            graph.add_edge(node1, node2)
            print(f"Added edge: {node1} - {node2}")

        except ValueError:
            print("Invalid input. Please enter integers.")

    if not graph.adjacency_list:
        print("No edges were added. Graph creation cancelled.")
        return None

    if not graph.is_connected():
        print("Warning: The graph is not connected. Please ensure all nodes are reachable.")
        return None

    return graph


def create_graph_from_file():
    """Create a graph from a file containing edge definitions."""
    filename = input("Enter filename: ").strip()

    if filename.lower() == 'q':
        return None

    try:
        graph = Graph()

        with open(filename, 'r') as file:
            line_number = 0
            for line in file:
                line_number += 1
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                if len(parts) != 2:
                    print(f"Warning: Skipping invalid line {line_number}: {line}")
                    continue

                try:
                    node1 = int(parts[0])
                    node2 = int(parts[1])

                    if node1 < 1 or node2 < 1:
                        print(f"Warning: Skipping line {line_number} (negative node numbers)")
                        continue

                    if node1 == node2:
                        print(f"Warning: Skipping line {line_number} (self-loop)")
                        continue

                    graph.add_edge(node1, node2)

                except ValueError:
                    print(f"Warning: Skipping invalid line {line_number}: {line}")

        if not graph.adjacency_list:
            print("No valid edges found in file.")
            return None

        if not graph.is_connected():
            print("Warning: The graph is not connected.")
            return None

        print(f"Successfully loaded graph with {len(graph.get_nodes())} nodes.")
        return graph

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None


def create_random_graph():
    """Generate a random connected graph."""
    print("\nRandom Graph Generation")

    num_nodes_input = input("Enter number of nodes: ").strip()
    if num_nodes_input.lower() == 'q':
        return None

    try:
        num_nodes = int(num_nodes_input)
        if num_nodes < 2:
            print("Need at least 2 nodes.")
            return None
    except ValueError:
        print("Invalid input.")
        return None

    num_edges_input = input(f"Enter number of edges (min {num_nodes-1}, max {num_nodes*(num_nodes-1)//2}), or press Enter for random: ").strip()

    if num_edges_input.lower() == 'q':
        return None

    min_edges = num_nodes - 1
    max_edges = num_nodes * (num_nodes - 1) // 2

    if num_edges_input == '':
        num_edges = random.randint(min_edges, min(min_edges + num_nodes, max_edges))
    else:
        try:
            num_edges = int(num_edges_input)
            if num_edges < min_edges:
                print(f"Need at least {min_edges} edges for connectivity.")
                return None
            if num_edges > max_edges:
                print(f"Maximum {max_edges} edges possible.")
                return None
        except ValueError:
            print("Invalid input.")
            return None

    graph = Graph()
    nodes = list(range(1, num_nodes + 1))

    # Create a random spanning tree to ensure connectivity
    remaining_nodes = nodes[1:]
    random.shuffle(remaining_nodes)
    connected_nodes = [nodes[0]]

    for node in remaining_nodes:
        connect_to = random.choice(connected_nodes)
        graph.add_edge(node, connect_to)
        connected_nodes.append(node)

    # Add additional random edges
    edges_added = num_nodes - 1
    max_attempts = num_edges * 3
    attempts = 0

    while edges_added < num_edges and attempts < max_attempts:
        attempts += 1
        node1 = random.choice(nodes)
        node2 = random.choice(nodes)

        if node1 != node2 and node2 not in graph.get_neighbors(node1):
            graph.add_edge(node1, node2)
            edges_added += 1

    print(f"Generated random graph with {num_nodes} nodes and {edges_added} edges.")
    return graph


def assign_tiles_manually(graph):
    """Allow user to manually assign tiles to nodes."""
    print("\nManual Tile Assignment")
    print("Assign a tile number to each node.")

    nodes = graph.get_nodes()
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

    graph.assign_tiles(tile_assignment)
    return True


def assign_tiles_randomly(graph):
    """Randomly assign tiles to nodes."""
    nodes = graph.get_nodes()
    tiles = nodes.copy()
    random.shuffle(tiles)

    tile_assignment = {}
    for i, node in enumerate(nodes):
        tile_assignment[node] = tiles[i]

    graph.assign_tiles(tile_assignment)
    print("Tiles assigned randomly.")


def calculate_optimal_moves(tile_configuration):
    """
    Calculate the minimum number of swaps needed to sort tiles.
    This uses cycle decomposition of the permutation.

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
            # Where is this tile currently?
            current_position = current_positions[current_tile]
            # Move to the tile that should be at this position
            current_tile = current_position

        # A cycle of length n requires n-1 swaps
        if cycle_length > 1:
            num_swaps += cycle_length - 1

    return num_swaps


def play_game(graph, initial_tiles):
    """
    Main game loop.

    Args:
        graph: The graph to play on
        initial_tiles: The initial tile configuration for optimal calculation
    """
    move_count = 0

    print("\n" + "="*50)
    print("GAME START")
    print("="*50)

    graph.display_graph()

    # Show adjacency matrix at start if applicable
    if len(graph.get_nodes()) > 10:
        graph.display_graph_visual()

    graph.display_tiles()

    optimal_moves = calculate_optimal_moves(initial_tiles)

    print(f"\nCurrent Score (moves): {move_count}")
    print(f"Optimal Solution: {optimal_moves} moves")
    print("\nSwap tiles between connected nodes to match all tiles to their nodes.")
    print("Enter 'q' at any time to quit.")

    while not graph.is_solved():
        print("\n" + "-"*50)

        # Display visual graph before prompting for move
        graph.display_graph_visual()

        user_input = input("\nEnter two connected nodes to swap their tiles (node1 node2): ").strip()

        if user_input.lower() == 'q':
            print("\nGame abandoned.")
            return

        parts = user_input.split()
        if len(parts) != 2:
            print("Invalid format. Please enter two node numbers.")
            continue

        try:
            node1 = int(parts[0])
            node2 = int(parts[1])

            if node1 not in graph.adjacency_list or node2 not in graph.adjacency_list:
                print(f"Invalid nodes. Available nodes: {graph.get_nodes()}")
                continue

            if node2 not in graph.get_neighbors(node1):
                print(f"Nodes {node1} and {node2} are not connected.")
                print(f"Node {node1} is connected to: {sorted(graph.get_neighbors(node1))}")
                continue

            graph.swap_tiles(node1, node2)
            move_count += 1

            graph.display_tiles()
            print(f"\nCurrent Score (moves): {move_count}")

        except ValueError:
            print("Invalid input. Please enter integers.")

    # Game won!
    print("\n" + "="*50)
    print("CONGRATULATIONS! YOU WON!")
    print("="*50)
    print(f"Final Score: {move_count} moves")
    print(f"Optimal Solution: {optimal_moves} moves")

    if move_count == optimal_moves:
        print("PERFECT! You solved it optimally!")
    elif move_count <= optimal_moves * 1.5:
        print("Great job! Very efficient solution!")
    else:
        print("You solved it! Try to find a more efficient path next time.")

    print("="*50)


def main():
    """Main program loop."""
    print("="*50)
    print("GRAPH TILE PUZZLE GAME")
    print("="*50)

    while True:
        print("\n" + "="*50)
        print("STEP 1: Create Graph")
        print("="*50)
        print("1. Enter edges manually")
        print("2. Load from file")
        print("3. Generate random graph")
        print("q. Quit")

        choice = input("\nChoice: ").strip()

        if choice == 'q':
            print("Goodbye!")
            return

        graph = None

        if choice == '1':
            graph = create_graph_manually()
        elif choice == '2':
            graph = create_graph_from_file()
        elif choice == '3':
            graph = create_random_graph()
        else:
            print("Invalid choice.")
            continue

        if graph is None:
            continue

        graph.display_graph()

        # Step 2: Assign tiles
        print("\n" + "="*50)
        print("STEP 2: Assign Tiles")
        print("="*50)
        print("1. Assign tiles manually")
        print("2. Assign tiles randomly")
        print("q. Quit")

        choice = input("\nChoice: ").strip()

        if choice == 'q':
            print("Goodbye!")
            return
        elif choice == '1':
            if not assign_tiles_manually(graph):
                continue
        elif choice == '2':
            assign_tiles_randomly(graph)
        else:
            print("Invalid choice.")
            continue

        # Check if already solved
        if graph.is_solved():
            print("\nThe tiles are already in the correct positions!")
            print("Randomizing tiles...")
            assign_tiles_randomly(graph)

        # Store initial state for optimal calculation
        initial_tiles = graph.tiles.copy()

        # Step 3: Play the game
        play_game(graph, initial_tiles)

        # Ask if they want to play again
        print("\n" + "="*50)
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Goodbye!")
            return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
