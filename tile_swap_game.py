#!/usr/bin/env python3
"""
Tile Swap Game Module

Main game controller for Tile Swap.
"""

from graph_builder import GraphBuilder
from tile_manager import TileManager
from game_display import GameDisplay
from score_calculator import ScoreCalculator


class TileSwapGame:
    """Main game controller for Tile Swap."""

    def __init__(self):
        self.graph = None
        self.tile_manager = None
        self.display = None
        self.move_count = 0
        self.initial_tiles = None
        self.optimal_moves = 0

    def setup_graph(self):
        """Guide player through graph creation."""
        print("\n" + "="*50)
        print("STEP 1: Create Graph")
        print("="*50)
        print("1. Enter edges manually")
        print("2. Load from file")
        print("3. Generate random graph")
        print("q. Quit")

        choice = input("\nChoice: ").strip()

        if choice == 'q':
            return False

        if choice == '1':
            self.graph = GraphBuilder.create_manually()
        elif choice == '2':
            self.graph = GraphBuilder.create_from_file()
        elif choice == '3':
            self.graph = GraphBuilder.create_random()
        else:
            print("Invalid choice.")
            return False

        if self.graph is None:
            return False

        self.tile_manager = TileManager(self.graph)
        self.display = GameDisplay(self.graph)

        self.display.display_graph_structure()
        return True

    def setup_tiles(self):
        """Guide player through tile assignment."""
        print("\n" + "="*50)
        print("STEP 2: Assign Tiles")
        print("="*50)
        print("1. Assign tiles manually")
        print("2. Assign tiles randomly")
        print("q. Quit")

        choice = input("\nChoice: ").strip()

        if choice == 'q':
            return False
        elif choice == '1':
            if not self.tile_manager.assign_tiles_manually():
                return False
        elif choice == '2':
            self.tile_manager.assign_tiles_randomly()
        else:
            print("Invalid choice.")
            return False

        # Check if already solved
        if self.tile_manager.is_solved():
            print("\nThe tiles are already in the correct positions!")
            print("Randomizing tiles...")
            self.tile_manager.assign_tiles_randomly()

        # Store initial state for optimal calculation
        self.initial_tiles = self.tile_manager.get_initial_configuration()
        self.optimal_moves = ScoreCalculator.calculate_optimal_moves(self.initial_tiles)

        # Display adjacency matrix after tiles are assigned
        print("\n" + "="*50)
        print("TILE ASSIGNMENT COMPLETE")
        print("="*50)
        self.display.display_adjacency_matrix()

        return True

    def play(self):
        """Main game loop."""
        self.move_count = 0

        print("\n" + "="*50)
        print("TILE SWAP - GAME START")
        print("="*50)

        self.display.display_tiles()

        print(f"\nCurrent Score (moves): {self.move_count}")
        print(f"Optimal Solution: {self.optimal_moves} moves")
        print("\nSwap tiles between connected nodes to match all tiles to their nodes.")
        print("Enter 'q' at any time to quit.")

        while not self.tile_manager.is_solved():
            print("\n" + "-"*50)

            # Display circular layout before prompting for move (always)
            self.display.display_visual_graph()

            user_input = input("\nEnter two connected nodes to swap their tiles (node1 node2): ").strip()

            if user_input.lower() == 'q':
                print("\nGame abandoned.")
                return

            if not self._process_move(user_input):
                continue

            self.display.display_tiles()
            print(f"\nCurrent Score (moves): {self.move_count}")

        self._display_victory()

    def _process_move(self, user_input):
        """Process a player move. Returns True if valid, False otherwise."""
        parts = user_input.split()
        if len(parts) != 2:
            print("Invalid format. Please enter two node numbers.")
            return False

        try:
            node1 = int(parts[0])
            node2 = int(parts[1])

            if not self.graph.has_node(node1) or not self.graph.has_node(node2):
                print(f"Invalid nodes. Available nodes: {self.graph.get_nodes()}")
                return False

            if not self.graph.are_connected(node1, node2):
                print(f"Nodes {node1} and {node2} are not connected.")
                print(f"Node {node1} is connected to: {sorted(self.graph.get_neighbors(node1))}")
                return False

            self.tile_manager.swap_tiles(node1, node2)
            self.move_count += 1
            return True

        except ValueError:
            print("Invalid input. Please enter integers.")
            return False

    def _display_victory(self):
        """Display victory message and statistics."""
        print("\n" + "="*50)
        print("CONGRATULATIONS! YOU WON!")
        print("="*50)
        print(f"Final Score: {self.move_count} moves")
        print(f"Optimal Solution: {self.optimal_moves} moves")

        if self.move_count == self.optimal_moves:
            print("PERFECT! You solved it optimally!")
        elif self.move_count <= self.optimal_moves * 1.5:
            print("Great job! Very efficient solution!")
        else:
            print("You solved it! Try to find a more efficient path next time.")

        print("="*50)

    def run(self):
        """Run the complete game session."""
        print("="*50)
        print("TILE SWAP")
        print("A Graph-Based Puzzle Game")
        print("="*50)

        while True:
            if not self.setup_graph():
                print("Goodbye!")
                return

            if not self.setup_tiles():
                continue

            self.play()

            # Ask if they want to play again
            print("\n" + "="*50)
            play_again = input("Play again? (y/n): ").strip().lower()
            if play_again != 'y':
                print("Thanks for playing Tile Swap!")
                return
