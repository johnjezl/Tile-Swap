# Sound Effects Troubleshooting Guide

## Quick Fix (Most Common Issue)

**The audio context needs user interaction to start.** This is a browser security feature.

### Solution:
1. Refresh the page (Ctrl+R or Cmd+R)
2. Create a new game
3. Click on a node to select it
4. Click on another connected node to swap
5. **You should now hear the swap sound!**

The first interaction activates the audio context. After that, all sounds will work.

---

## Detailed Troubleshooting Steps

### Step 1: Check the Sound Toggle

In the left panel under "Game Status", make sure the **"Sound Effects"** checkbox is checked ✓.

If it's unchecked, click it to enable sounds.

### Step 2: Verify Browser Support

Open your browser's Developer Console:
- **Windows/Linux:** Press `F12` or `Ctrl+Shift+I`
- **Mac:** Press `Cmd+Option+I`

Look at the Console tab. If you see:
```
Web Audio API not supported
```

Your browser doesn't support the Web Audio API. Try updating to the latest version or using a different browser.

**Supported Browsers:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Step 3: Test Each Sound Type

#### Test Swap Sound:
1. Create a new game
2. Click on a node (select it)
3. Click on a connected node (swap tiles)
4. **Expected:** Rising pitch sound (whoosh)

#### Test Click Sound:
1. Click the Undo button (if you have moves)
2. **Expected:** Short beep

#### Test Victory Sound:
1. Solve the puzzle completely
2. **Expected:** Four ascending notes (C-E-G-C)

### Step 4: Check System Volume

Make sure:
- Your system volume is not muted
- Browser tab is not muted (check speaker icon on tab)
- Headphones/speakers are connected properly

### Step 5: Check Browser Permissions

Some browsers block audio by default on certain sites.

**Chrome:**
1. Click the lock icon in the address bar
2. Check "Sound" is set to "Allow"

**Firefox:**
1. Click the site information icon (i) in the address bar
2. Click "More Information"
3. Go to Permissions tab
4. Make sure "Autoplay" is not blocked

### Step 6: Try a Different Browser

If nothing works, test in a different browser:
- Chrome
- Firefox
- Edge
- Safari (Mac only)

This helps determine if it's a browser-specific issue.

---

## Common Issues & Solutions

### Issue: "No sound at all"

**Solution:** The audio context was suspended by the browser.

**Fix Applied:** The code now automatically resumes the audio context on first interaction. This should work after refreshing the page.

### Issue: "Sound worked before, but stopped"

**Possible causes:**
1. You unchecked the "Sound Effects" checkbox
2. Browser tab was muted
3. System audio settings changed

**Solution:**
1. Check the sound toggle is enabled
2. Refresh the page
3. Try a test sound (swap tiles)

### Issue: "Victory sound plays, but swap sound doesn't"

**Solution:** The victory sound has multiple notes, so if it plays, audio is working.

**Possible cause:** Swap sound is very brief (0.1 seconds). Try:
1. Increase system volume
2. Use headphones
3. Listen carefully - it's a quick "beep-boop" rising pitch

### Issue: "Console shows 'Web Audio API not supported'"

**Solution:** Your browser is too old or doesn't support Web Audio API.

**Fix:**
1. Update your browser to the latest version
2. Or use a modern browser (Chrome, Firefox, Edge, Safari)

### Issue: "Sounds are distorted or crackling"

**Possible causes:**
1. System audio driver issues
2. Too many browser tabs playing audio
3. Low-end hardware

**Solutions:**
1. Close other tabs/applications using audio
2. Restart your browser
3. Try disabling hardware acceleration in browser settings

---

## Testing the Fix

After refreshing the page, follow these steps:

1. **Open the page fresh** (hard refresh: Ctrl+Shift+R)
2. **Click "New Random Game"**
3. **Click on any node** (this activates audio context)
4. **Click on a connected node** (swap tiles)
5. **Listen for the rising pitch sound** 🔊

If you still don't hear anything, try:
```javascript
// Open browser console (F12) and paste this:
console.log('Audio Context State:', window.game.soundEffects.audioContext.state);
```

**Expected output:** `"running"` or `"suspended"`
- If `"running"` - audio should work
- If `"suspended"` - the auto-resume failed, which is unusual

---

## Manual Testing in Console

If nothing else works, you can manually test the sound system:

1. Open browser console (F12)
2. Paste this code:

```javascript
// Force resume audio context
await window.game.soundEffects.audioContext.resume();

// Test swap sound
window.game.soundEffects.playSwap();

// Wait 1 second, then test click
setTimeout(() => window.game.soundEffects.playClick(), 1000);

// Wait 2 seconds, then test victory
setTimeout(() => window.game.soundEffects.playVictory(), 2000);
```

If these work, the audio system is functional but might need page refresh.

---

## Still Not Working?

If you've tried everything and sounds still don't work:

### Option 1: Disable Sounds
Simply uncheck the "Sound Effects" toggle and play without audio.

### Option 2: Report the Issue
Open an issue on GitHub with:
- Your browser name and version
- Operating system
- Console error messages (if any)
- Result of the manual testing code above

### Option 3: Alternative Browser
The game works perfectly fine without sound. All visual features still function normally.

---

## Summary

**Most common fix:**
1. Refresh the page
2. Create a new game
3. Make one swap
4. Sound should now work!

**The code now automatically resumes the audio context on every sound play attempt, so this issue should be resolved after refreshing the page.**

Happy gaming! 🎮🔊
