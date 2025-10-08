#!/usr/bin/env python3
"""
Tile Swap - A Graph-Based Puzzle Game

Main entry point for the Tile Swap game.

A puzzle game where players create a connected graph and swap tiles between
connected nodes until all tiles match their corresponding node numbers.
"""

import sys
from tile_swap_game import TileSwapGame


def main():
    """Main entry point for Tile Swap."""
    try:
        game = TileSwapGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
