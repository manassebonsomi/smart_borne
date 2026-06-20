const API_BASE_URL =
    "http://127.0.0.1:5000/api";


async function apiGet(url) {

    const response =
        await fetch(
            API_BASE_URL + url
        );

    return await response.json();
}


async function apiPost(
    url,
    data
) {

    const response =
        await fetch(
            API_BASE_URL + url,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(data)
            }
        );

    return await response.json();
}


async function apiPut(
    url,
    data
) {

    const response =
        await fetch(
            API_BASE_URL + url,
            {
                method: "PUT",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(data)
            }
        );

    return await response.json();
}


async function apiDelete(
    url
) {

    const response =
        await fetch(
            API_BASE_URL + url,
            {
                method: "DELETE"
            }
        );

    return await response.json();
}