import { writable } from 'svelte/store';
import { type User } from '$lib/type/resources/user';

const isBrowser = typeof localStorage !== 'undefined';

// Lire le user depuis localStorage (si présent)
const storedUser: User | null = isBrowser
  ? JSON.parse(localStorage.getItem('arosaje.user') || 'null')
  : null;

export const user = writable<User | null>(storedUser);

// Persister le user dans localStorage à chaque changement
user.subscribe((value) => {
  if (!isBrowser) return;

  if (value) {
    localStorage.setItem('arosaje.user', JSON.stringify(value));
  } else {
    localStorage.removeItem('arosaje.user');
  }
});