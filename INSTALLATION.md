# Installation Guide

This guide will help you set up and run the Tile Swap game with both the command-line and web interfaces.

## Prerequisites

- **Python 3.7 or higher** installed on your system
- **pip** (Python package installer, usually comes with Python)
- A modern web browser (for web interface)

## Setup Instructions

### 1. Verify Python Installation

Open a terminal/command prompt and run:

```bash
python --version
```

You should see Python 3.7 or higher. If not, download Python from [python.org](https://www.python.org/downloads/).

### 2. Navigate to Project Directory

```bash
cd "h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap"
```

(Adjust the path based on where you cloned/downloaded the project)

### 3. Test Setup (Optional but Recommended)

Run the setup test to check if everything is configured correctly:

```bash
python test_web_setup.py
```

This will verify:
- ✓ All core modules can be imported
- ✓ Required files and directories exist
- ✗ Flask installation status (expected to fail before installation)

### 4. Install Web Dependencies

To use the web interface, install Flask:

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Werkzeug 3.0.1

**Note:** The command-line interface doesn't require any external dependencies!

## Running the Game

### Command-Line Interface

No installation needed! Just run:

```bash
python graph_tile_game.py
```

or the modular version:

```bash
python tile_swap.py
```

### Web Interface

After installing Flask:

```bash
python web_app.py
```

Then open your browser to:
```
http://localhost:5000
```

**Port Already in Use?** Edit `web_app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Use 8080 instead
```

## Verifying Installation

### Quick Test - Command Line

```bash
python graph_tile_game.py
```

Choose option 3 (random graph), enter 5 nodes, then choose option 2 (random tiles). You should be able to play the game!

### Quick Test - Web Interface

1. Start the server:
   ```bash
   python web_app.py
   ```

2. You should see:
   ```
   ==================================================
   TILE SWAP - WEB INTERFACE
   ==================================================

   Starting web server...
   Open your browser to: http://localhost:5000

   Press Ctrl+C to stop the server
   ==================================================
   ```

3. Open http://localhost:5000 in your browser

4. Click "New Random Game"

5. Click on nodes to swap tiles!

## Troubleshooting

### Problem: "python: command not found"

**Solution:** Try using `python3` instead:
```bash
python3 web_app.py
```

### Problem: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Install requirements:
```bash
pip install -r requirements.txt
```

If `pip` doesn't work, try:
```bash
python -m pip install -r requirements.txt
```

### Problem: "Permission denied" when installing packages

**Solution:** Use a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python web_app.py
```

### Problem: Web interface shows blank page

**Solution:**
1. Check that `templates/` and `static/` directories exist
2. Make sure you're running from the project root directory
3. Check browser console for JavaScript errors (F12 -> Console tab)

### Problem: "Address already in use"

**Solution:** Another program is using port 5000. Either:
1. Stop the other program, or
2. Change the port in `web_app.py` to 8080 or another number

## Uninstallation

To remove only the web dependencies:

```bash
pip uninstall flask werkzeug
```

To remove everything (if using virtual environment):

```bash
# Deactivate virtual environment
deactivate

# Delete the venv folder
rm -rf venv  # Mac/Linux
rmdir /s venv  # Windows
```

## Next Steps

Once installed, check out these guides:

- **README.md** - Complete game documentation and features
- **WEB_INTERFACE_GUIDE.md** - Detailed web interface architecture
- **CLAUDE CODE SESSION.md** - Development history and prompts used

Enjoy playing Tile Swap!
