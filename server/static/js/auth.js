async function login(username, password) {
    await Api_request("login", {
        username: username,
        password: password
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
}


async function register(username, password) {
    await Api_request("register", {
        username: username,
        password: password
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
}
