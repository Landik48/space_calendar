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