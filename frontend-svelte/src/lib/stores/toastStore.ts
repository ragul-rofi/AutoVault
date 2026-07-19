import { writable } from 'svelte/store';

export interface ToastItem {
    id: string;
    message: string;
    type: 'success' | 'error' | 'warning' | 'info';
    duration: number;
}

export const toasts = writable<ToastItem[]>([]);

export function addToast(message: string, type: ToastItem['type'] = 'info', duration: number = 4000) {
    const id = Math.random().toString(36).slice(2);
    const toast: ToastItem = { id, message, type, duration };

    toasts.update((all) => [toast, ...all]);

    if (duration > 0) {
        setTimeout(() => removeToast(id), duration);
    }
}

export function removeToast(id: string) {
    toasts.update((all) => all.filter((t) => t.id !== id));
}
