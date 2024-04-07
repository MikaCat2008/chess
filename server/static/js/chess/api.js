class ChessApi extends BaseApi {
    async gameMove(gameId, playerId, poss) {
        return (await this.request("game_move", {
            game_id: gameId,
            player_id: playerId,
            poss: poss
        })).data.message;
    }
}


let api = new ChessApi();
