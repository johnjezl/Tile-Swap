/**
 * Tile Swap Game - Enhanced Interactive JavaScript
 *
 * Features: Interactive graph visualization, animations, undo/redo,
 * save/load, dark mode, sound effects, and custom graph editor.
 */

// ============================================================================
// SOUND EFFECTS MANAGER
// ============================================================================

class SoundEffects {
    constructor() {
        this.audioContext = null;
        this.enabled = true;
        this.initAudioContext();
    }

    initAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.warn('Web Audio API not supported', e);
        }
    }

    playSwap() {
        if (!this.enabled || !this.audioContext) return;

        // Resume audio context if suspended (required by some browsers)
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.setValueAtTime(440, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(880, this.audioContext.currentTime + 0.2);

        gainNode.gain.setValueAtTime(0.5, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.2);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.2);
    }

    playVictory() {
        if (!this.enabled || !this.audioContext) return;

        // Resume audio context if suspended
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }

        const notes = [523.25, 659.25, 783.99, 1046.50]; // C, E, G, C
        notes.forEach((freq, i) => {
            setTimeout(() => {
                const oscillator = this.audioContext.createOscillator();
                const gainNode = this.audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(this.audioContext.destination);

                oscillator.frequency.value = freq;
                gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);

                oscillator.start(this.audioContext.currentTime);
                oscillator.stop(this.audioContext.currentTime + 0.3);
            }, i * 100);
        });
    }

    playClick() {
        if (!this.enabled || !this.audioContext) return;

        // Resume audio context if suspended
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.value = 800;
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.1);
    }

    setEnabled(enabled) {
        this.enabled = enabled;
    }
}

// ============================================================================
// GRAPH EDITOR
// ============================================================================

class GraphEditor {
    constructor(canvas, onComplete) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.onComplete = onComplete;
        this.nodes = [];
        this.edges = [];
        this.nextNodeId = 1;
        this.nodeRadius = 25;
        this.draggingFrom = null;
        this.dragLine = null;

        this.setupEvents();
        this.draw();
    }

    setupEvents() {
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
        this.canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseup', (e) => this.handleMouseUp(e));
        this.canvas.addEventListener('contextmenu', (e) => this.handleRightClick(e));
    }

    handleClick(e) {
        if (this.draggingFrom !== null) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const clickedNode = this.getNodeAt(x, y);

        if (!clickedNode && this.nodes.length < 20) {
            this.addNode(x, y);
        }
    }

    handleMouseDown(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const node = this.getNodeAt(x, y);
        if (node) {
            this.draggingFrom = node;
            this.dragLine = { x, y };
        }
    }

    handleMouseMove(e) {
        if (this.draggingFrom) {
            const rect = this.canvas.getBoundingClientRect();
            this.dragLine = {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            };
            this.draw();
        }
    }

    handleMouseUp(e) {
        if (this.draggingFrom) {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const node = this.getNodeAt(x, y);
            if (node && node !== this.draggingFrom) {
                this.addEdge(this.draggingFrom, node);
            }

            this.draggingFrom = null;
            this.dragLine = null;
            this.draw();
        }
    }

    handleRightClick(e) {
        e.preventDefault();
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const node = this.getNodeAt(x, y);
        if (node) {
            this.removeNode(node);
        }
    }

    addNode(x, y) {
        this.nodes.push({ id: this.nextNodeId++, x, y });
        this.updateStatus();
        this.draw();
    }

    removeNode(node) {
        this.edges = this.edges.filter(e => e[0] !== node.id && e[1] !== node.id);
        this.nodes = this.nodes.filter(n => n !== node);
        this.updateStatus();
        this.draw();
    }

    addEdge(node1, node2) {
        const edge = [Math.min(node1.id, node2.id), Math.max(node1.id, node2.id)];
        const exists = this.edges.some(e => e[0] === edge[0] && e[1] === edge[1]);
        if (!exists) {
            this.edges.push(edge);
            this.updateStatus();
        }
    }

    getNodeAt(x, y) {
        for (const node of this.nodes) {
            const dx = x - node.x;
            const dy = y - node.y;
            if (Math.sqrt(dx * dx + dy * dy) <= this.nodeRadius) {
                return node;
            }
        }
        return null;
    }

    isConnected() {
        if (this.nodes.length === 0) return false;
        if (this.nodes.length === 1) return true;

        const visited = new Set();
        const queue = [this.nodes[0].id];
        visited.add(this.nodes[0].id);

        while (queue.length > 0) {
            const current = queue.shift();
            for (const [n1, n2] of this.edges) {
                const neighbor = n1 === current ? n2 : (n2 === current ? n1 : null);
                if (neighbor && !visited.has(neighbor)) {
                    visited.add(neighbor);
                    queue.push(neighbor);
                }
            }
        }

        return visited.size === this.nodes.length;
    }

    updateStatus() {
        document.getElementById('editor-node-count').textContent = this.nodes.length;
        document.getElementById('editor-edge-count').textContent = this.edges.length;
        const status = document.getElementById('editor-connected-status');
        const connected = this.isConnected();
        status.textContent = connected ? '✓ Connected' : '✗ Not connected';
        status.style.color = connected ? '#4CAF50' : '#f44336';
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw edges
        this.ctx.strokeStyle = '#999';
        this.ctx.lineWidth = 2;
        for (const [id1, id2] of this.edges) {
            const node1 = this.nodes.find(n => n.id === id1);
            const node2 = this.nodes.find(n => n.id === id2);
            if (node1 && node2) {
                this.ctx.beginPath();
                this.ctx.moveTo(node1.x, node1.y);
                this.ctx.lineTo(node2.x, node2.y);
                this.ctx.stroke();
            }
        }

        // Draw drag line
        if (this.draggingFrom && this.dragLine) {
            this.ctx.strokeStyle = '#FFC107';
            this.ctx.setLineDash([5, 5]);
            this.ctx.beginPath();
            this.ctx.moveTo(this.draggingFrom.x, this.draggingFrom.y);
            this.ctx.lineTo(this.dragLine.x, this.dragLine.y);
            this.ctx.stroke();
            this.ctx.setLineDash([]);
        }

        // Draw nodes
        for (const node of this.nodes) {
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, this.nodeRadius, 0, 2 * Math.PI);
            this.ctx.fillStyle = '#2196F3';
            this.ctx.fill();
            this.ctx.strokeStyle = '#333';
            this.ctx.lineWidth = 2;
            this.ctx.stroke();

            this.ctx.fillStyle = '#fff';
            this.ctx.font = 'bold 16px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(node.id, node.x, node.y);
        }
    }

    clear() {
        this.nodes = [];
        this.edges = [];
        this.nextNodeId = 1;
        this.updateStatus();
        this.draw();
    }

    getGraphData() {
        return {
            nodes: this.nodes.length,
            edges: this.edges.map(e => [e[0], e[1]])
        };
    }
}

// ============================================================================
// MAIN GAME CLASS
// ============================================================================

class TileSwapGame {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.gameState = null;
        this.selectedNode = null;
        this.hoveredNode = null;
        this.nodeRadius = 30;
        this.soundEffects = new SoundEffects();
        this.editor = null;

        // Animation state
        this.animating = false;
        this.animationProgress = 0;
        this.animatingNodes = null;

        this.setupEventListeners();
        this.resizeCanvas();
        this.loadDarkMode();
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    setupEventListeners() {
        // Game controls
        document.getElementById('new-game-btn').addEventListener('click', () => this.newGame());
        document.getElementById('custom-graph-btn').addEventListener('click', () => this.openGraphEditor());
        document.getElementById('undo-btn').addEventListener('click', () => this.undo());
        document.getElementById('redo-btn').addEventListener('click', () => this.redo());
        document.getElementById('save-btn').addEventListener('click', () => this.saveGame());
        document.getElementById('load-btn').addEventListener('click', () => this.loadGame());

        // Canvas interaction
        this.canvas.addEventListener('click', (e) => this.handleCanvasClick(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleCanvasHover(e));

        // Message overlay
        document.getElementById('message-close').addEventListener('click', () => this.hideMessage());

        // Dark mode
        document.getElementById('dark-mode-toggle').addEventListener('click', () => this.toggleDarkMode());

        // Sound toggle
        document.getElementById('sound-toggle').addEventListener('change', (e) => {
            this.soundEffects.setEnabled(e.target.checked);
        });

        // Graph editor controls
        document.getElementById('editor-done').addEventListener('click', () => this.finishGraphEditor());
        document.getElementById('editor-clear').addEventListener('click', () => {
            if (this.editor) this.editor.clear();
        });
        document.getElementById('editor-cancel').addEventListener('click', () => this.closeGraphEditor());

        // File input for loading
        document.getElementById('file-input').addEventListener('change', (e) => this.handleFileLoad(e));

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 'z') {
                    e.preventDefault();
                    if (e.shiftKey) {
                        this.redo();
                    } else {
                        this.undo();
                    }
                } else if (e.key === 's') {
                    e.preventDefault();
                    this.saveGame();
                }
            }
        });
    }

    // ========================================================================
    // DARK MODE
    // ========================================================================

    toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
        this.draw();
    }

    loadDarkMode() {
        const isDark = localStorage.getItem('darkMode') === 'true';
        if (isDark) {
            document.body.classList.add('dark-mode');
        }
    }

    // ========================================================================
    // GRAPH EDITOR
    // ========================================================================

    openGraphEditor() {
        document.getElementById('editor-overlay').classList.remove('hidden');
        const editorCanvas = document.getElementById('editor-canvas');
        this.editor = new GraphEditor(editorCanvas);
    }

    closeGraphEditor() {
        document.getElementById('editor-overlay').classList.add('hidden');
        this.editor = null;
    }

    async finishGraphEditor() {
        if (!this.editor) return;

        const graphData = this.editor.getGraphData();

        if (graphData.nodes < 2) {
            this.showMessage('Error', 'Need at least 2 nodes to create a graph.');
            return;
        }

        if (!this.editor.isConnected()) {
            this.showMessage('Error', 'Graph must be connected (all nodes must be reachable).');
            return;
        }

        this.closeGraphEditor();

        try {
            const response = await fetch('/api/custom_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ edges: graphData.edges })
            });

            const data = await response.json();

            if (data.success) {
                this.gameState = data.state;
                this.selectedNode = null;
                this.updateUI();
                this.draw();
            } else {
                this.showMessage('Error', data.message || 'Failed to create game');
            }
        } catch (error) {
            console.error('Error creating custom game:', error);
            this.showMessage('Error', 'Failed to connect to server');
        }
    }

    // ========================================================================
    // GAME LOGIC
    // ========================================================================

    resizeCanvas() {
        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = container.clientHeight;
        this.draw();
    }

    async newGame() {
        const numNodes = parseInt(document.getElementById('num-nodes').value);

        try {
            const response = await fetch('/api/new_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ num_nodes: numNodes })
            });

            const data = await response.json();

            if (data.success) {
                this.gameState = data.state;
                this.selectedNode = null;
                this.updateUI();
                this.draw();
            } else {
                this.showMessage('Error', data.message || 'Failed to create game');
            }
        } catch (error) {
            console.error('Error creating game:', error);
            this.showMessage('Error', 'Failed to connect to server');
        }
    }

    async swapTiles(node1, node2) {
        if (this.animating) return;

        try {
            const response = await fetch('/api/swap', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ node1, node2 })
            });

            const data = await response.json();

            if (data.success) {
                // Animate the swap
                await this.animateSwap(node1, node2);

                this.gameState = data.state;
                this.selectedNode = null;
                this.updateUI();
                this.draw();

                this.soundEffects.playSwap();

                // Check if game is won
                if (data.solved) {
                    setTimeout(() => this.handleGameWon(data.move_count, data.optimal_moves), 300);
                }
            } else {
                this.showMessage('Invalid Move', data.message);
            }
        } catch (error) {
            console.error('Error swapping tiles:', error);
            this.showMessage('Error', 'Failed to connect to server');
        }
    }

    async animateSwap(node1, node2) {
        this.animating = true;
        this.animatingNodes = { node1, node2 };
        this.animationProgress = 0;

        return new Promise(resolve => {
            const animate = () => {
                this.animationProgress += 0.1;
                this.draw();

                if (this.animationProgress >= 1) {
                    this.animating = false;
                    this.animatingNodes = null;
                    resolve();
                } else {
                    requestAnimationFrame(animate);
                }
            };
            animate();
        });
    }

    async undo() {
        try {
            const response = await fetch('/api/undo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();

            if (data.success) {
                this.gameState = data.state;
                this.selectedNode = null;
                this.updateUI();
                this.draw();
                this.soundEffects.playClick();
            }
        } catch (error) {
            console.error('Error undoing:', error);
        }
    }

    async redo() {
        try {
            const response = await fetch('/api/redo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();

            if (data.success) {
                this.gameState = data.state;
                this.selectedNode = null;
                this.updateUI();
                this.draw();
                this.soundEffects.playClick();
            }
        } catch (error) {
            console.error('Error redoing:', error);
        }
    }

    // ========================================================================
    // SAVE/LOAD
    // ========================================================================

    async saveGame() {
        try {
            const response = await fetch('/api/save');
            const data = await response.json();

            if (data.success) {
                // Download as JSON file
                const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `tileswap-save-${new Date().toISOString().slice(0, 10)}.json`;
                a.click();
                URL.revokeObjectURL(url);

                this.soundEffects.playClick();
                this.showMessage('Success', 'Game saved successfully!');
            }
        } catch (error) {
            console.error('Error saving game:', error);
            this.showMessage('Error', 'Failed to save game');
        }
    }

    loadGame() {
        document.getElementById('file-input').click();
    }

    async handleFileLoad(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const saveData = JSON.parse(e.target.result);

                const response = await fetch('/api/load', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: saveData })
                });

                const data = await response.json();

                if (data.success) {
                    this.gameState = data.state;
                    this.selectedNode = null;
                    this.updateUI();
                    this.draw();
                    this.soundEffects.playClick();
                    this.showMessage('Success', 'Game loaded successfully!');
                } else {
                    this.showMessage('Error', data.message || 'Failed to load game');
                }
            } catch (error) {
                console.error('Error loading game:', error);
                this.showMessage('Error', 'Invalid save file');
            }
        };
        reader.readAsText(file);

        // Reset file input
        event.target.value = '';
    }

    // ========================================================================
    // UI AND INTERACTION
    // ========================================================================

    handleCanvasClick(e) {
        if (!this.gameState || !this.gameState.active || this.animating) {
            return;
        }

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const clickedNode = this.getNodeAtPosition(x, y);

        if (clickedNode !== null) {
            if (this.selectedNode === null) {
                this.selectedNode = clickedNode;
                this.soundEffects.playClick();
                this.draw();
            } else if (this.selectedNode === clickedNode) {
                this.selectedNode = null;
                this.soundEffects.playClick();
                this.draw();
            } else {
                this.swapTiles(this.selectedNode, clickedNode);
            }
        } else {
            this.selectedNode = null;
            this.draw();
        }
    }

    handleCanvasHover(e) {
        if (!this.gameState) {
            return;
        }

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const hoveredNode = this.getNodeAtPosition(x, y);

        if (hoveredNode !== this.hoveredNode) {
            this.hoveredNode = hoveredNode;
            this.canvas.style.cursor = hoveredNode !== null ? 'pointer' : 'default';
            this.draw();
        }
    }

    getNodeAtPosition(x, y) {
        if (!this.gameState) return null;

        for (const node of this.gameState.nodes) {
            const pos = this.getNodeScreenPosition(node);
            const dx = x - pos.x;
            const dy = y - pos.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance <= this.nodeRadius) {
                return node;
            }
        }

        return null;
    }

    getNodeScreenPosition(node) {
        const pos = this.gameState.node_positions[node.toString()];
        return {
            x: pos.x * this.canvas.width,
            y: pos.y * this.canvas.height
        };
    }

    updateUI() {
        if (!this.gameState) {
            document.getElementById('move-count').textContent = '0';
            document.getElementById('optimal-moves').textContent = '0';
            document.getElementById('game-status').textContent = 'Not started';
            document.getElementById('undo-btn').disabled = true;
            document.getElementById('redo-btn').disabled = true;
            return;
        }

        document.getElementById('move-count').textContent = this.gameState.move_count;
        document.getElementById('optimal-moves').textContent = this.gameState.optimal_moves;
        document.getElementById('game-status').textContent =
            this.gameState.active ? 'Playing' : 'Game over';

        document.getElementById('undo-btn').disabled = !this.gameState.can_undo;
        document.getElementById('redo-btn').disabled = !this.gameState.can_redo;
    }

    // ========================================================================
    // RENDERING
    // ========================================================================

    draw() {
        const isDark = document.body.classList.contains('dark-mode');

        // Clear canvas
        this.ctx.fillStyle = isDark ? '#1a1a2e' : '#fafafa';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        if (!this.gameState) {
            this.drawWelcomeMessage();
            return;
        }

        this.drawEdges();
        this.drawNodes();
    }

    drawWelcomeMessage() {
        const isDark = document.body.classList.contains('dark-mode');
        this.ctx.fillStyle = isDark ? '#ccc' : '#666';
        this.ctx.font = '24px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(
            'Click "New Random Game" to start',
            this.canvas.width / 2,
            this.canvas.height / 2
        );
    }

    drawEdges() {
        const isDark = document.body.classList.contains('dark-mode');
        this.ctx.strokeStyle = isDark ? '#444' : '#ccc';
        this.ctx.lineWidth = 2;

        for (const edge of this.gameState.edges) {
            const pos1 = this.getNodeScreenPosition(edge[0]);
            const pos2 = this.getNodeScreenPosition(edge[1]);

            this.ctx.beginPath();
            this.ctx.moveTo(pos1.x, pos1.y);
            this.ctx.lineTo(pos2.x, pos2.y);
            this.ctx.stroke();
        }
    }

    drawNodes() {
        const isDark = document.body.classList.contains('dark-mode');

        for (const node of this.gameState.nodes) {
            let pos = this.getNodeScreenPosition(node);
            const tileInfo = this.gameState.tiles[node.toString()];
            const isSelected = node === this.selectedNode;
            const isHovered = node === this.hoveredNode;

            // Handle animation
            if (this.animating && this.animatingNodes) {
                if (node === this.animatingNodes.node1 || node === this.animatingNodes.node2) {
                    const otherNode = node === this.animatingNodes.node1 ?
                        this.animatingNodes.node2 : this.animatingNodes.node1;
                    const otherPos = this.getNodeScreenPosition(otherNode);

                    // Interpolate position with easing
                    const t = this.easeInOutQuad(this.animationProgress);
                    pos = {
                        x: pos.x + (otherPos.x - pos.x) * t,
                        y: pos.y + (otherPos.y - pos.y) * t
                    };
                }
            }

            // Draw node circle
            this.ctx.beginPath();
            this.ctx.arc(pos.x, pos.y, this.nodeRadius, 0, 2 * Math.PI);

            // Fill color based on matched status
            if (tileInfo.matched) {
                this.ctx.fillStyle = '#4CAF50';
            } else {
                this.ctx.fillStyle = '#2196F3';
            }
            this.ctx.fill();

            // Draw border
            this.ctx.lineWidth = isSelected ? 5 : (isHovered ? 3 : 2);
            this.ctx.strokeStyle = isSelected ? '#FFC107' :
                (isHovered ? (isDark ? '#888' : '#666') : (isDark ? '#555' : '#333'));
            this.ctx.stroke();

            // Draw node number (small, top)
            this.ctx.fillStyle = '#fff';
            this.ctx.font = 'bold 12px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(`Node ${node}`, pos.x, pos.y - 8);

            // Draw tile number (large, bottom)
            this.ctx.font = 'bold 20px Arial';
            this.ctx.fillText(`${tileInfo.tile}`, pos.x, pos.y + 10);
        }
    }

    easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    }

    // ========================================================================
    // MESSAGES
    // ========================================================================

    handleGameWon(moves, optimal) {
        this.soundEffects.playVictory();

        let rating = '';
        if (moves === optimal) {
            rating = 'PERFECT! You solved it optimally!';
        } else if (moves <= optimal * 1.5) {
            rating = 'Great job! Very efficient solution!';
        } else {
            rating = 'You solved it! Try to find a more efficient path next time.';
        }

        this.showMessage(
            'Congratulations! You Won!',
            `Final Score: ${moves} moves\nOptimal Solution: ${optimal} moves\n\n${rating}`
        );
    }

    showMessage(title, text) {
        document.getElementById('message-title').textContent = title;
        document.getElementById('message-text').textContent = text;
        document.getElementById('message-overlay').classList.remove('hidden');
    }

    hideMessage() {
        document.getElementById('message-overlay').classList.add('hidden');
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    window.game = new TileSwapGame();
});
