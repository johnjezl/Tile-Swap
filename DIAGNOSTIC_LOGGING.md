# Diagnostic Logging Added

## Purpose

To identify why non-host players are loading in preview mode instead of with tiles.

## Changes Made

### Server-Side ([web_app_multiplayer.py:512-515](web_app_multiplayer.py#L512-L515))

Added detailed logging in `handle_start_game()`:

```python
# DIAGNOSTIC: Show exactly what tiles are in room_info
print(f"DEBUG: room_info_data['initial_tiles'] = {room_info_data.get('initial_tiles')}")
print(f"DEBUG: type(room_info_data['initial_tiles']) = {type(room_info_data.get('initial_tiles'))}")
print(f"DEBUG: len(room_info_data['initial_tiles']) = {len(room_info_data.get('initial_tiles', {}))}")
```

### Client-Side

#### In `handleGameStarted()` ([multiplayer.js:262-266](static/multiplayer.js#L262-L266))

```javascript
// DIAGNOSTIC: Check what tiles data we received
console.log('DEBUG: roomInfo.initial_tiles =', roomInfo.initial_tiles);
console.log('DEBUG: typeof roomInfo.initial_tiles =', typeof roomInfo.initial_tiles);
console.log('DEBUG: Object.keys(roomInfo.initial_tiles) =', Object.keys(roomInfo.initial_tiles));
console.log('DEBUG: Object.keys(roomInfo.initial_tiles).length =', Object.keys(roomInfo.initial_tiles).length);
```

#### In `loadMultiplayerGraph()` ([multiplayer.js:462-478](static/multiplayer.js#L462-L478))

```javascript
// DIAGNOSTIC: Log what we're working with
console.log('DEBUG loadMultiplayerGraph: showTilesNow =', showTilesNow);
console.log('DEBUG loadMultiplayerGraph: tiles =', tiles);
console.log('DEBUG loadMultiplayerGraph: typeof tiles =', typeof tiles);
console.log('DEBUG loadMultiplayerGraph: tiles === null?', tiles === null);
console.log('DEBUG loadMultiplayerGraph: tiles === undefined?', tiles === undefined);
console.log('DEBUG loadMultiplayerGraph: hasTiles =', hasTiles);
```

## Testing Instructions

### Step 1: Restart Server

```bash
python web_app_multiplayer.py
```

**CRITICAL:** Server must be restarted for changes to take effect!

### Step 2: Open Browser Consoles

Open console (F12) in **BOTH** browsers BEFORE starting.

### Step 3: Create and Join Room

**Browser 1 (Host):**
1. Create room
2. Click "Ready"

**Browser 2 (Non-Host):**
1. Join room
2. Click "Ready"

### Step 4: Start Game

Host clicks "Start Game"

### Step 5: Analyze Logs

## Expected Server Console Output

```
Starting game in room TILE-XXXX with tiles: {0: 2, 1: 0, 2: 1, ...}
Broadcasting game_started to room TILE-XXXX
Players in room: ['session_abc', 'session_xyz']
Room info state: playing
Room info has tiles: True
DEBUG: room_info_data['initial_tiles'] = {0: 2, 1: 0, 2: 1, ...}
DEBUG: type(room_info_data['initial_tiles']) = <class 'dict'>
DEBUG: len(room_info_data['initial_tiles']) = 6
Game started event broadcast complete
```

**What to check:**
- `initial_tiles` should show actual tile data like `{0: 2, 1: 0, ...}`
- Length should match number of nodes (e.g., 6 for a 6-node graph)
- Type should be `<class 'dict'>`

**Red flags:**
- If `initial_tiles = {}` (empty dict) → Tiles not captured from host
- If `len = 0` → Empty tiles being sent

## Expected Browser Console Output

### Host (Browser 1)

```
Game started event received! {room_info: {...}}
Am I host? true
DEBUG: roomInfo.initial_tiles = {0: 2, 1: 0, 2: 1, ...}
DEBUG: typeof roomInfo.initial_tiles = object
DEBUG: Object.keys(roomInfo.initial_tiles) = ['0', '1', '2', '3', '4', '5']
DEBUG: Object.keys(roomInfo.initial_tiles).length = 6
Host: Revealing tiles
```

### Non-Host (Browser 2) - CRITICAL

```
Game started event received! {room_info: {...}}
Am I host? false
DEBUG: roomInfo.initial_tiles = {0: 2, 1: 0, 2: 1, ...}
DEBUG: typeof roomInfo.initial_tiles = object
DEBUG: Object.keys(roomInfo.initial_tiles) = ['0', '1', '2', '3', '4', '5']
DEBUG: Object.keys(roomInfo.initial_tiles).length = 6
Non-host: Loading graph with tiles
DEBUG loadMultiplayerGraph: showTilesNow = true
DEBUG loadMultiplayerGraph: tiles = {0: 2, 1: 0, 2: 1, ...}
DEBUG loadMultiplayerGraph: typeof tiles = object
DEBUG loadMultiplayerGraph: tiles === null? false
DEBUG loadMultiplayerGraph: tiles === undefined? false
DEBUG loadMultiplayerGraph: hasTiles = true
Loading multiplayer graph with tiles: {0: 2, 1: 0, 2: 1, ...}
Multiplayer graph loaded. Tiles: {0: 2, 1: 0, 2: 1, ...}
```

**What to check:**
- `initial_tiles` should be an object with keys like `['0', '1', '2', ...]`
- `Object.keys(roomInfo.initial_tiles).length` should be > 0
- `hasTiles` should be `true`
- Should see "Loading multiplayer graph with tiles:" NOT "Loading graph preview"

**Red flags:**
- If `initial_tiles = {}` (empty object) → Data not transmitted correctly
- If `Object.keys(roomInfo.initial_tiles).length = 0` → Empty object received
- If `hasTiles = false` → Logic check failing
- If sees "Loading graph preview" → Going to wrong code path

## Diagnosis Based on Logs

### Scenario 1: Server has tiles but client receives empty object

**Server logs:**
```
DEBUG: room_info_data['initial_tiles'] = {0: 2, 1: 0, ...}
DEBUG: len(room_info_data['initial_tiles']) = 6
```

**Client logs:**
```
DEBUG: roomInfo.initial_tiles = {}
DEBUG: Object.keys(roomInfo.initial_tiles).length = 0
```

**Problem:** Serialization issue or Socket.IO not transmitting correctly

**Fix:** Check Flask-SocketIO version, check JSON serialization

---

### Scenario 2: Server has empty tiles

**Server logs:**
```
DEBUG: room_info_data['initial_tiles'] = {}
DEBUG: len(room_info_data['initial_tiles']) = 0
```

**Problem:** Tiles not being captured from host's game state

**Fix:** Check `host_game.graph.tiles` is populated before calling `room.start_game()`

---

### Scenario 3: Client receives tiles but hasTiles = false

**Client logs:**
```
DEBUG: roomInfo.initial_tiles = {0: 2, 1: 0, ...}
DEBUG: Object.keys(roomInfo.initial_tiles).length = 6
DEBUG loadMultiplayerGraph: hasTiles = false
```

**Problem:** Logic error in `hasTiles` check

**Fix:** Check if keys are strings vs numbers, or if check logic is wrong

---

### Scenario 4: Everything looks correct but still goes to preview

**All logs show correct data but still sees:**
```
Loading graph preview (no tiles yet), edges: [...]
```

**Problem:** Race condition or code path issue

**Fix:** Check if there's another code path calling `loadMultiplayerGraph()` with wrong parameters

## What to Report

Please provide:

1. **Full server console output** from "Starting game in room..." to "broadcast complete"
2. **Full non-host browser console output** from "Game started event received!" through all DEBUG lines
3. **Any JavaScript errors** (shown in red in console)

This will pinpoint exactly where the issue is occurring.

---

**Status:** Diagnostic logging in place, ready for testing
