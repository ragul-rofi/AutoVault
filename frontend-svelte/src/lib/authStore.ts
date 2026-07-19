import { writable } from 'svelte/store';

interface User {
    id: number;
    name: string;
    role: string;
}

const storedUser = localStorage.getItem('user');
export const user = writable<User | null>(storedUser ? JSON.parse(storedUser) : null);

user.subscribe(value => {
    if (value) {
        localStorage.setItem('user', JSON.stringify(value));
    } else {
        localStorage.removeItem('user');
    }
});
