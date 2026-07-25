import { get } from 'svelte/store';
import { user } from './authStore';
import { API_BASE_URL } from './config';

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
    const currentUser = get(user);
    const headers = new Headers(options.headers || {});

    if (currentUser) {
        if (!headers.has('X-User-Role') && currentUser.role) {
            headers.set('X-User-Role', currentUser.role);
        }
        if (!headers.has('X-User-Id') && currentUser.id) {
            headers.set('X-User-Id', String(currentUser.id));
        }
    }

    const url = endpoint.startsWith('http://') || endpoint.startsWith('https://')
        ? endpoint
        : `${API_BASE_URL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;

    return fetch(url, {
        ...options,
        headers,
    });
}
