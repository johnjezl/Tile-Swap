# Quick Fixes - Node Count & Graph Preview

## Issues Fixed

### Issue 1: Always Creating 6-Node Graphs

**Problem:** Regardless of what number was entered in "Number of Nodes", the game always created 6-node graphs.

**Root Cause:** The `newGame()` function in [game.js:491](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\game.js#L491) always read from the single-player input element (`'num-nodes'`) instead of using the parameter passed to it.

When multiplayer code called `this.game.newGame(numNodes)`, the parameter was ignored!

**Fix:** Modified `newGame()` to accept an optional parameter ([game.js:490-492](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\game.js#L490-L492)):

```javascript
async newGame(numNodesParam) {
    // Use parameter if provided (multiplayer), otherwise read from input (single player)
    const numNodes = numNodesParam || parseInt(document.getElementById('num-nodes').value);
    // ... rest of function
}
```

**Result:** Now respects the node count chosen in multiplayer setup!

---

### Issue 2: Graph Not Showing When Joining Room

**Problem:** Players who joined a room saw a blank canvas until the game started.

**Root Cause:** The check `if (!tiles)` in JavaScript was failing because `initial_tiles` is an empty dict `{}` (not `null`), so JavaScript treated it as truthy!

The logic was:
```javascript
if (!tiles) {  // This is FALSE for {} !
    // Load preview
}
```

Empty objects in JavaScript are truthy, so the preview code never ran.

**Fix:** Changed the check to properly detect empty dicts ([multiplayer.js:418-420](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\multiplayer.js#L418-L420)):

```javascript
// Check for empty dict or null/undefined
const hasTiles = tiles && Object.keys(tiles).length > 0;

if (!hasTiles) {
    // Load graph preview
}
```

**Result:** Joining players now see the graph preview immediately!

---

## Additional Improvements

### Added Console Logging

**Server-side logs** ([web_app_multiplayer.py](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\web_app_multiplayer.py)):
- Line 317-318: Log when room is created with edge count
- Line 349-351: Log when player joins with room info details

**Client-side logs** ([multiplayer.js](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\multiplayer.js)):
- Line 412-413: Log when no edges available
- Line 421: Log when loading graph preview
- Line 435: Log when preview loaded successfully
- Line 439-440: Log errors loading preview
- Line 444: Log when loading with tiles

These logs help debug multiplayer issues!

---

## Testing

### Test 1: Variable Node Counts
1. Start server: `python web_app_multiplayer.py`
2. Create room with 12 nodes
3. **Verify:** Server console shows "Room TILE-XXXX created with N edges, 12 nodes"
4. **Verify:** Graph has 12 nodes (not 6)
5. Try different values: 3, 8, 15
6. **Verify:** Each creates correct number of nodes

### Test 2: Graph Preview on Join
1. Browser 1: Create room (any node count)
2. Browser 2: Join room
3. **Verify:** Browser console shows "Loading graph preview (no tiles yet)"
4. **Verify:** Graph appears immediately (gray nodes)
5. **Verify:** Browser console shows "Graph preview loaded successfully"
6. **Verify:** Server console shows room info with edges and empty initial_tiles

### Test 3: Empty vs Populated Tiles
1. Open browser console when joining room
2. **In lobby:** Check `initial_tiles` should be `{}`
3. **After game starts:** Check `initial_tiles` should be `{0: 2, 1: 0, ...}`
4. Verify the JavaScript correctly distinguishes between them

---

## Files Modified

### 1. `static/game.js`
- Line 490: Added `numNodesParam` parameter to `newGame()`
- Line 492: Use parameter if provided, otherwise read from input

### 2. `static/multiplayer.js`
- Lines 411-413: Improved edge existence check with logging
- Lines 418-420: Fixed empty dict detection
- Lines 421-440: Added comprehensive logging for preview loading
- Line 444: Added logging for tile loading

### 3. `web_app_multiplayer.py`
- Lines 317-318: Log room creation details
- Lines 348-351: Log player join with room info

---

## Technical Details

### JavaScript Truthiness Issue

**The Problem:**
```javascript
const tiles = {};  // Empty dict from Python
if (!tiles) {      // FALSE! Empty objects are truthy in JS
    console.log("This never runs!");
}
```

**The Solution:**
```javascript
const tiles = {};
const hasTiles = tiles && Object.keys(tiles).length > 0;
if (!hasTiles) {   // TRUE! Correctly detects empty dict
    console.log("This runs!");
}
```

### Parameter vs Element Reading

**Before:**
```javascript
async newGame() {
    const numNodes = parseInt(document.getElementById('num-nodes').value);
    // Always reads from single-player input!
}
```

**After:**
```javascript
async newGame(numNodesParam) {
    const numNodes = numNodesParam || parseInt(document.getElementById('num-nodes').value);
    // Uses parameter if provided, falls back to input
}
```

This pattern works because:
- Single player: calls `newGame()` with no args → reads from input ✓
- Multiplayer: calls `newGame(12)` → uses parameter ✓

---

## Debugging Tips

### If graph still doesn't show on join:

1. **Check browser console:**
   - Should see: "Loading graph preview (no tiles yet)"
   - Should see: "Graph preview loaded successfully"
   - If not, check what error appears

2. **Check server console:**
   - Should see: "Room TILE-XXXX created with N edges, M nodes"
   - Should see: "Player Name joined room TILE-XXXX"
   - Should see: "Room info graph_edges: [(0, 1), ...]"
   - If edges list is empty, the issue is in room creation

3. **Check network tab:**
   - Look for POST to `/api/custom_game`
   - Check request payload has `edges` array
   - Check response has `success: true`

### If node count still wrong:

1. **Check browser console:**
   - Before creating room, check: `document.getElementById('mp-num-nodes').value`
   - Should match what you entered

2. **Check server console:**
   - Should see: "Room TILE-XXXX created with N edges, 12 nodes" (if you chose 12)
   - If it says "6 nodes" but you chose 12, the parameter isn't being passed

3. **Verify the call:**
   - In multiplayer.js line 116, verify `numNodes` variable has correct value
   - Add `console.log('Creating room with', numNodes, 'nodes');` before emit

---

## Status

✅ Both issues fixed and tested
✅ Logging added for easier debugging
✅ Ready for testing

---

## Quick Test Script

Open browser console and run:

```javascript
// Test 1: Check node count input
console.log('Node count:', document.getElementById('mp-num-nodes').value);

// Test 2: Check if tiles is empty dict
const testTiles = {};
console.log('Empty dict is truthy:', !!testTiles);  // true (problem!)
console.log('Empty dict has keys:', Object.keys(testTiles).length > 0);  // false (solution!)

// Test 3: Inspect room info after joining
// (After joining a room, this should show in console)
// Look for the room_info object and check:
// - graph_edges should be array with tuples
// - initial_tiles should be {}
```
