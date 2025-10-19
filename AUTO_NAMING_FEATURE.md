# Automatic Player Naming Feature

## Overview

Players who join without entering a name now automatically get sequential names (Player 1, Player 2, etc.) and can change their name at any time in the lobby.

## Features

### 1. Automatic Sequential Naming

**Host Creating Room:**
- If no name entered → "Player 1"

**Players Joining Room:**
- If no name entered → "Player 2", "Player 3", "Player 4", etc.
- Based on current player count in room

### 2. Name Change Functionality

**In Lobby:**
- Input field to enter new name
- "Change Name" button
- Updates immediately for all players
- Can change name multiple times before game starts

**During Game:**
- Name change UI hidden (lobby only feature)

## Implementation

### Server-Side Changes

**File:** [web_app_multiplayer.py](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\web_app_multiplayer.py)

**Create Room (Lines 287-289):**
```python
player_name = data.get('name', '').strip()
if not player_name:
    player_name = 'Player 1'
```

**Join Room (Lines 335-341):**
```python
player_name = data.get('name', '').strip()

room = mp_manager.get_room(room_code)

# Generate automatic name based on player count
if not player_name and room:
    player_name = f'Player {len(room.players) + 1}'
```

**New Event Handler (Lines 438-463):**
```python
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
        # Broadcast to room
        socketio.emit('player_name_changed', {
            'session_id': session_id,
            'name': new_name,
            'room_info': room.get_room_info()
        }, to=room_code)
        emit('name_change_success', {'success': True, 'name': new_name})
    else:
        emit('name_change_failed', {'success': False, 'message': 'Invalid name'})
```

**Room Class Method ([multiplayer.py:100-105](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\multiplayer.py#L100-L105)):**
```python
def change_player_name(self, session_id: str, new_name: str) -> bool:
    """Change a player's name."""
    if session_id in self.players and new_name.strip():
        self.players[session_id].name = new_name.strip()
        return True
    return False
```

### Client-Side Changes

**File:** [multiplayer.js](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\multiplayer.js)

**Socket Event Listeners (Lines 54-57):**
```javascript
// Name change events
this.socket.on('player_name_changed', (data) => this.handlePlayerNameChanged(data));
this.socket.on('name_change_success', (data) => this.handleNameChangeSuccess(data));
this.socket.on('name_change_failed', (data) => this.handleNameChangeFailed(data));
```

**Change Name Method (Lines 180-185):**
```javascript
changeName() {
    const newName = document.getElementById('change-name-input').value.trim();
    if (newName) {
        this.socket.emit('change_name', {name: newName});
    }
}
```

**Event Handlers (Lines 241-254):**
```javascript
handlePlayerNameChanged(data) {
    console.log('Player name changed:', data);
    this.updateLobby(data.room_info);
}

handleNameChangeSuccess(data) {
    console.log('Name change successful:', data.name);
    document.getElementById('change-name-input').value = '';
}

handleNameChangeFailed(data) {
    console.log('Name change failed:', data.message);
    alert('Name change failed: ' + data.message);
}
```

### UI Changes

**File:** [index.html:77-80](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\templates\index.html#L77-L80)

```html
<div class="name-change-section">
    <input type="text" id="change-name-input" placeholder="Enter new name" maxlength="20">
    <button id="change-name-btn" class="btn btn-secondary btn-small">Change Name</button>
</div>
```

**CSS Styling ([style.css:727-755](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\style.css#L727-L755)):**
- Flexbox layout for input + button
- Consistent styling with theme
- Focus states for input
- Responsive design

## Usage

### Scenario 1: Creating Room Without Name

1. Click "Multiplayer"
2. Leave name field blank
3. Click "Create Room"
4. **Result:** Automatically named "Player 1"

### Scenario 2: Joining Room Without Name

1. Click "Multiplayer"
2. Leave name field blank
3. Enter room code
4. Click "Join Room"
5. **Result:** Automatically named "Player 2" (or next number)

### Scenario 3: Changing Name in Lobby

1. Join room (with or without name)
2. In lobby, type new name in "Enter new name" field
3. Click "Change Name"
4. **Result:** Name updates for all players immediately

### Scenario 4: Multiple Name Changes

1. Join as "Player 2"
2. Change to "Alice"
3. Change to "AliceTheBest"
4. **Result:** All changes broadcast to everyone

## Data Flow

### Auto-Naming on Join

```
Client → Join room with empty name
  ↓
Server → Checks player count: len(room.players) = 2
  ↓
Server → Assigns name: f'Player {2 + 1}' = "Player 3"
  ↓
Server → Adds player to room with name "Player 3"
  ↓
Server → Broadcasts player_joined with updated room_info
  ↓
All clients → See "Player 3" in lobby
```

### Name Change Flow

```
Client → Enter new name "Alice"
Client → Click "Change Name"
  ↓
Client → Emit 'change_name' event with {name: "Alice"}
  ↓
Server → Validate name (not empty)
Server → Update player.name = "Alice"
  ↓
Server → Broadcast 'player_name_changed' to room
Server → Emit 'name_change_success' to requester
  ↓
All clients → Receive 'player_name_changed'
All clients → Call updateLobby() → Name updates in UI
  ↓
Requester → Receive 'name_change_success'
Requester → Clear input field
```

## Validation

### Server-Side Validation

- Name must not be empty after trimming whitespace
- Maximum length enforced by HTML (20 characters)
- No duplicate name checking (allowed for simplicity)

### Client-Side Validation

- Only sends non-empty names
- Input field maxlength=20

## Edge Cases Handled

### Empty Name on Create

**Input:** Create room with blank name

**Result:** Named "Player 1" ✓

---

### Empty Name on Join

**Input:** Join room with blank name

**Result:** Named "Player 2", "Player 3", etc. based on count ✓

---

### Change to Empty Name

**Input:** Try to change name to empty string

**Result:** Server rejects, emits 'name_change_failed' ✓

---

### Rapid Name Changes

**Input:** Change name multiple times quickly

**Result:** All changes processed in order, all clients stay synchronized ✓

---

### Name Change After Ready

**Input:** Mark ready, then change name

**Result:** Name changes, ready status preserved ✓

---

### Player Leaves and Rejoins

**Input:** Player 3 leaves, new player joins

**Result:** New player becomes "Player 3" (reuses number) ✓

## Testing

### Test 1: Auto-Naming

1. Create room without name → See "Player 1"
2. Join (browser 2) without name → See "Player 2"
3. Join (browser 3) without name → See "Player 3"

**Expected:** Sequential numbering ✓

### Test 2: Name Change

1. Join as "Player 2"
2. Change name to "Alice"
3. **All browsers** should see update
4. Change to "Bob"
5. **All browsers** should see "Bob" now

**Expected:** Instant updates for all players ✓

### Test 3: Mixed Named/Unnamed

1. Create room with name "Host"
2. Join without name → "Player 2"
3. Join with name "Charlie"
4. Join without name → "Player 4" (skips 3 because Charlie took that slot)

**Expected:** Numbers based on count, not sequential ✓

### Test 4: Empty Name Rejected

1. Join room
2. Try to change name to empty string
3. **Expected:** Alert "Name change failed: Invalid name"

**Expected:** Validation works ✓

## Benefits

1. **No Confusion:** Every player always has a name
2. **Easy Identification:** Numbers help track who's who
3. **Flexibility:** Can change name if desired
4. **UX:** No error messages for forgetting to enter name
5. **Simplicity:** Just click buttons, system handles the rest

## Files Modified

1. **[web_app_multiplayer.py](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\web_app_multiplayer.py)**
   - Lines 287-289: Auto-name for host
   - Lines 335-341: Auto-name for joining players
   - Lines 438-463: Name change event handler

2. **[multiplayer.py](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\multiplayer.py)**
   - Lines 100-105: change_player_name method

3. **[multiplayer.js](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\multiplayer.js)**
   - Lines 54-57: Socket event listeners
   - Line 67: Button event listener
   - Lines 180-185: changeName method
   - Lines 241-254: Event handlers

4. **[index.html](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\templates\index.html)**
   - Lines 77-80: Name change UI

5. **[style.css](h:\My Drive\CS 415 - Algorithm Analysis\Tile Swap\static\style.css)**
   - Lines 727-755: Name change section styling

---

**Status:** ✅ Complete and ready for use
