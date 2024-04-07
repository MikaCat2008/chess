class SearchApi extends BaseApi {
    async getGames() {
        return (await this.request("get_games")).data.games;
    }
}


async function create() {
    let gameData = await api.createGame();
    
    join(gameData.id);
}


async function join(gameId) {
    await api.joinGame(gameId, playerId); 
    
    window.location.href = "/chess";
}


let api = new SearchApi(), 
    gamesElement = document.querySelector(".games");

setInterval(async () => {
    let games = await api.getGames(), inner = "";

    games.forEach(game => {       
        let players = "";

        game.players.forEach(player => {
            players += (players == "" ? "" : ", ") + `${player.username}[${player.id}]`;
        });
        
        inner += `
        <div class="game">
            Id: ${game.id};
            Players: ${players}.
            <input type="button" onclick="join(${game.id})" value="join">
        </div>`;
    });

    if (gamesElement.innerHTML != inner) {
        gamesElement.innerHTML = inner;
    }
}, 500);
