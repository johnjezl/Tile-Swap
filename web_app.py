#!/usr/bin/env python3
"""
Flask Web Application for Tile Swap Game

Provides a web interface for the tile swap puzzle game with
interactive graph visualization.
"""

from flask import Flask, render_template, jsonify, request, session
from web_game_state import WebGameState
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store game states per session
game_states = {}


def get_game_state():
    """Get or create game state for current session."""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(16)

    session_id = session['session_id']
    if session_id not in game_states:
        game_states[session_id] = WebGameState()

    return game_states[session_id]


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

    # Convert edge list to tuples
    edge_tuples = [(e[0], e[1]) for e in edges]

    if not game.create_graph_from_edges(edge_tuples):
        return jsonify({'success': False, 'message': 'Invalid graph - must be connected'}), 400

    if not game.assign_tiles_randomly():
        return jsonify({'success': False, 'message': 'Failed to assign tiles'}), 400

    return jsonify({
        'success': True,
        'state': game.get_game_state()
    })


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

    # Add updated game state to response
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


if __name__ == '__main__':
    print("="*50)
    print("TILE SWAP - WEB INTERFACE")
    print("="*50)
    print("\nStarting web server...")
    print("Open your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)
