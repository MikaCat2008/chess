(async function () {
    let controller = new NetworkController(new Board(), new Player(playerId));

    if (gameId != -1) {
        await controller.loadGame(gameId);
    }

    setInterval(async () => {
        await controller.update();
    }, 200);
})()
