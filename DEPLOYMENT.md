# Tile Swap Multiplayer - Deployment Guide

This guide explains how to deploy and run the Tile Swap multiplayer game for your class.

## Quick Start (Local Network)

Perfect for a classroom setting where all students are on the same WiFi network.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python web_app_multiplayer.py
```

You should see:
```
==================================================
TILE SWAP - WEB INTERFACE (MULTIPLAYER)
==================================================

Starting web server with WebSocket support...
Open your browser to: http://localhost:5000

Features:
  - Single player mode
  - Competitive multiplayer (up to 30 players)
  - Real-time and turn-based modes

Press Ctrl+C to stop the server
==================================================
```

### 3. Find Your IP Address

Students need to connect to your computer's local IP address.

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" under your WiFi adapter (e.g., `192.168.1.100`)

**Mac/Linux:**
```bash
ifconfig
```
Look for "inet" address under your WiFi adapter (e.g., `192.168.1.100`)

### 4. Share the URL

Tell students to open their browsers to:
```
http://YOUR_IP_ADDRESS:5000
```

For example: `http://192.168.1.100:5000`

## Firewall Configuration

If students can't connect, you may need to allow port 5000 through your firewall.

**Windows Firewall:**
1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Select "Port" → Next
5. TCP, Port 5000 → Next
6. Allow the connection → Next
7. Check all profiles → Next
8. Name it "Tile Swap Game" → Finish

**Mac Firewall:**
1. System Preferences → Security & Privacy → Firewall
2. Click "Firewall Options"
3. Click "+" and add Python
4. Set to "Allow incoming connections"

**Linux (UFW):**
```bash
sudo ufw allow 5000/tcp
```

## Cloud Deployment (Optional)

For running the game outside a classroom or for remote students.

### Option 1: Render.com (Free Tier Available)

1. Create a free account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python web_app_multiplayer.py`
   - **Environment:** Python 3
5. Click "Create Web Service"
6. Your game will be available at `https://your-app-name.onrender.com`

**Note:** Free tier may sleep after inactivity. Upgrade to paid tier for 24/7 availability.

### Option 2: Railway.app

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and installs requirements
5. Game available at the provided URL

### Option 3: DigitalOcean App Platform

1. Create account at [digitalocean.com](https://digitalocean.com)
2. Apps → Create App
3. Select your GitHub repository
4. Choose "Basic" plan ($5/month)
5. Deploy

### Option 4: Heroku

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create `Procfile` in project root:
   ```
   web: python web_app_multiplayer.py
   ```
3. Create `runtime.txt`:
   ```
   python-3.11.0
   ```
4. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

## Production Configuration

### Environment Variables

For production, set these environment variables:

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
```

**Windows:**
```bash
set FLASK_ENV=production
set SECRET_KEY=your-secret-key-here
```

### HTTPS (Recommended for Production)

Most cloud platforms (Render, Railway, Heroku) provide HTTPS automatically.

For self-hosting with HTTPS, use a reverse proxy like Nginx or use Flask-Talisman.

### Server Configuration

Edit `web_app_multiplayer.py` line 460 to customize:

```python
socketio.run(app,
    debug=False,          # Set to False in production
    host='0.0.0.0',       # Allow external connections
    port=5000             # Change port if needed
)
```

## Usage Instructions for Students

### Joining a Game

1. Open the game URL in your browser
2. Click "Multiplayer" tab
3. Enter your name
4. Either:
   - **Create Room:** Choose game mode and click "Create Room"
   - **Join Room:** Enter room code (e.g., TILE-A1B2) and click "Join"

### Room Codes

- Format: `TILE-XXXX` (e.g., `TILE-A1B2`)
- Host shares this code with other players
- Codes are temporary and expire when room is empty

### Game Modes

**Real-Time Race:**
- All players solve simultaneously
- First to finish wins
- Live leaderboard shows everyone's progress

**Turn-Based:**
- Players take turns making moves
- One swap per turn
- Turn order randomized at start
- Turn indicator shows whose turn it is

### Starting a Game

1. All players click "Ready"
2. Host clicks "Start Game" when everyone is ready
3. Game begins with same graph for all players

## Troubleshooting

### Students Can't Connect

**Check these:**
1. Is the server running? (Should see console output)
2. Are you on the same WiFi network?
3. Is the IP address correct? (Run `ipconfig` or `ifconfig` again)
4. Is port 5000 allowed through firewall?
5. Try accessing from server computer first: `http://localhost:5000`

### WebSocket Connection Failed

**Browser console shows WebSocket errors:**
- Check that Flask-SocketIO is installed: `pip list | grep Flask-SocketIO`
- Ensure you're running `web_app_multiplayer.py`, not `web_app.py`
- Try a different browser (Chrome/Firefox recommended)
- Check browser console for specific error messages

### Room Code Not Working

- Codes are case-sensitive (though auto-converted to uppercase)
- Codes expire when last player leaves
- Room may be full (30 player maximum)
- Game may have already started

### Sound Not Working

- Click anywhere on the page first (browser security requirement)
- Check browser audio permissions
- Check system volume/audio output device
- Try different browser

### Game Feels Slow

**For many players:**
- Use faster hardware for server
- Consider cloud deployment
- Ensure good WiFi signal for all players

### Players Getting Disconnected

- Check WiFi stability
- Ensure server computer doesn't sleep
- Consider cloud deployment for better reliability

## Performance Tips

### For 30-Player Games

1. **Use wired connection** for server if possible
2. **Close unnecessary programs** on server computer
3. **Use modern browsers** (Chrome, Firefox, Safari, Edge)
4. **Good WiFi coverage** for all students
5. **Consider smaller graphs** (6-8 nodes) for large groups

### Recommended Hardware

- **Minimum:** 4GB RAM, dual-core CPU, WiFi
- **Recommended:** 8GB RAM, quad-core CPU, wired ethernet
- **For cloud:** Use at least the $5-10/month tier

## Monitoring

### Server Console Output

The server shows:
- Player connections/disconnections
- Room creation/deletion
- WebSocket events

### Active Rooms

To see active rooms, add this endpoint to `web_app_multiplayer.py`:

```python
@app.route('/api/stats')
def stats():
    return jsonify({
        'active_rooms': mp_manager.get_active_rooms_count(),
        'total_players': mp_manager.get_total_players_count()
    })
```

Access at: `http://your-url:5000/api/stats`

## Backup Plan

If multiplayer isn't working, students can still play single-player mode:
1. Each student runs their own server: `python web_app_multiplayer.py`
2. Access at `http://localhost:5000`
3. Click "Single Player" tab
4. Play independently

## Security Notes

### For Classroom Use (Local Network)
- Default configuration is fine
- No sensitive data transmitted
- Connections limited to local network

### For Public Internet
- Change `SECRET_KEY` in `web_app_multiplayer.py` (line 16)
- Use HTTPS (automatic with cloud platforms)
- Consider adding rate limiting
- Monitor for abuse

## Support

### Common Commands

**Check if server is running:**
```bash
# Windows
netstat -an | findstr 5000

# Mac/Linux
lsof -i :5000
```

**Stop the server:**
- Press `Ctrl+C` in the terminal running the server

**Restart the server:**
- Stop with `Ctrl+C`
- Run `python web_app_multiplayer.py` again

**Clear all rooms:**
- Restart the server (all rooms are in-memory)

## Testing Multiplayer Locally

You can test with multiple browser windows:

1. Start server: `python web_app_multiplayer.py`
2. Open multiple tabs/windows to `http://localhost:5000`
3. Use different names in each window
4. Create room in one, join in others
5. Test both game modes

## Architecture Overview

```
┌─────────────┐
│   Student   │───┐
│  Browser 1  │   │
└─────────────┘   │
                  │
┌─────────────┐   │     ┌──────────────┐
│   Student   │───┼────▶│ Flask Server │
│  Browser 2  │   │     │  + SocketIO  │
└─────────────┘   │     └──────────────┘
                  │           │
┌─────────────┐   │           ▼
│   Student   │───┘     ┌──────────────┐
│  Browser 3  │         │ Game Rooms   │
└─────────────┘         │  (in-memory) │
                        └──────────────┘
```

- **Central server** manages all game state
- **WebSocket** connections for real-time updates
- **HTTP** for initial page load and single-player API
- **In-memory storage** (rooms cleared on restart)

## License & Credits

Created for CS 415 - Algorithm Analysis class extra credit project.

The multiplayer system supports competitive play for analyzing the efficiency of different solving strategies.

---

**Ready to play?** Run `python web_app_multiplayer.py` and share the URL with your class!
