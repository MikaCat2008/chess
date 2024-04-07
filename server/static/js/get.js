async function GET_request(url_string, data) {
    let url = new URL(window.origin + url_string);
    url.search = new URLSearchParams(data);

    return await fetch(url.toString());
}


async function Api_request(method, data) {
    return await GET_request(`/api/${method}`, data);
}
