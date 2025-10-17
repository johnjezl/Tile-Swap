#!/usr/bin/env python3
"""
Graph Builder Module

Factory class for creating graphs from various sources for Tile Swap.
"""

import random
from graph import Graph


class GraphBuilder:
    """Handles graph creation from various sources."""

    @staticmethod
    def create_manually():
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

        if len(graph.get_nodes()) > 20:
            print(f"Graph has {len(graph.get_nodes())} nodes. Maximum 20 nodes allowed.")
            return None

        if not graph.is_connected():
            print("Warning: The graph is not connected. Please ensure all nodes are reachable.")
            return None

        return graph

    @staticmethod
    def create_from_file():
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

            if len(graph.get_nodes()) > 20:
                print(f"Graph has {len(graph.get_nodes())} nodes. Maximum 20 nodes allowed.")
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

    @staticmethod
    def create_random():
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
            if num_nodes > 20:
                print("Maximum 20 nodes allowed.")
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

    @staticmethod
    def create_random_with_params(num_nodes, num_edges):
        """
        Generate a random connected graph with specified parameters.

        Args:
            num_nodes: Number of nodes to create
            num_edges: Number of edges to create

        Returns:
            Graph object or None if invalid parameters
        """
        if num_nodes < 2 or num_nodes > 20:
            return None

        min_edges = num_nodes - 1
        max_edges = num_nodes * (num_nodes - 1) // 2

        if num_edges < min_edges or num_edges > max_edges:
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

        return graph
