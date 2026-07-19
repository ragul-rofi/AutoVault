import { writable } from 'svelte/store';

export type Theme = 'dark' | 'light';

function getInitialTheme(): Theme {
    const stored = localStorage.getItem('autovault-theme');
    if (stored === 'dark' || stored === 'light') return stored;
    // Default to dark (Linear-inspired default)
    if (typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: light)').matches) {
        return 'light';
    }
    return 'dark';
}

export const theme = writable<Theme>(getInitialTheme());

theme.subscribe((value) => {
    if (typeof document !== 'undefined') {
        document.documentElement.setAttribute('data-theme', value);
        localStorage.setItem('autovault-theme', value);
    }
});

export function toggleTheme() {
    theme.update((current) => (current === 'dark' ? 'light' : 'dark'));
}
