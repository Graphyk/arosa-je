import type { RefreshTokenData, TokenData } from '$lib/types/auth';

import { customFetch } from './fetch';
import { browser } from '$app/environment';
import { jwtDecode } from 'jwt-decode';
import { get, writable, type Writable } from 'svelte/store';
import { HttpError } from './error/httpError';

// cache expiration to avoid unwraping the token every time
interface AuthProviderData {
	payload: TokenData;
	access_token_expire_at: Date;
	refresh_token_expire_at: Date;
    access_token: string;
    refresh_token: string;
}

export type LoginParams = {
        username: string;
        password: string;
    }

export interface AuthProvider<T> extends Writable<T> {
    login: (_: LoginParams) => Promise<void>;
    logout: () => void;
    isAuthenticated: () => boolean;
	token: () => Promise<string | null>
}

const ACCESS_TOKEN_KEY = 'arosaje.access_token';
const REFRESH_TOKEN_KEY = 'arosaje.refresh_token';

function isExpired(date: Date): boolean {
	// 1 minute before real expiration to avoid false negatives due to network latency
	return new Date().getTime() > date.getTime() - 60;
}

const authProvider = ((): AuthProvider<AuthProviderData> => {
	const auth = writable<AuthProviderData | null>(null);

	function setAuth(access_token: string, refresh_token: string | null) {
		const payload = jwtDecode<TokenData>(access_token);
		localStorage.setItem(ACCESS_TOKEN_KEY, access_token);
		
		if (refresh_token === null) {
			const stored_token = localStorage.getItem(REFRESH_TOKEN_KEY)
			if (stored_token === null) {
				throw new Error("there isn't any refresh token")
			}
			refresh_token = stored_token;
		} else {
			localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
		}
		auth.set({
			payload,
			access_token,
			access_token_expire_at: new Date(payload.exp * 1000),
			refresh_token,
			refresh_token_expire_at: new Date(jwtDecode<RefreshTokenData>(refresh_token).exp * 1000),
		});
	}

	if (browser && localStorage) {
		const access_token = localStorage.getItem(ACCESS_TOKEN_KEY);
		const refresh_token = localStorage.getItem(REFRESH_TOKEN_KEY);
		if (access_token && refresh_token) {
			setAuth(access_token, refresh_token);
		}
	}

	async function login(params: LoginParams): Promise<void> {
		const { json } = await customFetch('/api/token/', {
			method: 'POST',
			body: new URLSearchParams(params),
			headers: new Headers({
				'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
			}),
		});
		setAuth(json.access, json.refresh);
	}

	function logout() {
		localStorage.removeItem(ACCESS_TOKEN_KEY);
		localStorage.removeItem(REFRESH_TOKEN_KEY);
		auth.set(null);
		window.location.replace('/');
	}

	async function token(): Promise<string | null> {
		const token = get(auth);
		if (!token) {
			return null;
		}

		// Token not expired
		if (!isExpired(token.access_token_expire_at)) {
			return token.access_token;
		}

		// Can be refreshed
		if (!isExpired(token.refresh_token_expire_at)) {
			try {
				const { json } = await customFetch('/api/token/refresh/', {
					method: 'POST',
					body: JSON.stringify({ refresh: localStorage.getItem(REFRESH_TOKEN_KEY) }),
				});
				setAuth(json.access, json.refresh);
				return json.access_token;
			} catch (e) {
				if (!(e instanceof HttpError && e.status === 401)) {
					throw e;
				}
			}
		}

		logout();
		return null;
	}

	function isAuthenticated(): boolean {
		const data = get(auth);
		// Check only the refresh token as the access one will be auto refreshed
		return data ? data.refresh_token_expire_at > new Date() : false;
	}

	function getTokenData(): TokenData | null {
		const token = get(auth);
		return token ? token.payload : null;
	}

	return {
		...auth,
		login,
		logout,
		token,
		isAuthenticated,
		getTokenData,
	};
})();

export default authProvider;
