export async function PostRequest(json, url) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: json
        })
        return await response.json()
    } catch (error) {
        console.error(error)
    }
}

export async function GetRequest(url) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        return await response.json()
    } catch (error) {
        console.error(error)
    }
}