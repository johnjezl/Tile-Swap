# Quick Start Guide - Enhanced Web Interface

Get up and running with the enhanced Tile Swap game in minutes!

## Installation

### 1. Install Flask

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python web_app.py
```

### 3. Open Your Browser

Navigate to: **http://localhost:5000**

That's it! You're ready to play.

---

## First Game (5-Minute Tutorial)

### Step 1: Create a Random Game

1. Look at the left panel under "Game Setup"
2. Set "Number of Nodes" to **6** (default)
3. Click **"New Random Game"**
4. A graph with 6 nodes appears on the canvas

### Step 2: Understand the Display

**Node Colors:**
- **Green** = Tile matches node number (goal!)
- **Blue** = Tile doesn't match (needs swapping)

**Node Labels:**
- Top text = Node number
- Bottom number = Current tile number

**Goal:** Make all nodes green by swapping tiles!

### Step 3: Make Your First Move

1. Click on any blue node (it gets a yellow outline)
2. Click on a connected blue node
3. Watch the tiles smoothly animate as they swap!
4. The move counter increases

### Step 4: Use Undo if Needed

Made a mistake? Click the **↶ Undo** button to reverse your last move.

Want to try again? Click **↷ Redo** to reapply it.

### Step 5: Solve the Puzzle

Keep swapping until all nodes are green!

When you win:
- A victory message appears
- Victory music plays
- Your score is compared to the optimal solution

---

## Exploring Advanced Features

### Try the Graph Editor

1. Click **"Custom Graph Editor"**
2. Click anywhere to add nodes
3. Drag from one node to another to connect them
4. Right-click a node to delete it
5. Make sure it says "✓ Connected" at the bottom
6. Click **"Start Game"**

Now you're playing your own custom puzzle!

### Toggle Dark Mode

Click the **🌙** button in the top-right corner.

Your eyes will thank you! (Preference is saved automatically)

### Save Your Progress

1. Click **💾 Save Game**
2. A JSON file downloads
3. Come back later and click **📂 Load Game**
4. Select your saved file
5. Continue where you left off!

### Use Keyboard Shortcuts

- `Ctrl+Z` - Undo
- `Ctrl+Shift+Z` - Redo
- `Ctrl+S` - Save game

(Use `Cmd` instead of `Ctrl` on Mac)

### Adjust Sound

Don't like the sound effects? Uncheck **"Sound Effects"** in the Game Status section.

---

## Tips for Success

### Strategy Tips

1. **Plan ahead** - Look at the entire graph before making moves
2. **Focus on cycles** - Tiles often form circular patterns
3. **Use undo liberally** - Experiment without fear!
4. **Check the optimal count** - Try to beat or match it

### Graph Editor Tips

1. **Start simple** - Try a triangle (3 nodes, 3 edges) first
2. **Make it connected** - Every node must have at least one edge
3. **More edges = easier** - More swap options available
4. **Fewer edges = harder** - More constrained puzzle

### Interface Tips

1. **Use keyboard shortcuts** - Much faster than clicking
2. **Save interesting graphs** - Reuse them later
3. **Try dark mode** - Better for long sessions
4. **Watch the animations** - They help visualize the swaps

---

## Troubleshooting

### "Failed to connect to server"

Make sure the Flask server is running:
```bash
python web_app.py
```

### Port 5000 already in use

Edit `web_app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

Then visit http://localhost:8080

### Sound doesn't work

- Check your browser supports Web Audio API (all modern browsers do)
- Make sure "Sound Effects" is checked
- Check your system volume

### Dark mode doesn't persist

Make sure your browser allows localStorage:
- Chrome: Settings → Privacy → Cookies (allow all)
- Firefox: Options → Privacy → Cookies (standard)

### Save/load doesn't work

- Make sure pop-ups are allowed
- Check file permissions in your browser
- Try downloading to a different folder

---

## What's Next?

### Learn More

- [ENHANCED_FEATURES.md](ENHANCED_FEATURES.md) - Detailed feature documentation
- [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md) - Architecture overview
- [README.md](README.md) - Complete project documentation

### Challenge Yourself

1. Try to solve a 10-node graph optimally
2. Create a specific graph topology (like a binary tree)
3. Beat your previous score on the same graph
4. Create the hardest possible 6-node graph

### Share with Friends

1. Save an interesting graph configuration
2. Send the JSON file to a friend
3. Compare your solutions!

---

## Summary

**Basic Flow:**
1. New Random Game → Play → Win
2. Custom Graph Editor → Create → Play → Win
3. Save Game → Load Game → Continue

**Key Features:**
- 🎨 Custom graph editor
- ↶↷ Undo/redo
- 💾📂 Save/load
- 🌙 Dark mode
- 🔊 Sound effects
- ⌨️ Keyboard shortcuts

**Have fun solving puzzles!** 🎮✨
