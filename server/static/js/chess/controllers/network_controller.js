class NetworkController extends HandlersController {
    async update() {
        let updates = await api.getUpdates(this.player.id);
    
        updates.forEach(update => {
            this.handleUpdate(update);
        });
    }

    async loadGame(gameId) {
        this.setGame(await api.loadGame(gameId));
        
        if (this.game.started) {
            this.applyBoard();
        }
    }

    async createGame() {
        await api.createGame();
    }

    async joinGame(gameId) {
        this.setGame(await api.joinGame(gameId, this.player.id));
    }

    async gameMove(poss) {
        await api.gameMove(
            this.game.id, 
            this.player.id, 
            this.format(poss)
        );
    }
}
