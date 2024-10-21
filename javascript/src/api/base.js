export const API_URL = process.env.NODE_ENV !== 'Production' ? 'https://primary-dragon-publicly.ngrok-free.app' : ''

export function API(path) {
    return `${API_URL}/${path}`
}