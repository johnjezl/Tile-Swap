# Multiplayer Debugging & Testing Guide

## Recent Fixes

### Fix 1: Ready Status Indicators

**Problem:** Host couldn't see which players were ready.

**Solution:**
- Added `ready` field to player info in leaderboard ([multiplayer.py:168](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\multiplayer.py#L168))
- Updated lobby UI to show "✓ Ready" (green) or "⏳ Not Ready" (amber) ([multiplayer.js:312-314](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\multiplayer.js#L312-L314))

**Visual:**
```
Lobby Players:
Alice (Host) (You)     ✓ Ready    (green)
Bob                    ⏳ Not Ready (amber)
Charlie                ✓ Ready    (green)
```

---

### Fix 2: Game Start Event Debugging

**Problem:** Game might not be starting for non-host players.

**Solution:** Added comprehensive logging to diagnose the issue.

**Server Logs Added:**
- Room creation with socket ID
- Player joins with socket ID and session ID
- Game start broadcast with player list
- Broadcast completion confirmation

**Client Logs Added:**
- Game started event received
- Host vs non-host detection
- Graph loading with tiles

---

## Testing the Multiplayer System

### Test 1: Ready Indicators

**Steps:**
1. Start server: `python web_app_multiplayer.py`
2. Open Browser 1: Create room
3. Open Browser 2: Join room

**Expected in Browser 1 (Host):**
```
Players:
YourName (Host) (You)     ⏳ Not Ready
Player2                   ⏳ Not Ready
```

**Click "Ready" in Browser 1:**
```
Players:
YourName (Host) (You)     ✓ Ready
Player2                   ⏳ Not Ready
```

**Click "Ready" in Browser 2:**
```
Players:
YourName (Host) (You)     ✓ Ready
Player2                   ✓ Ready

[Start Game] button appears
```

---

### Test 2: Game Start Synchronization

**Steps:**
1. Both players ready (from Test 1)
2. Host clicks "Start Game"
3. **Open browser console in BOTH windows** (F12)

**Expected Server Console:**
```
Host socket abc123 created and joined room TILE-XXXX
Room TILE-XXXX created with 11 edges, 6 nodes
Graph edges: [(0, 1), (1, 2), ...]

Socket def456 joined room TILE-XXXX
Player Player2 (session xyz789) joined room TILE-XXXX
Room info graph_edges: [(0, 1), (1, 2), ...]
Room info initial_tiles: {}

Starting game in room TILE-XXXX with tiles: {0: 2, 1: 0, ...}
Broadcasting game_started to room TILE-XXXX
Players in room: ['session_abc', 'session_xyz']
Game started event broadcast complete
```

**Expected Browser 1 Console (Host):**
```
Game started event received! {room_info: {...}}
Am I host? true
Host: Revealing tiles
```

**Expected Browser 2 Console (Non-Host):**
```
Game started event received! {room_info: {...}}
Am I host? false
Non-host: Loading graph with tiles
Loading multiplayer graph with tiles: {0: 2, 1: 0, ...}
Multiplayer graph loaded. Tiles: {0: 2, 1: 0, ...}
```

---

## Troubleshooting

### Issue: Non-Host Doesn't Receive game_started Event

**Symptoms:**
- Server console shows "Game started event broadcast complete"
- Host browser console shows "Game started event received!"
- **Non-host browser console shows NOTHING**

**Diagnosis:**

1. **Check if player joined socket.io room:**
   - Look for server log: `Socket def456 joined room TILE-XXXX`
   - If missing, the socket.io `join_room()` call failed

2. **Check session vs socket mismatch:**
   - Session ID used for game logic
   - Socket ID used for socket.io rooms
   - Both should be tracked in `session_rooms` dict

3. **Verify socket connection:**
   - Non-host console should show: `Connected to server: session_xyz`
   - If missing, socket.io connection failed

**Fix:**
The socket.io `join_room()` uses `request.sid` (the socket ID), which is different from `session_id` (the Flask session ID). This should work correctly, but verify the logs show both IDs.

---

### Issue: game_started Event Received But Nothing Happens

**Symptoms:**
- Browser console shows "Game started event received!"
- No visual change (lobby still visible)
- No tiles appear

**Diagnosis:**

1. **Check if handleGameStarted is actually running:**
   - Should see: `Am I host? false` (or true)
   - If missing, event handler isn't executing

2. **Check for JavaScript errors:**
   - Open browser console
   - Look for red error messages
   - Common: `Cannot read property of undefined`

3. **Check if room_info has data:**
   - Console log should show full room_info object
   - Verify `graph_edges` is populated
   - Verify `initial_tiles` has tile data

**Fix:**
If `initial_tiles` is empty `{}`, the game hasn't properly stored the host's tiles. Check server log: "Starting game in room TILE-XXXX with tiles: {...}" should show actual tiles, not `{}`.

---

### Issue: Ready Button Doesn't Update

**Symptoms:**
- Click "Ready" button
- Status doesn't change to "✓ Ready"
- Other players don't see update

**Diagnosis:**

1. **Check WebSocket connection:**
   - Console should show: `Connected to server: session_xyz`

2. **Check toggle_ready event:**
   - Add log in `handlePlayerReadyChanged`:
     ```javascript
     handlePlayerReadyChanged(data) {
         console.log('Player ready changed:', data);
         this.updateLobby(data.room_info);
     }
     ```

3. **Check server receives event:**
   - Server should have handler for `toggle_ready`
   - Check if `@socketio.on('toggle_ready')` exists

**Fix:**
The ready toggle uses socket.io events. Ensure WebSocket connection is active.

---

## Common Scenarios

### Scenario 1: Three Players, One Not Ready

```
Browser 1 (Host):    ✓ Ready
Browser 2:           ✓ Ready
Browser 3:           ⏳ Not Ready
```

**Expected:** Start Game button does NOT appear

**Why:** `room.all_players_ready()` returns `False`

**Action:** Player 3 must click "Ready"

---

### Scenario 2: All Ready, Host Clicks Start

**Timeline:**

```
T+0s: Host clicks "Start Game"
      ↓
T+0.1s: Server receives start_game event
      ↓
T+0.2s: Server extracts host's tiles: {0: 2, 1: 0, ...}
      ↓
T+0.3s: Server calls room.start_game(edges, tiles)
      ↓
T+0.4s: Server broadcasts game_started to room
      ↓
T+0.5s: ALL browsers receive game_started
        - Host: Shows tiles (already has graph)
        - Players: Load graph + tiles via API
      ↓
T+0.7s: All players see game board with tiles
        Game begins!
```

---

### Scenario 3: Player Joins After Start

```
Player tries to join room TILE-XXXX
      ↓
Server checks: room.state != LOBBY
      ↓
Server emits: join_failed
      ↓
Player sees: "Room is full or game already started"
```

**Expected:** Cannot join after game starts

---

## Debugging Checklist

When game doesn't start for non-host:

- [ ] Server logs show room creation
- [ ] Server logs show host socket joined room
- [ ] Server logs show player socket joined room
- [ ] Both browsers show "Connected to server"
- [ ] Ready indicators work for all players
- [ ] All players show "✓ Ready"
- [ ] Start button appears for host
- [ ] Host console shows "Game started event received!"
- [ ] Player console shows "Game started event received!"
- [ ] Server shows "Broadcasting game_started to room TILE-XXXX"
- [ ] Server shows "Players in room: [...]" with all session IDs
- [ ] Player console shows "Non-host: Loading graph with tiles"
- [ ] Player console shows "Multiplayer graph loaded. Tiles: {...}"
- [ ] Both browsers show the game board
- [ ] Tiles match in both browsers

If ANY checkbox fails, that's where the issue is!

---

## Manual Socket.io Testing

Open browser console and test socket.io directly:

```javascript
// Check if socket connected
console.log('Socket ID:', window.multiplayerClient.socket.id);
console.log('Connected:', window.multiplayerClient.socket.connected);

// Manually emit game_started (for testing)
window.multiplayerClient.socket.emit('start_game');

// Listen for events manually
window.multiplayerClient.socket.on('test_event', (data) => {
    console.log('Received test event:', data);
});

// Check current room
console.log('Current room:', window.multiplayerClient.currentRoom);
console.log('Is host:', window.multiplayerClient.isHost);
console.log('Is ready:', window.multiplayerClient.isReady);
```

---

## Network Tab Debugging

**Chrome DevTools → Network → WS (WebSockets)**

Look for:
- Connection to `/socket.io/?EIO=4&transport=websocket`
- Messages tab shows outgoing/incoming events
- Search for "game_started" in messages
- Verify message sent to correct room

**What to check:**
1. **Outgoing (Client → Server):**
   - `create_room` with player name and mode
   - `join_room` with room code
   - `toggle_ready` with ready: true
   - `start_game` (host only)

2. **Incoming (Server → Client):**
   - `connected` with session_id
   - `room_created` or `room_joined`
   - `player_ready_changed`
   - `game_started` **← This is the critical one!**

---

## Quick Fix: Force Refresh

If things seem broken:

1. **Stop server:** Ctrl+C
2. **Clear browser cache:** Ctrl+Shift+Delete
3. **Restart server:** `python web_app_multiplayer.py`
4. **Hard refresh browsers:** Ctrl+Shift+R
5. **Try again**

This clears:
- Cached JavaScript files
- Old socket.io connections
- Stale session data

---

## Success Indicators

**✅ Everything Working:**

**Server Console:**
```
Room TILE-A1B2 created with 11 edges, 6 nodes
Socket abc123 joined room TILE-A1B2
Socket def456 joined room TILE-A1B2
Broadcasting game_started to room TILE-A1B2
Players in room: ['session1', 'session2']
Game started event broadcast complete
```

**Host Browser Console:**
```
Connected to server: session1
Game started event received!
Am I host? true
Host: Revealing tiles
```

**Player Browser Console:**
```
Connected to server: session2
Loading graph preview (no tiles yet), edges: [...]
Graph preview loaded successfully
Game started event received!
Am I host? false
Non-host: Loading graph with tiles
Loading multiplayer graph with tiles: {0: 2, 1: 0, ...}
Multiplayer graph loaded. Tiles: {0: 2, 1: 0, ...}
```

**Both Browsers:**
- See identical game boards
- See identical tile arrangements
- Can make swaps
- Move counters update
- Leaderboard updates in real-time

---

**Status:** Debugging tools in place, ready to diagnose any multiplayer issues!
