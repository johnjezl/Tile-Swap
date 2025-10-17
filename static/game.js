/**
 * Tile Swap Game - Interactive JavaScript
 *
 * Handles the interactive graph visualization and game logic for the web interface.
 */

class TileSwapGame {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.gameState = null;
        this.selectedNode = null;
        this.hoveredNode = null;
        this.nodeRadius = 30;

        this.setupEventListeners();
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    setupEventListeners() {
        // New game button
        document.getElementById('new-game-btn').addEventListener('click', () => {
            this.newGame();
        });

        // Canvas click
        this.canvas.addEventListener('click', (e) => {
            this.handleCanvasClick(e);
        });

        // Canvas hover
        this.canvas.addEventListener('mousemove', (e) => {
            this.handleCanvasHover(e);
        });

        // Message overlay close
        document.getElementById('message-close').addEventListener('click', () => {
            this.hideMessage();
        });
    }

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
        try {
            const response = await fetch('/api/swap', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ node1, node2 })
            });

            const data = await response.json();

            if (data.success) {
                this.gameState = data.state;
                this.selectedNode = null;
                this.updateUI();
                this.draw();

                // Check if game is won
                if (data.solved) {
                    this.handleGameWon(data.move_count, data.optimal_moves);
                }
            } else {
                this.showMessage('Invalid Move', data.message);
            }
        } catch (error) {
            console.error('Error swapping tiles:', error);
            this.showMessage('Error', 'Failed to connect to server');
        }
    }

    handleCanvasClick(e) {
        if (!this.gameState || !this.gameState.active) {
            return;
        }

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const clickedNode = this.getNodeAtPosition(x, y);

        if (clickedNode !== null) {
            if (this.selectedNode === null) {
                // First click - select node
                this.selectedNode = clickedNode;
                this.draw();
            } else if (this.selectedNode === clickedNode) {
                // Click same node - deselect
                this.selectedNode = null;
                this.draw();
            } else {
                // Second click - attempt swap
                this.swapTiles(this.selectedNode, clickedNode);
            }
        } else {
            // Click empty space - deselect
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
            return;
        }

        document.getElementById('move-count').textContent = this.gameState.move_count;
        document.getElementById('optimal-moves').textContent = this.gameState.optimal_moves;
        document.getElementById('game-status').textContent =
            this.gameState.active ? 'Playing' : 'Not started';
    }

    draw() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        if (!this.gameState) {
            this.drawWelcomeMessage();
            return;
        }

        // Draw edges first
        this.drawEdges();

        // Draw nodes on top
        this.drawNodes();
    }

    drawWelcomeMessage() {
        this.ctx.fillStyle = '#666';
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
        this.ctx.strokeStyle = '#ccc';
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
        for (const node of this.gameState.nodes) {
            const pos = this.getNodeScreenPosition(node);
            const tileInfo = this.gameState.tiles[node.toString()];
            const isSelected = node === this.selectedNode;
            const isHovered = node === this.hoveredNode;

            // Draw node circle
            this.ctx.beginPath();
            this.ctx.arc(pos.x, pos.y, this.nodeRadius, 0, 2 * Math.PI);

            // Fill color based on matched status
            if (tileInfo.matched) {
                this.ctx.fillStyle = '#4CAF50';  // Green for matched
            } else {
                this.ctx.fillStyle = '#2196F3';  // Blue for unmatched
            }
            this.ctx.fill();

            // Draw border
            this.ctx.lineWidth = isSelected ? 5 : (isHovered ? 3 : 2);
            this.ctx.strokeStyle = isSelected ? '#FFC107' : (isHovered ? '#666' : '#333');
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

    handleGameWon(moves, optimal) {
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

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.game = new TileSwapGame();
});
