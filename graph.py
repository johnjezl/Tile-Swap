#!/usr/bin/env python3
"""
Graph Module

Represents an undirected connected graph data structure for Tile Swap.
"""

from collections import deque


class Graph:
    """Represents an undirected connected graph with tile assignments."""

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

    def has_node(self, node):
        """Check if a node exists in the graph."""
        return node in self.adjacency_list

    def are_connected(self, node1, node2):
        """Check if two nodes are directly connected."""
        return node2 in self.get_neighbors(node1)
