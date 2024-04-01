async function login(username, password) {
    await api("login", {
        username: username,
        password: password
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
}


async function register(username, password) {
    await api("register", {
        username: username,
        password: password
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
}
