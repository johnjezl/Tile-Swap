#!/usr/bin/env python3
"""
Multiplayer Room Manager

Manages game rooms for competitive multiplayer Tile Swap.
Supports both real-time and turn-based modes with up to 30 players per room.
"""

import random
import string
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class GameMode(Enum):
    """Game mode enum."""
    REAL_TIME = "realtime"
    TURN_BASED = "turnbased"


class RoomState(Enum):
    """Room state enum."""
    LOBBY = "lobby"          # Waiting for players
    READY = "ready"          # All players ready, countdown
    PLAYING = "playing"      # Game in progress
    FINISHED = "finished"    # Game completed


@dataclass
class Player:
    """Represents a player in a multiplayer game."""
    session_id: str
    name: str
    player_number: int = 0  # For display purposes (Player 1, Player 2, etc.)
    moves: int = 0
    solved: bool = False
    ready: bool = False
    finish_time: Optional[float] = None
    finish_rank: Optional[int] = None
    current_turn: bool = False  # For turn-based mode


@dataclass
class GameRoom:
    """Represents a multiplayer game room."""
    code: str
    mode: GameMode
    max_players: int = 30
    host_session_id: str = ""
    state: RoomState = RoomState.LOBBY
    players: Dict[str, Player] = field(default_factory=dict)

    # Game configuration (same for all players)
    graph_edges: List[tuple] = field(default_factory=list)
    initial_tiles: Dict[int, int] = field(default_factory=dict)

    # Turn-based specific
    current_turn_index: int = 0
    turn_order: List[str] = field(default_factory=list)

    # Timing
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    finished_at: Optional[float] = None

    def add_player(self, session_id: str, name: str) -> bool:
        """Add a player to the room."""
        if len(self.players) >= self.max_players:
            return False

        if self.state != RoomState.LOBBY:
            return False

        # Set first player as host
        if not self.host_session_id:
            self.host_session_id = session_id

        # Assign player number based on current count
        player_number = len(self.players) + 1

        # If no custom name provided, just show player number
        if not name.strip():
            display_name = f'Player {player_number}'
        else:
            display_name = f'Player {player_number}: {name.strip()}'

        self.players[session_id] = Player(
            session_id=session_id,
            name=display_name,
            player_number=player_number
        )
        return True

    def remove_player(self, session_id: str) -> None:
        """Remove a player from the room."""
        if session_id in self.players:
            del self.players[session_id]

        # If host left, assign new host
        if session_id == self.host_session_id and self.players:
            self.host_session_id = list(self.players.keys())[0]

        # Remove from turn order if turn-based
        if session_id in self.turn_order:
            self.turn_order.remove(session_id)

    def set_player_ready(self, session_id: str, ready: bool) -> None:
        """Set player ready status."""
        if session_id in self.players:
            self.players[session_id].ready = ready

    def change_player_name(self, session_id: str, new_name: str) -> bool:
        """Change a player's name, keeping the player number prefix."""
        if session_id in self.players and new_name.strip():
            player = self.players[session_id]
            # Keep the player number, update the custom name
            self.players[session_id].name = f'Player {player.player_number}: {new_name.strip()}'
            return True
        return False

    def all_players_ready(self) -> bool:
        """Check if all players are ready."""
        if not self.players:
            return False
        return all(p.ready for p in self.players.values())

    def start_game(self, graph_edges: List[tuple], initial_tiles: Dict[int, int]) -> None:
        """Start the game with the given configuration."""
        self.graph_edges = graph_edges
        self.initial_tiles = initial_tiles
        self.state = RoomState.PLAYING
        self.started_at = time.time()

        # Setup turn order for turn-based mode
        if self.mode == GameMode.TURN_BASED:
            self.turn_order = list(self.players.keys())
            random.shuffle(self.turn_order)
            if self.turn_order:
                self.players[self.turn_order[0]].current_turn = True

    def update_player_progress(self, session_id: str, moves: int, solved: bool) -> None:
        """Update a player's progress."""
        if session_id not in self.players:
            return

        player = self.players[session_id]
        player.moves = moves

        # Handle solve
        if solved and not player.solved:
            player.solved = True
            player.finish_time = time.time()

            # Calculate rank
            finished_count = sum(1 for p in self.players.values() if p.solved)
            player.finish_rank = finished_count

            # Check if all finished
            if all(p.solved for p in self.players.values()):
                self.state = RoomState.FINISHED
                self.finished_at = time.time()

    def next_turn(self) -> Optional[str]:
        """Advance to next player's turn (turn-based mode only)."""
        if self.mode != GameMode.TURN_BASED or not self.turn_order:
            return None

        # Clear current turn
        current_session = self.turn_order[self.current_turn_index]
        self.players[current_session].current_turn = False

        # Find next player who hasn't solved yet
        attempts = 0
        while attempts < len(self.turn_order):
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
            next_session = self.turn_order[self.current_turn_index]

            # If this player hasn't solved, give them the turn
            if not self.players[next_session].solved:
                self.players[next_session].current_turn = True
                return next_session

            attempts += 1

        # All players have solved - no one gets a turn
        return None

    def get_leaderboard(self) -> List[Dict]:
        """Get sorted leaderboard data."""
        players_list = []

        for session_id, player in self.players.items():
            players_list.append({
                'session_id': session_id,
                'name': player.name,
                'moves': player.moves,
                'solved': player.solved,
                'ready': player.ready,
                'rank': player.finish_rank,
                'is_current_turn': player.current_turn,
                'is_host': session_id == self.host_session_id
            })

        # Sort: solved players by rank, then by moves, then unsolved by moves
        def sort_key(p):
            if p['solved']:
                return (0, p['rank'], p['moves'])
            else:
                return (1, p['moves'], 0)

        players_list.sort(key=sort_key)
        return players_list

    def get_room_info(self) -> Dict:
        """Get room information for clients."""
        return {
            'code': self.code,
            'mode': self.mode.value,
            'state': self.state.value,
            'player_count': len(self.players),
            'max_players': self.max_players,
            'all_ready': self.all_players_ready(),
            'leaderboard': self.get_leaderboard(),
            'graph_edges': self.graph_edges,
            'initial_tiles': self.initial_tiles,
            'current_turn_session': self.turn_order[self.current_turn_index] if self.turn_order else None
        }


class MultiplayerManager:
    """Manages all multiplayer rooms."""

    def __init__(self):
        self.rooms: Dict[str, GameRoom] = {}

    def generate_room_code(self) -> str:
        """Generate a unique room code."""
        while True:
            code = 'TILE-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            if code not in self.rooms:
                return code

    def create_room(self, host_session_id: str, mode: GameMode, max_players: int = 30) -> str:
        """Create a new game room."""
        code = self.generate_room_code()
        self.rooms[code] = GameRoom(
            code=code,
            mode=mode,
            max_players=max_players,
            host_session_id=host_session_id
        )
        return code

    def get_room(self, code: str) -> Optional[GameRoom]:
        """Get a room by code."""
        return self.rooms.get(code)

    def delete_room(self, code: str) -> None:
        """Delete a room."""
        if code in self.rooms:
            del self.rooms[code]

    def cleanup_empty_rooms(self) -> None:
        """Remove rooms with no players."""
        empty_rooms = [code for code, room in self.rooms.items() if not room.players]
        for code in empty_rooms:
            del self.rooms[code]

    def cleanup_old_rooms(self, max_age_hours: int = 24) -> None:
        """Remove rooms older than max_age_hours."""
        cutoff_time = time.time() - (max_age_hours * 3600)
        old_rooms = [
            code for code, room in self.rooms.items()
            if room.created_at < cutoff_time
        ]
        for code in old_rooms:
            del self.rooms[code]

    def get_active_rooms_count(self) -> int:
        """Get count of active rooms."""
        return len(self.rooms)

    def get_total_players_count(self) -> int:
        """Get total number of players across all rooms."""
        return sum(len(room.players) for room in self.rooms.values())
