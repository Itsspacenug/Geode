const BASE_URL = 'http://localhost:8000'

async function request(endpoint, options={}) {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    })

    if (!res.ok) {
        throw new Error(`Reqeust failed: ${res.status}`)
    }

    return res.json()
}

export function post(endpoint, body) {
    return request(endpoint, {
        method: 'POST',
        body: JSON.stringify(body),
    })
}

export function get(endpoint) {
    return request(endpoint)
}