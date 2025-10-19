/**
 * Tile Swap Game - Multiplayer Client
 *
 * Handles WebSocket communication and multiplayer game logic for competitive play.
 * Supports both real-time and turn-based modes with up to 30 players.
 */

class MultiplayerClient {
    constructor(gameInstance) {
        this.game = gameInstance;
        this.socket = null;
        this.currentRoom = null;
        this.isHost = false;
        this.isReady = false;
        this.mySessionId = null;
        this.isMultiplayerMode = false;
        this.roomMode = null; // 'realtime' or 'turnbased'

        this.setupUI();
        this.connect();
    }

    connect() {
        // Connect to WebSocket server
        this.socket = io();

        // Connection events
        this.socket.on('connected', (data) => {
            this.mySessionId = data.session_id;
            console.log('Connected to server:', this.mySessionId);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.handleDisconnect();
        });

        // Room events
        this.socket.on('room_created', (data) => this.handleRoomCreated(data));
        this.socket.on('room_joined', (data) => this.handleRoomJoined(data));
        this.socket.on('join_failed', (data) => this.handleJoinFailed(data));
        this.socket.on('player_joined', (data) => this.handlePlayerJoined(data));
        this.socket.on('player_left', (data) => this.handlePlayerLeft(data));
        this.socket.on('player_ready_changed', (data) => this.handlePlayerReadyChanged(data));
        this.socket.on('game_started', (data) => this.handleGameStarted(data));
        this.socket.on('leaderboard_update', (data) => this.handleLeaderboardUpdate(data));
        this.socket.on('left_room', (data) => this.handleLeftRoom(data));

        // Test event to verify room broadcasts work
        this.socket.on('test_broadcast', (data) => {
            console.log('TEST BROADCAST RECEIVED:', data);
        });

        // Name change events
        this.socket.on('player_name_changed', (data) => this.handlePlayerNameChanged(data));
        this.socket.on('name_change_success', (data) => this.handleNameChangeSuccess(data));
        this.socket.on('name_change_failed', (data) => this.handleNameChangeFailed(data));
    }

    setupUI() {
        // Mode tabs
        document.getElementById('mode-single').addEventListener('click', () => this.switchToSinglePlayer());
        document.getElementById('mode-multi').addEventListener('click', () => this.switchToMultiplayer());

        // Multiplayer controls
        document.getElementById('create-room-btn').addEventListener('click', () => this.createRoom());
        document.getElementById('join-room-btn').addEventListener('click', () => this.joinRoom());
        document.getElementById('leave-room-btn').addEventListener('click', () => this.leaveRoom());
        document.getElementById('toggle-ready-btn').addEventListener('click', () => this.toggleReady());
        document.getElementById('start-game-btn').addEventListener('click', () => this.startGame());
        document.getElementById('end-mp-game-btn').addEventListener('click', () => this.endMultiplayerGame());
        document.getElementById('change-name-btn').addEventListener('click', () => this.changeName());

        // Room code input - auto uppercase
        document.getElementById('room-code').addEventListener('input', (e) => {
            e.target.value = e.target.value.toUpperCase();
        });
    }

    switchToSinglePlayer() {
        this.isMultiplayerMode = false;

        // Update tab styles
        document.getElementById('mode-single').classList.add('active');
        document.getElementById('mode-multi').classList.remove('active');

        // Show/hide sections
        document.getElementById('single-player-setup').classList.remove('hidden');
        document.getElementById('multiplayer-setup').classList.add('hidden');
        document.getElementById('multiplayer-lobby').classList.add('hidden');
        document.getElementById('multiplayer-leaderboard').classList.add('hidden');
        document.getElementById('game-controls').classList.remove('hidden');

        // Re-enable tile display for single player
        this.game.showTiles = true;
        if (this.game.gameState) {
            this.game.draw();
        }

        // Leave room if in one
        if (this.currentRoom) {
            this.leaveRoom();
        }
    }

    switchToMultiplayer() {
        this.isMultiplayerMode = true;

        // Update tab styles
        document.getElementById('mode-single').classList.remove('active');
        document.getElementById('mode-multi').classList.add('active');

        // Show/hide sections
        document.getElementById('single-player-setup').classList.add('hidden');
        document.getElementById('multiplayer-setup').classList.remove('hidden');
        document.getElementById('game-controls').classList.add('hidden');
    }

    createRoom() {
        const playerName = document.getElementById('player-name').value.trim() || 'Player';
        const mode = document.getElementById('game-mode-select').value;
        const numNodes = parseInt(document.getElementById('mp-num-nodes').value);

        this.roomMode = mode;

        // Create game first
        this.game.newGame(numNodes).then(() => {
            // Hide tiles until game starts (host should also not see tiles in lobby)
            this.game.showTiles = false;
            this.game.draw();

            // Emit create room event
            this.socket.emit('create_room', {
                name: playerName,
                mode: mode,
                num_nodes: numNodes
            });
        });
    }

    joinRoom() {
        const playerName = document.getElementById('player-name').value.trim() || 'Player';
        const roomCode = document.getElementById('room-code').value.trim().toUpperCase();

        if (!roomCode) {
            this.game.showMessage('Error', 'Please enter a room code');
            return;
        }

        this.socket.emit('join_room', {
            room_code: roomCode,
            name: playerName
        });
    }

    leaveRoom() {
        this.socket.emit('leave_room');
    }

    toggleReady() {
        this.isReady = !this.isReady;

        const btn = document.getElementById('toggle-ready-btn');
        btn.textContent = this.isReady ? '✓ Ready' : 'Ready';
        btn.classList.toggle('btn-primary', this.isReady);
        btn.classList.toggle('btn-secondary', !this.isReady);

        this.socket.emit('toggle_ready', {ready: this.isReady});
    }

    startGame() {
        this.socket.emit('start_game');
    }

    endMultiplayerGame() {
        this.leaveRoom();
        this.switchToSinglePlayer();
    }

    changeName() {
        const newName = document.getElementById('change-name-input').value.trim();
        if (newName) {
            this.socket.emit('change_name', {name: newName});
        }
    }

    // ========================================================================
    // EVENT HANDLERS
    // ========================================================================

    handleRoomCreated(data) {
        if (!data.success) return;

        this.currentRoom = data.room_code;
        this.isHost = true;

        // Update UI to show lobby
        document.getElementById('multiplayer-setup').classList.add('hidden');
        document.getElementById('multiplayer-lobby').classList.remove('hidden');

        this.updateLobby(data.room_info);

        // Load the game graph preview (without tiles showing) - same as non-host
        this.loadMultiplayerGraph(data.room_info, false);
    }

    handleRoomJoined(data) {
        if (!data.success) return;

        this.currentRoom = data.room_code;
        this.isHost = false;

        // Update UI to show lobby
        document.getElementById('multiplayer-setup').classList.add('hidden');
        document.getElementById('multiplayer-lobby').classList.remove('hidden');

        this.updateLobby(data.room_info);

        // Load the game graph preview (without tiles showing)
        this.loadMultiplayerGraph(data.room_info, false);
    }

    handleJoinFailed(data) {
        this.game.showMessage('Join Failed', data.message);
    }

    handlePlayerJoined(data) {
        this.updateLobby(data.room_info);

        // If I'm not the joiner, show notification
        if (data.session_id !== this.mySessionId) {
            this.game.soundEffects.playClick();
        }
    }

    handlePlayerLeft(data) {
        this.updateLobby(data.room_info);
    }

    handlePlayerReadyChanged(data) {
        this.updateLobby(data.room_info);
    }

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

    handleGameStarted(data) {
        console.log('Game started event received!', data);
        console.log('Am I host?', this.isHost);

        const roomInfo = data.room_info;

        // DIAGNOSTIC: Check what tiles data we received
        console.log('DEBUG: roomInfo.initial_tiles =', roomInfo.initial_tiles);
        console.log('DEBUG: typeof roomInfo.initial_tiles =', typeof roomInfo.initial_tiles);
        console.log('DEBUG: Object.keys(roomInfo.initial_tiles) =', Object.keys(roomInfo.initial_tiles));
        console.log('DEBUG: Object.keys(roomInfo.initial_tiles).length =', Object.keys(roomInfo.initial_tiles).length);

        this.roomMode = roomInfo.mode;

        // Hide lobby, show game + leaderboard
        document.getElementById('multiplayer-lobby').classList.add('hidden');
        document.getElementById('multiplayer-leaderboard').classList.remove('hidden');

        // Load the graph if not host, otherwise just show tiles for host
        if (!this.isHost) {
            console.log('Non-host: Loading graph with tiles');
            this.loadMultiplayerGraph(roomInfo, true); // Show tiles now
        } else {
            console.log('Host: Revealing tiles');
            // Host already has the graph, just reveal the tiles
            this.game.showTiles = true;
            this.game.draw();
        }

        // For turn-based, disable controls if not my turn
        if (this.roomMode === 'turnbased') {
            this.updateTurnBasedControls(roomInfo);
        }

        this.updateLeaderboard(roomInfo);
        this.game.soundEffects.playVictory();
    }

    handleLeaderboardUpdate(data) {
        this.updateLeaderboard(data.room_info);

        // Update turn controls if turn-based
        if (this.roomMode === 'turnbased') {
            this.updateTurnBasedControls(data.room_info);
        }
    }

    handleLeftRoom(data) {
        this.currentRoom = null;
        this.isHost = false;
        this.isReady = false;

        // Reset UI
        document.getElementById('toggle-ready-btn').textContent = 'Ready';
        document.getElementById('toggle-ready-btn').classList.remove('btn-primary');
        document.getElementById('toggle-ready-btn').classList.add('btn-secondary');

        this.switchToMultiplayer();
    }

    handleDisconnect() {
        if (this.currentRoom) {
            this.currentRoom = null;
            this.isHost = false;
            this.isReady = false;
            this.switchToMultiplayer();
            this.game.showMessage('Disconnected', 'Connection to server lost');
        }
    }

    // ========================================================================
    // UI UPDATES
    // ========================================================================

    updateLobby(roomInfo) {
        document.getElementById('lobby-room-code').textContent = roomInfo.code;
        document.getElementById('lobby-mode').textContent =
            roomInfo.mode === 'realtime' ? 'Real-Time Race' : 'Turn-Based';
        document.getElementById('lobby-player-count').textContent = roomInfo.player_count;

        // Update players list
        const playersList = document.getElementById('lobby-players-list');
        playersList.innerHTML = '';

        roomInfo.leaderboard.forEach(player => {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'lobby-player';

            const nameSpan = document.createElement('span');
            nameSpan.textContent = player.name;
            if (player.is_host) {
                nameSpan.textContent += ' (Host)';
            }
            if (player.session_id === this.mySessionId) {
                nameSpan.textContent += ' (You)';
                playerDiv.classList.add('lobby-player-you');
            }

            const statusSpan = document.createElement('span');
            statusSpan.className = 'lobby-player-status';
            // In lobby, show ready status; during game, show solved status
            if (roomInfo.state === 'lobby') {
                statusSpan.textContent = player.ready ? '✓' : '✗';
                statusSpan.style.color = player.ready ? '#4CAF50' : '#FFC107';
            } else {
                statusSpan.textContent = player.solved ? '✓' : '';
            }

            playerDiv.appendChild(nameSpan);
            playerDiv.appendChild(statusSpan);
            playersList.appendChild(playerDiv);
        });

        // Show start button for host if all ready
        if (this.isHost) {
            const startBtn = document.getElementById('start-game-btn');
            if (roomInfo.all_ready && roomInfo.player_count >= 1) {
                startBtn.classList.remove('hidden');
            } else {
                startBtn.classList.add('hidden');
            }
        }
    }

    updateLeaderboard(roomInfo) {
        const leaderboardList = document.getElementById('leaderboard-list');
        leaderboardList.innerHTML = '';

        roomInfo.leaderboard.forEach((player, index) => {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'leaderboard-player';

            if (player.session_id === this.mySessionId) {
                playerDiv.classList.add('leaderboard-player-you');
            }

            if (player.solved) {
                playerDiv.classList.add('leaderboard-player-finished');
            }

            // Rank
            const rankSpan = document.createElement('span');
            rankSpan.className = 'leaderboard-rank';
            if (player.solved) {
                rankSpan.textContent = `#${player.rank}`;
            } else {
                rankSpan.textContent = `${index + 1}.`;
            }

            // Name
            const nameSpan = document.createElement('span');
            nameSpan.className = 'leaderboard-name';
            nameSpan.textContent = player.name;
            if (player.session_id === this.mySessionId) {
                nameSpan.textContent += ' (You)';
            }

            // Moves
            const movesSpan = document.createElement('span');
            movesSpan.className = 'leaderboard-moves';
            movesSpan.textContent = `${player.moves} moves`;
            if (player.solved) {
                movesSpan.textContent += ' ✓';
            }

            // Turn indicator for turn-based
            if (this.roomMode === 'turnbased' && player.is_current_turn && !player.solved) {
                const turnIndicator = document.createElement('span');
                turnIndicator.className = 'turn-indicator';
                turnIndicator.textContent = '▶';
                playerDiv.appendChild(turnIndicator);
            }

            playerDiv.appendChild(rankSpan);
            playerDiv.appendChild(nameSpan);
            playerDiv.appendChild(movesSpan);

            leaderboardList.appendChild(playerDiv);
        });
    }

    updateTurnBasedControls(roomInfo) {
        const isMyTurn = roomInfo.current_turn_session === this.mySessionId;
        const gameState = this.game.gameState;

        if (!gameState) return;

        // Enable/disable game interactions based on turn
        if (isMyTurn && gameState.active) {
            // My turn - enable canvas
            this.game.canvas.style.opacity = '1';
            this.game.canvas.style.pointerEvents = 'auto';
        } else {
            // Not my turn - disable canvas
            this.game.canvas.style.opacity = '0.5';
            this.game.canvas.style.pointerEvents = 'none';
            this.game.selectedNode = null;
            this.game.draw();
        }
    }

    loadMultiplayerGraph(roomInfo, showTilesNow = false) {
        // Load graph from room info
        const edges = roomInfo.graph_edges;
        const tiles = roomInfo.initial_tiles;

        // DIAGNOSTIC: Log what we're working with
        console.log('DEBUG loadMultiplayerGraph: showTilesNow =', showTilesNow);
        console.log('DEBUG loadMultiplayerGraph: tiles =', tiles);
        console.log('DEBUG loadMultiplayerGraph: typeof tiles =', typeof tiles);
        console.log('DEBUG loadMultiplayerGraph: tiles === null?', tiles === null);
        console.log('DEBUG loadMultiplayerGraph: tiles === undefined?', tiles === undefined);

        if (!edges || edges.length === 0) {
            console.log('No edges to load');
            return;
        }

        // If no tiles yet (in lobby), just load the graph structure without tiles
        // Check for empty dict or null/undefined
        const hasTiles = tiles && Object.keys(tiles).length > 0;

        console.log('DEBUG loadMultiplayerGraph: hasTiles =', hasTiles);

        if (!hasTiles) {
            console.log('Loading graph preview (no tiles yet), edges:', edges);
            fetch('/api/custom_game', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({edges: edges})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.game.gameState = data.state;
                    this.game.selectedNode = null;
                    this.game.showTiles = false; // Hide tiles in lobby
                    this.game.updateUI();
                    this.game.draw();
                    console.log('Graph preview loaded successfully');
                }
            })
            .catch(error => {
                console.error('Error loading graph preview:', error);
            });
            return;
        }

        console.log('Loading multiplayer graph with tiles:', tiles);

        // Use the custom_game endpoint with specific tiles
        fetch('/api/custom_game_with_tiles', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                edges: edges,
                tiles: tiles
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.game.gameState = data.state;
                this.game.selectedNode = null;
                this.game.showTiles = showTilesNow; // Control tile visibility
                this.game.updateUI();
                this.game.draw();
                console.log('Multiplayer graph loaded. Tiles:', this.game.gameState.tiles);
            }
        });
    }

    // ========================================================================
    // GAME INTEGRATION
    // ========================================================================

    notifyMove(moves, solved) {
        if (!this.currentRoom || !this.isMultiplayerMode) return;

        this.socket.emit('player_move', {
            moves: moves,
            solved: solved
        });

        // If solved in multiplayer, show local message too
        if (solved) {
            setTimeout(() => {
                this.game.showMessage('Puzzle Solved!', `You finished in ${moves} moves!\n\nWait for other players to finish.`);
            }, 500);
        }
    }
}

// ============================================================================
// INTEGRATION WITH MAIN GAME
// ============================================================================

// Initialize multiplayer client when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait for main game to initialize
    setTimeout(() => {
        if (window.game) {
            window.multiplayerClient = new MultiplayerClient(window.game);

            // Hook into game's swap function
            const originalSwap = window.game.swapTiles.bind(window.game);
            window.game.swapTiles = async function(node1, node2) {
                await originalSwap(node1, node2);

                // Notify multiplayer if in MP mode
                if (window.multiplayerClient.isMultiplayerMode &&
                    window.multiplayerClient.currentRoom &&
                    this.gameState) {
                    window.multiplayerClient.notifyMove(
                        this.gameState.move_count,
                        !this.gameState.active // solved = not active
                    );
                }
            };
        }
    }, 100);
});
