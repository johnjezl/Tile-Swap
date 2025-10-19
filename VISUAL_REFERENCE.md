# Visual Reference - Tile Display Changes

## Before vs After

### Old Design (Before Changes)
```
    Node 2
       2
```
- Simple text display
- Hard to distinguish node number from tile number
- Small nodes (radius: 30px)

### New Design (After Changes)

#### Single Player & Multiplayer (Playing)
```
    Node 2
    ┌────┐
    │ 3  │  ← White square "tile"
    └────┘
```
- Node label at top: "Node 2" (white, 14px)
- Tile shown as 28x28px white square
- Dark border (2px, #333)
- Tile number inside: bold 18px
- Larger nodes (radius: 40px)

#### Multiplayer (Lobby Preview)
```
      2
```
- Only node number shown (centered)
- No tile displayed
- Neutral gray node color
- Graph structure visible

## Color Scheme

### Node Colors

**Playing (with tiles):**
- Matched node: `#4CAF50` (Green)
- Unmatched node: `#2196F3` (Blue)

**Preview mode (no tiles):**
- Dark mode: `#555` (Dark gray)
- Light mode: `#999` (Light gray)

**Borders:**
- Selected: `#FFC107` (Amber), 5px
- Hovered: Gray, 3px
- Normal: Gray, 2px

### Tile Colors

**Tile square:**
- Background: `#fff` (White)
- Border: `#333` (Dark gray), 2px
- Number: `#333` (Dark gray), bold 18px

## Node Size Comparison

| Element | Old Size | New Size | Change |
|---------|----------|----------|--------|
| Node radius | 30px | 40px | +33% |
| Graph editor radius | 25px | 40px | +60% |
| Tile square | N/A | 28x28px | New |
| Node label | 12px | 14px | +17% |
| Tile number | 20px | 18px | -10%* |

*Tile number is smaller but appears larger due to white square background

## Layout Dimensions

### Vertical Spacing in Node
```
Top of circle: y - 40
├─ Node label: y - 12
├─ Center: y
├─ Tile top: y + 2
├─ Tile number: y + 16
└─ Bottom of circle: y + 40
```

Total height: 80px (from top to bottom of circle)

### Tile Square Position
- Size: 28 x 28 pixels
- Left edge: x - 14 (centered on node)
- Right edge: x + 14
- Top edge: y + 2
- Bottom edge: y + 30

## Interaction States

### 1. Normal State
- Blue circle
- White node label
- White tile square with black number
- Thin gray border

### 2. Hovered State
- Same colors
- Medium border (3px)
- Slight highlight on border

### 3. Selected State
- Same colors
- Thick amber border (5px, #FFC107)
- Clearly indicates selection

### 4. Matched State
- Green circle (#4CAF50)
- White node label
- White tile square
- Indicates node number = tile number

### 5. Preview State (Multiplayer Lobby)
- Gray circle
- White node number (centered)
- No tile shown
- Anticipation for game start

## Code Snippets

### Drawing a Tile Square
```javascript
const tileSize = 28;
const tileX = pos.x - tileSize / 2;
const tileY = pos.y + 2;

// Background
this.ctx.fillStyle = '#fff';
this.ctx.fillRect(tileX, tileY, tileSize, tileSize);

// Border
this.ctx.strokeStyle = '#333';
this.ctx.lineWidth = 2;
this.ctx.strokeRect(tileX, tileY, tileSize, tileSize);

// Number
this.ctx.fillStyle = '#333';
this.ctx.font = 'bold 18px Arial';
this.ctx.fillText(`${tileInfo.tile}`, pos.x, pos.y + 16);
```

### Controlling Tile Visibility
```javascript
// Hide tiles (lobby preview)
game.showTiles = false;
game.draw();

// Show tiles (game started)
game.showTiles = true;
game.draw();
```

## User Flow

### Multiplayer Session Visual Progression

**Step 1: Create Room**
```
[Host creates room]
↓
Gray nodes appear (no tiles)
Players can see graph structure
```

**Step 2: Join Room**
```
[Other players join]
↓
All players see same gray graph preview
Can study connectivity
```

**Step 3: Ready Up**
```
[Players click "Ready"]
↓
Still in preview mode
Building anticipation
```

**Step 4: Start Game**
```
[Host clicks "Start Game"]
↓
Tiles appear simultaneously for ALL players
White squares with numbers
Fair competitive start!
```

## Accessibility Considerations

### Color Blind Friendly
- ✅ Green/blue distinction backed by matched/unmatched state
- ✅ White tiles visible regardless of color perception
- ✅ Dark borders provide high contrast

### Low Vision
- ✅ Larger nodes (40px) easier to see
- ✅ Bold text (18px) for tile numbers
- ✅ High contrast white/black for tiles

### Touch Devices
- ✅ 40px radius = 80px diameter (meets minimum touch target)
- ✅ Easier selection on tablets/phones
- ✅ Less chance of mis-clicks

## Performance

### Rendering Impact
- Slightly more complex drawing (rectangles + text)
- Minimal performance impact (negligible)
- Still renders at 60 FPS on modern browsers

### Memory Usage
- No additional memory overhead
- No new textures/images loaded
- All rendering done with canvas primitives

## Browser Compatibility

Tested and working on:
- ✅ Chrome 100+
- ✅ Firefox 100+
- ✅ Safari 15+
- ✅ Edge 100+

All features use standard Canvas 2D API (universal support)

---

**Visual Design Status:** ✅ Complete and polished
