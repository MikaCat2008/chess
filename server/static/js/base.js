class BaseApi {
    async request(method, data) {
        let response = await Api_request(method, data);
        
        return await response.json();
    }

    async loadGame(gameId) {
        return (await this.request("load_game", {
            game_id: gameId
        })).data.game;
    }

    async createGame() {
        return (await this.request("create_game")).data.game;
    }

    async joinGame(gameId, playerId) {
        return (await this.request("join_game", {
            game_id: gameId,
            player_id: playerId,
        })).data.game;
    }

    async getUpdates(playerId) {
        return (await this.request("get_updates", {
            player_id: playerId
        })).data.updates;
    }
}


class Dispatcher {
    constructor () {
        this.listeners = {};
    }

    on(event, listener) {
        let listeners = this.listeners[event];

        if (listeners == undefined) {
            this.listeners[event] = [listener]
        }
        else {
            listeners.push(listener)
        }
    }

    emit(event, data) {
        let listeners = this.listeners[event], results = [];
        
        if (!Array.isArray(data)) {
            data = [data];
        }

        if (listeners != undefined) {
            for (let i = 0; i < listeners.length; i++) {                
                results.push(listeners[i](...data));
            }
        }

        return results.every(result => result);
    }
}


class BaseGame extends Dispatcher {
    constructor (id, started, players) {
        super();

        this.id = id;
        this.started = started;
        this.players = players;
    }

    start() {
        this.started = true;
    }
}


class BasePlayer {
    constructor (id) {
        this.id = id;
    }
}
