#!/usr/bin/env python3
"""
Flask Web Application for Tile Swap Game - WITH MULTIPLAYER

Enhanced version with WebSocket support for competitive multiplayer gaming.
Supports both real-time and turn-based modes with up to 30 players per room.
"""

from flask import Flask, render_template, jsonify, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from web_game_state import WebGameState
from multiplayer import MultiplayerManager, GameMode
from score_calculator import ScoreCalculator
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = app.secret_key

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game states per session (single player)
game_states = {}

# Multiplayer manager
mp_manager = MultiplayerManager()

# Track session -> room mapping
session_rooms = {}

# Track session -> socket ID mapping
session_sockets = {}


def get_game_state():
    """Get or create game state for current session."""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)

    session_id = session['session_id']
    if session_id not in game_states:
        game_states[session_id] = WebGameState()

    return game_states[session_id]


def get_session_id():
    """Get current session ID."""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)
    return session['session_id']


# ============================================================================
# REGULAR ROUTES (Single Player)
# ============================================================================

@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Create a new random game."""
    data = request.get_json()
    num_nodes = data.get('num_nodes', 6)
    num_edges = data.get('num_edges', None)

    game = get_game_state()
    game.reset_game()

    if not game.create_random_graph(num_nodes, num_edges):
        return jsonify({'success': False, 'message': 'Failed to create graph'}), 400

    if not game.assign_tiles_randomly():
        return jsonify({'success': False, 'message': 'Failed to assign tiles'}), 400

    return jsonify({
        'success': True,
        'state': game.get_game_state()
    })


@app.route('/api/custom_game', methods=['POST'])
def custom_game():
    """Create a game from custom edge list."""
    data = request.get_json()
    edges = data.get('edges', [])

    game = get_game_state()
    game.reset_game()

    edge_tuples = [(e[0], e[1]) for e in edges]

    if not game.create_graph_from_edges(edge_tuples):
        return jsonify({'success': False, 'message': 'Invalid graph - must be connected'}), 400

    if not game.assign_tiles_randomly():
        return jsonify({'success': False, 'message': 'Failed to assign tiles'}), 400

    return jsonify({
        'success': True,
        'state': game.get_game_state()
    })


@app.route('/api/custom_game_with_tiles', methods=['POST'])
def custom_game_with_tiles():
    """Create a game from custom edge list with specific tile assignment."""
    try:
        data = request.get_json()
        edges = data.get('edges', [])
        tiles = data.get('tiles', {})

        print(f"DEBUG custom_game_with_tiles: received edges={len(edges)}, tiles={tiles}")

        game = get_game_state()
        game.reset_game()

        edge_tuples = [(e[0], e[1]) for e in edges]

        if not game.create_graph_from_edges(edge_tuples):
            return jsonify({'success': False, 'message': 'Invalid graph - must be connected'}), 400

        # Convert tile keys from strings to ints if needed
        if tiles:
            tile_dict = {int(k): int(v) for k, v in tiles.items()}
            game.graph.tiles = tile_dict

            # Set up game state properly
            game.initial_tiles = tile_dict.copy()
            game.game_active = True
            game.move_count = 0
            game.move_history = []
            game.redo_stack = []

            # Calculate optimal moves using ScoreCalculator
            game.optimal_moves = ScoreCalculator.calculate_optimal_moves(tile_dict)
        else:
            print("WARNING: No tiles provided to custom_game_with_tiles")

        return jsonify({
            'success': True,
            'state': game.get_game_state()
        })
    except Exception as e:
        print(f"ERROR in custom_game_with_tiles: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/swap', methods=['POST'])
def swap():
    """Swap tiles between two nodes."""
    data = request.get_json()
    node1 = data.get('node1')
    node2 = data.get('node2')

    if node1 is None or node2 is None:
        return jsonify({'success': False, 'message': 'Missing nodes'}), 400

    game = get_game_state()
    result = game.swap_tiles(node1, node2)

    if not result['success']:
        return jsonify(result), 400

    result['state'] = game.get_game_state()
    return jsonify(result)


@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current game state."""
    game = get_game_state()
    return jsonify(game.get_game_state())


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the current game."""
    game = get_game_state()
    game.reset_game()
    return jsonify({'success': True})


@app.route('/api/undo', methods=['POST'])
def undo():
    """Undo the last move."""
    game = get_game_state()
    result = game.undo_move()

    if not result['success']:
        return jsonify(result), 400

    result['state'] = game.get_game_state()
    return jsonify(result)


@app.route('/api/redo', methods=['POST'])
def redo():
    """Redo a previously undone move."""
    game = get_game_state()
    result = game.redo_move()

    if not result['success']:
        return jsonify(result), 400

    result['state'] = game.get_game_state()
    return jsonify(result)


@app.route('/api/save', methods=['GET'])
def save():
    """Save current game state."""
    game = get_game_state()
    save_data = game.save_game()

    if save_data is None:
        return jsonify({'success': False, 'message': 'No game to save'}), 400

    return jsonify({'success': True, 'data': save_data})


@app.route('/api/load', methods=['POST'])
def load():
    """Load a saved game state."""
    data = request.get_json()
    save_data = data.get('data')

    if not save_data:
        return jsonify({'success': False, 'message': 'No save data provided'}), 400

    game = get_game_state()
    if not game.load_game(save_data):
        return jsonify({'success': False, 'message': 'Failed to load game'}), 400

    return jsonify({
        'success': True,
        'state': game.get_game_state()
    })


# ============================================================================
# WEBSOCKET EVENTS (Multiplayer)
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    session_id = get_session_id()
    session_sockets[session_id] = request.sid
    print(f"Client connected: {session_id}")
    emit('connected', {'session_id': session_id})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    session_id = get_session_id()

    # Remove from any room
    if session_id in session_rooms:
        room_code = session_rooms[session_id]
        room = mp_manager.get_room(room_code)

        if room:
            room.remove_player(session_id)
            leave_room(room_code)

            # Notify other players
            socketio.emit('player_left', {
                'session_id': session_id,
                'room_info': room.get_room_info()
            }, to=room_code)

            # Delete empty rooms
            if not room.players:
                mp_manager.delete_room(room_code)

        del session_rooms[session_id]

    if session_id in session_sockets:
        del session_sockets[session_id]

    print(f"Client disconnected: {session_id}")


@socketio.on('create_room')
def handle_create_room(data):
    """Create a new multiplayer room."""
    session_id = get_session_id()
    mode_str = data.get('mode', 'realtime')
    player_name = data.get('name', '').strip()
    # Don't auto-generate name here - will be set based on player number
    num_nodes = data.get('num_nodes', 6)

    # Create mode enum
    mode = GameMode.REAL_TIME if mode_str == 'realtime' else GameMode.TURN_BASED

    # Create room
    room_code = mp_manager.create_room(session_id, mode)
    room = mp_manager.get_room(room_code)

    # Add host as first player
    room.add_player(session_id, player_name)

    # Join socket.io room
    join_room(room_code)
    session_rooms[session_id] = room_code
    print(f"Host socket {request.sid} created and joined room {room_code}")

    # Create the game graph (host's game state)
    game = get_game_state()
    game.reset_game()
    game.create_random_graph(num_nodes)

    # Assign tiles to the host's graph so they're ready when game starts
    game.assign_tiles_randomly()
    print(f"Host graph created with tiles: {game.graph.tiles}")

    # Store graph structure AND tiles in room (for all players to use)
    graph_edges = []
    for node in game.graph.get_nodes():
        for neighbor in game.graph.get_neighbors(node):
            if node < neighbor:
                graph_edges.append((node, neighbor))
    room.graph_edges = graph_edges
    room.initial_tiles = game.graph.tiles.copy()  # Store tiles in room immediately!

    print(f"Room {room_code} created with {len(graph_edges)} edges, {num_nodes} nodes")
    print(f"Graph edges: {graph_edges}")
    print(f"Initial tiles stored in room: {room.initial_tiles}")

    emit('room_created', {
        'success': True,
        'room_code': room_code,
        'room_info': room.get_room_info()
    })


@socketio.on('join_room')
def handle_join_room(data):
    """Join an existing multiplayer room."""
    session_id = get_session_id()
    room_code = data.get('room_code', '').upper().strip()
    player_name = data.get('name', '').strip()

    room = mp_manager.get_room(room_code)

    # Don't auto-generate name here - will be set based on player number in add_player

    if not room:
        emit('join_failed', {'message': 'Room not found'})
        return

    if not room.add_player(session_id, player_name):
        emit('join_failed', {'message': 'Room is full or game already started'})
        return

    # Join socket.io room
    join_room(room_code)
    session_rooms[session_id] = room_code
    print(f"Socket {request.sid} joined room {room_code}")

    room_info = room.get_room_info()
    print(f"Player {player_name} (session {session_id}) joined room {room_code}")
    print(f"Room info graph_edges: {room_info['graph_edges']}")
    print(f"Room info initial_tiles: {room_info['initial_tiles']}")

    # Notify everyone
    print(f"Broadcasting player_joined to room {room_code}")
    socketio.emit('player_joined', {
        'session_id': session_id,
        'name': player_name,
        'room_info': room_info
    }, to=room_code)

    emit('room_joined', {
        'success': True,
        'room_code': room_code,
        'room_info': room_info
    })

    # Test broadcast to verify room membership works
    print(f"Sending test_broadcast to room {room_code}")
    socketio.emit('test_broadcast', {
        'message': f'Player {player_name} joined successfully'
    }, to=room_code)


@socketio.on('leave_room')
def handle_leave_room():
    """Leave current room."""
    session_id = get_session_id()

    if session_id not in session_rooms:
        return

    room_code = session_rooms[session_id]
    room = mp_manager.get_room(room_code)

    if room:
        room.remove_player(session_id)
        leave_room(room_code)

        # Notify others
        socketio.emit('player_left', {
            'session_id': session_id,
            'room_info': room.get_room_info()
        }, to=room_code)

        # Delete if empty
        if not room.players:
            mp_manager.delete_room(room_code)

    del session_rooms[session_id]
    emit('left_room', {'success': True})


@socketio.on('toggle_ready')
def handle_toggle_ready(data):
    """Toggle player ready status."""
    session_id = get_session_id()

    if session_id not in session_rooms:
        return

    room_code = session_rooms[session_id]
    room = mp_manager.get_room(room_code)

    if not room:
        return

    ready = data.get('ready', True)
    room.set_player_ready(session_id, ready)

    # Broadcast to room
    print(f"Broadcasting player_ready_changed to room {room_code}")
    socketio.emit('player_ready_changed', {
        'session_id': session_id,
        'ready': ready,
        'room_info': room.get_room_info()
    }, to=room_code)
    print(f"Ready status broadcast complete")


@socketio.on('change_name')
def handle_change_name(data):
    """Change player name."""
    session_id = get_session_id()

    if session_id not in session_rooms:
        return

    room_code = session_rooms[session_id]
    room = mp_manager.get_room(room_code)

    if not room:
        return

    new_name = data.get('name', '').strip()
    if room.change_player_name(session_id, new_name):
        print(f"Player {session_id} changed name to {new_name}")
        # Broadcast to room
        socketio.emit('player_name_changed', {
            'session_id': session_id,
            'name': new_name,
            'room_info': room.get_room_info()
        }, to=room_code)
        emit('name_change_success', {'success': True, 'name': new_name})
    else:
        emit('name_change_failed', {'success': False, 'message': 'Invalid name'})


@socketio.on('start_game')
def handle_start_game():
    """Start the multiplayer game (host only)."""
    session_id = get_session_id()

    if session_id not in session_rooms:
        emit('start_failed', {'message': 'Not in a room'})
        return

    room_code = session_rooms[session_id]
    room = mp_manager.get_room(room_code)

    if not room:
        emit('start_failed', {'message': 'Room not found'})
        return

    if room.host_session_id != session_id:
        emit('start_failed', {'message': 'Only host can start'})
        return

    if not room.all_players_ready():
        emit('start_failed', {'message': 'Not all players are ready'})
        return

    # Get graph from host's game state
    host_game = game_states[session_id]

    # DIAGNOSTIC: Check host's game state
    print(f"DEBUG: host_game exists: {host_game is not None}")
    print(f"DEBUG: host_game.graph exists: {host_game.graph is not None}")
    print(f"DEBUG: host_game.graph.tiles = {host_game.graph.tiles}")
    print(f"DEBUG: host_game.game_active = {host_game.game_active}")

    graph_edges = []
    for node in host_game.graph.get_nodes():
        for neighbor in host_game.graph.get_neighbors(node):
            if node < neighbor:
                graph_edges.append((node, neighbor))

    initial_tiles = host_game.graph.tiles.copy()
    print(f"Starting game in room {room_code} with tiles: {initial_tiles}")

    # Start the game
    room.start_game(graph_edges, initial_tiles)

    # Broadcast to all players in room
    print(f"Broadcasting game_started to room {room_code}")
    print(f"Players in room: {list(room.players.keys())}")

    room_info_data = room.get_room_info()
    print(f"Room info state: {room_info_data.get('state')}")
    print(f"Room info has tiles: {bool(room_info_data.get('initial_tiles'))}")

    # DIAGNOSTIC: Show exactly what tiles are in room_info
    print(f"DEBUG: room_info_data['initial_tiles'] = {room_info_data.get('initial_tiles')}")
    print(f"DEBUG: type(room_info_data['initial_tiles']) = {type(room_info_data.get('initial_tiles'))}")
    print(f"DEBUG: len(room_info_data['initial_tiles']) = {len(room_info_data.get('initial_tiles', {}))}")

    # Use emit() with broadcast=True to send to room including sender
    emit('game_started', {
        'room_info': room_info_data
    }, broadcast=True, to=room_code, include_self=True)
    print(f"Game started event broadcast complete")


@socketio.on('player_move')
def handle_player_move(data):
    """Handle a player making a move."""
    session_id = get_session_id()

    if session_id not in session_rooms:
        return

    room_code = session_rooms[session_id]
    room = mp_manager.get_room(room_code)

    if not room or room.state.value != 'playing':
        return

    # For turn-based, check if it's this player's turn
    if room.mode == GameMode.TURN_BASED:
        if session_id not in room.players or not room.players[session_id].current_turn:
            emit('move_failed', {'message': 'Not your turn'})
            return

    moves = data.get('moves', 0)
    solved = data.get('solved', False)

    # Update player progress
    room.update_player_progress(session_id, moves, solved)

    # Advance turn if turn-based (always advance, even if solved)
    if room.mode == GameMode.TURN_BASED:
        next_session = room.next_turn()

    # Broadcast updated leaderboard
    socketio.emit('leaderboard_update', {
        'room_info': room.get_room_info()
    }, to=room_code)


if __name__ == '__main__':
    print("="*50)
    print("TILE SWAP - WEB INTERFACE (MULTIPLAYER)")
    print("="*50)
    print("\nStarting web server with WebSocket support...")
    print("Open your browser to: http://localhost:5000")
    print("\nFeatures:")
    print("  - Single player mode")
    print("  - Competitive multiplayer (up to 30 players)")
    print("  - Real-time and turn-based modes")
    print("\nPress Ctrl+C to stop the server")
    print("="*50)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
