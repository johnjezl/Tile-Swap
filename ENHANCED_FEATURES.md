# Enhanced Web Interface Features

This document details all the advanced features added to the web interface.

## Table of Contents

- [Custom Graph Editor](#custom-graph-editor)
- [Animated Tile Swaps](#animated-tile-swaps)
- [Undo/Redo Functionality](#undoredo-functionality)
- [Save/Load Game States](#saveload-game-states)
- [Dark Mode](#dark-mode)
- [Sound Effects](#sound-effects)
- [Keyboard Shortcuts](#keyboard-shortcuts)

---

## Custom Graph Editor

### Overview
Create your own custom graphs using an intuitive drag-and-drop interface instead of random generation.

### How to Use

1. Click the **"Custom Graph Editor"** button in the Game Setup section
2. The graph editor overlay appears with an empty canvas

### Controls

**Adding Nodes:**
- Click anywhere on the canvas to add a new node
- Up to 20 nodes can be added
- Nodes are automatically numbered sequentially (1, 2, 3, ...)

**Adding Edges:**
- Click and hold on a node
- Drag to another node
- Release to create an edge between the two nodes
- Duplicate edges are automatically prevented

**Removing Nodes:**
- Right-click on a node to delete it
- All edges connected to that node are automatically removed

**Editor Status:**
- Live count of nodes and edges displayed at the bottom
- Connection status indicator:
  - ✓ Connected (green) - Graph is valid, all nodes are reachable
  - ✗ Not connected (red) - Graph is invalid, some nodes are isolated

### Starting the Game

1. Click **"Start Game"** when your graph is ready
2. The graph must be connected (all nodes must be reachable from every other node)
3. At least 2 nodes are required
4. Tiles will be randomly assigned to create the puzzle

### Tips

- Create interesting topologies: linear chains, cycles, stars, trees, complete graphs
- More edges generally make the puzzle easier (more swap options)
- Fewer edges create more constrained, challenging puzzles
- Try creating specific graph structures like binary trees or grids

---

## Animated Tile Swaps

### Overview
Smooth visual animations show tiles swapping positions, making moves easier to follow.

### Features

- **Smooth interpolation** - Tiles smoothly move between nodes
- **Easing function** - Uses ease-in-out quadratic easing for natural motion
- **Non-blocking** - Animation prevents accidental double-clicks during swap
- **Preserves game state** - Tiles update after animation completes

### Technical Details

- Animation duration: ~1 second (10 frames at 0.1 progress per frame)
- Uses `requestAnimationFrame` for smooth 60 FPS rendering
- Positions interpolate using ease-in-out quadratic easing
- Backend swap occurs before animation to ensure state consistency

### Accessibility

For users who prefer reduced motion, add this to your browser settings:
- Chrome: Settings → Accessibility → "Prefers reduced motion"
- Firefox: about:config → ui.prefersReducedMotion → 1

The CSS includes a `@media (prefers-reduced-motion: reduce)` rule that minimizes animations.

---

## Undo/Redo Functionality

### Overview
Navigate through your move history with full undo/redo support.

### Features

- **Full move history** - Every swap is recorded
- **Unlimited undo** - Go back to the very first move
- **Redo support** - Redo moves that were undone
- **Move count tracking** - Move counter decrements on undo, increments on redo
- **Smart state management** - Redo stack clears when new move is made after undo

### How to Use

**Using Buttons:**
- Click **↶ Undo** to undo the last move
- Click **↷ Redo** to redo the last undone move
- Buttons are disabled when no moves are available

**Using Keyboard:**
- `Ctrl+Z` (or `Cmd+Z` on Mac) - Undo
- `Ctrl+Shift+Z` (or `Cmd+Shift+Z` on Mac) - Redo

### Button States

- **Enabled** - Can be clicked, full opacity
- **Disabled** - Grayed out, reduced opacity, not clickable
- Updates automatically after every move

### Implementation Notes

- Move history stored as (node1, node2) tuples
- Undo swaps the tiles back and moves entry to redo stack
- Redo re-applies the swap and moves entry back to history
- Server-side state management ensures consistency

---

## Save/Load Game States

### Overview
Save your game progress at any time and resume later.

### Saving a Game

**Method 1: Button**
1. Click the **💾 Save Game** button
2. Browser downloads a JSON file named `tileswap-save-YYYY-MM-DD.json`
3. Success message appears confirming the save

**Method 2: Keyboard**
- Press `Ctrl+S` (or `Cmd+S` on Mac)
- Same as clicking the save button

### What Gets Saved

- Graph structure (all nodes and edges)
- Current tile positions
- Initial tile configuration (for optimal move calculation)
- Move count
- Optimal moves count
- Game active status
- Complete move history (for undo/redo)
- Redo stack

### Loading a Game

1. Click the **📂 Load Game** button
2. File picker opens
3. Select a previously saved `.json` file
4. Game state is restored completely
5. Success message confirms the load

### Save File Format

```json
{
  "version": "1.0",
  "edges": [[1, 2], [2, 3], ...],
  "tiles": {"1": 3, "2": 1, ...},
  "initial_tiles": {"1": 3, "2": 1, ...},
  "move_count": 5,
  "optimal_moves": 3,
  "game_active": true,
  "move_history": [[1, 2], [2, 3]],
  "redo_stack": []
}
```

### Tips

- Save files are human-readable JSON
- You can edit them manually (advanced users)
- Share save files with friends to try the same puzzle
- Save before experimenting with different strategies

---

## Dark Mode

### Overview
Toggle between light and dark color schemes to reduce eye strain.

### How to Use

Click the **🌙/☀️** button in the top-right corner of the header.

### Features

- **Instant toggle** - Mode switches immediately
- **Persistent preference** - Choice is saved to browser localStorage
- **Auto-restore** - Dark mode preference loads on page refresh
- **Smooth transitions** - All colors transition smoothly (0.3s)
- **Complete coverage** - All UI elements support dark mode

### Color Schemes

**Light Mode:**
- Background: Purple/violet gradient
- Cards: White
- Text: Dark gray (#333)
- Canvas: Light gray (#fafafa)

**Dark Mode:**
- Background: Dark purple gradient
- Cards: Dark blue-purple (#2a2a4e)
- Text: Light gray (#e0e0e0)
- Canvas: Very dark blue (#1a1a2e)

### Technical Implementation

Uses CSS custom properties (variables) for dynamic theming:
- `--bg-color`, `--card-bg`, `--text-color`, etc.
- JavaScript toggles `dark-mode` class on `<body>`
- localStorage key: `'darkMode'` (boolean)

---

## Sound Effects

### Overview
Audio feedback enhances the gaming experience with subtle sounds.

### Sound Types

**Swap Sound:**
- Plays when tiles are successfully swapped
- Frequency: 440 Hz → 880 Hz (one octave sweep)
- Duration: 0.1 seconds
- Volume: 30%

**Click Sound:**
- Plays when selecting/deselecting nodes
- Also plays for undo/redo/save/load actions
- Frequency: 800 Hz
- Duration: 0.05 seconds
- Volume: 10%

**Victory Sound:**
- Plays when puzzle is solved
- Four-note ascending arpeggio (C-E-G-C major chord)
- Frequencies: 523.25, 659.25, 783.99, 1046.50 Hz
- Notes play 100ms apart
- Duration per note: 0.3 seconds
- Volume: 20%

### Controls

**Toggle Sound:**
- Use the checkbox in the Game Status section
- Label: "Sound Effects"
- Default: Enabled
- Setting is per-session (not persisted)

### Technical Details

- Uses **Web Audio API** for synthesized sounds
- No external audio files required
- Oscillators generate pure sine waves
- Gain nodes control volume with exponential ramps
- Gracefully degrades if Web Audio API is unavailable

### Customization

Edit [game.js](static/game.js) to customize sounds:
```javascript
// Change swap sound frequency
oscillator.frequency.setValueAtTime(440, this.audioContext.currentTime);
oscillator.frequency.exponentialRampToValueAtTime(880, ...);

// Change victory notes
const notes = [523.25, 659.25, 783.99, 1046.50]; // C, E, G, C
```

---

## Keyboard Shortcuts

### Overview
Power users can control the game entirely from the keyboard.

### Available Shortcuts

| Shortcut | Action | Notes |
|----------|--------|-------|
| `Ctrl+Z` (Win/Linux)<br>`Cmd+Z` (Mac) | Undo last move | Same as clicking ↶ Undo button |
| `Ctrl+Shift+Z` (Win/Linux)<br>`Cmd+Shift+Z` (Mac) | Redo last undone move | Same as clicking ↷ Redo button |
| `Ctrl+S` (Win/Linux)<br>`Cmd+S` (Mac) | Save game | Same as clicking 💾 Save Game button |

### Implementation

- Shortcuts work globally (anywhere on the page)
- `preventDefault()` prevents browser default actions
- Both Ctrl (Windows/Linux) and Cmd (Mac) are supported
- Case-insensitive key detection

### Adding Custom Shortcuts

Edit [game.js](static/game.js) in the `setupEventListeners` method:
```javascript
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        if (e.key === 'r') {  // Example: Ctrl+R for reset
            e.preventDefault();
            this.resetGame();
        }
    }
});
```

---

## Summary

All these features work together seamlessly to create a polished, professional gaming experience:

1. **Create** custom graphs with the visual editor
2. **Play** with smooth animations and visual feedback
3. **Experiment** freely with undo/redo
4. **Save** your progress for later
5. **Customize** your experience with dark mode and sound settings
6. **Navigate** efficiently with keyboard shortcuts

The modular codebase makes it easy to add even more features in the future!
