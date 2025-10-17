# Web Interface Guide

This guide explains the new web interface for the Tile Swap puzzle game.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the web server:**
   ```bash
   python web_app.py
   ```

3. **Open your browser to:**
   ```
   http://localhost:5000
   ```

## How to Play

1. **Create a Game:** Click "New Random Game" to generate a random graph with the specified number of nodes

2. **Select a Node:** Click on any node to select it (it will show a yellow outline)

3. **Swap Tiles:** Click on a connected node to swap tiles between the selected node and the clicked node

4. **Win Condition:** Match all tile numbers to their corresponding node numbers

5. **Visual Feedback:**
   - **Green nodes** = Tile matches node number
   - **Blue nodes** = Tile doesn't match node number
   - **Yellow outline** = Currently selected node
   - **Gray lines** = Edges connecting nodes

## Architecture Overview

### Backend (Python)

The web interface uses Flask to provide a REST API that connects to the existing game logic:

```
web_app.py (Flask Server)
    ↓
web_game_state.py (Adapter)
    ↓
Core Modules (graph.py, tile_manager.py, etc.)
```

**API Endpoints:**
- `POST /api/new_game` - Create a new random game
- `POST /api/custom_game` - Create a game from custom edges
- `POST /api/swap` - Swap tiles between two nodes
- `GET /api/state` - Get current game state
- `POST /api/reset` - Reset the game

### Frontend (JavaScript)

The client-side is built with vanilla JavaScript and HTML5 Canvas:

```
index.html (Structure)
    ↓
game.js (Game Logic & Rendering)
    ↓
style.css (Visual Styling)
```

**Key Classes:**
- `TileSwapGame` - Main game controller
  - Manages canvas rendering
  - Handles user interactions
  - Communicates with backend via Fetch API
  - Draws graph visualization

## Modular Design Benefits

The web interface was designed to **minimize modifications** to the existing codebase:

### What Was Reused (Zero Changes)
- ✅ `graph.py` - Core graph data structure
- ✅ `tile_manager.py` - Tile operations
- ✅ `score_calculator.py` - Optimal solution calculation
- ✅ All test files

### What Was Extended (Minor Changes)
- ✅ `graph_builder.py` - Added `create_random_with_params()` method for programmatic graph creation

### What Was Added (New Files)
- ✅ `web_game_state.py` - Thin adapter layer between Flask and game logic
- ✅ `web_app.py` - Flask application
- ✅ `templates/index.html` - HTML structure
- ✅ `static/game.js` - Client-side game logic
- ✅ `static/style.css` - Visual styling
- ✅ `requirements.txt` - Python dependencies

## Key Design Decisions

1. **Session-Based State Management:** Each user gets their own game state stored server-side, identified by session ID

2. **RESTful API:** Clean separation between frontend and backend using JSON API

3. **Canvas Rendering:** HTML5 Canvas provides smooth, interactive graphics without external libraries

4. **Circular Layout:** Nodes are arranged in a circle for optimal visualization (same as CLI version)

5. **No External JS Libraries:** Pure vanilla JavaScript for simplicity and minimal dependencies

## Customization

### Changing Graph Size
Edit the HTML input in `templates/index.html`:
```html
<input type="number" id="num-nodes" min="3" max="15" value="6">
```

### Adjusting Visual Style
Edit colors and sizes in `static/style.css` or the draw functions in `static/game.js`

### Adding Features
The modular design makes it easy to add:
- Custom graph editor (drag-and-drop nodes)
- Different layout algorithms (force-directed, hierarchical)
- Multiplayer mode (using WebSockets)
- Undo/redo functionality
- Save/load game states

## Troubleshooting

**Problem:** Port 5000 already in use
**Solution:** Change the port in `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

**Problem:** Templates not found
**Solution:** Make sure you're running from the project root directory

**Problem:** Static files not loading
**Solution:** Check that the `static/` and `templates/` directories exist with the correct files

## Performance Notes

- The web interface supports graphs up to 20 nodes (same as CLI)
- Canvas rendering is optimized for smooth 60 FPS interaction
- Session cleanup happens automatically (sessions expire after inactivity)

## Future Enhancements

Possible improvements for the web interface:
- [ ] Drag-and-drop graph builder
- [ ] Animation for tile swaps
- [ ] Sound effects
- [ ] Leaderboard/high scores
- [ ] Multiple difficulty levels
- [ ] Tutorial mode with hints
- [ ] Mobile touch gestures
- [ ] Dark mode toggle

Enjoy the new web interface!
