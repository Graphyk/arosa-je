import { type DataProvider } from './type/dataProvider';

import { HttpError } from './error/httpError';
import authProvider from '$lib/authProvider';
import { type Options } from './type/http/options';

import { customFetch } from './fetch';

export function formDataToJson(formData: FormData): Record<string, FormDataEntryValue | unknown> {
	return Object.fromEntries(formData.entries());
}

const httpClient = async (path: string | URL, options: Options = {}) => {
	console.log(await authProvider.token());
	let token = await authProvider.token();
	const user = () =>
		token ? { token: `Bearer ${token}`, authenticated: Boolean(token) } : undefined;

	try {
		return await customFetch(path, { ...options, user: user() });
	} catch (error) {
		if (error instanceof HttpError && error?.status === 401) {
			if (authProvider.isAuthenticated()) {
				try {
					token = await authProvider.token();
					return await customFetch(path, { ...options, user: user() });
				} catch (error) {
					if (error instanceof HttpError && error?.status === 401) {
						window.location.href = '/login';
					}
					throw error;
				}
			}
		}
		throw error;
	}
};

const dataProvider = ((_httpClient: typeof customFetch = httpClient): DataProvider => {
	const fetchRoute = async (route: string, options: Options = {}) =>
		_httpClient(new URL(route, window.location.origin), options);

	return {
		getList: async (resource, params) => {
			const query = new URLSearchParams();
			if (params?.filter) {
				for (const [key, value] of Object.entries(params?.filter)) {
					if (value === undefined) continue;
					if (value instanceof Array) {
						value.forEach((elt) => {
							if (query.has(key)) {
								query.set(key, query.get(key) + ',' + elt);
							} else {
								query.append(key, elt);
							}
						});
						continue;
					}
					query.append(key, value);
				}
			}
			if (params?.sort?.length) {
				query.append(
					'sort',
					params.sort
						.map((p) => {
							const order = (p.order ?? 'ASC') == 'DESC' ? '-' : '';
							const nullFirst = p.nullFirst ? '~' : '';
							return `${order}${nullFirst}${p.field}`;
						})
						.join(','),
				);
			}

			if (params?.pagination?.limit) {
				query.append('limit', params?.pagination?.limit.toString());
			}

			if (params?.pagination?.offset) {
				query.append('offset', params?.pagination?.offset.toString());
			}

			const url = `${resource}?${query}`;

			let options = {};
			if (params?.meta?.extraHeaders) {
				options = { headers: new Headers(params.meta.extraHeaders) };
			}

			const { headers, json } = await fetchRoute(url, options);

			return {
				data: json,
				pageInfo: {
					hasMore: headers.get('x-has-more') === 'True',
					previousOffset: parseInt(headers.get('x-previous-offset') || '0'),
					nextOffset: parseInt(headers.get('x-next-offset') || '0'),
				},
			};
		},
		getCount: async (resource, params) => {
			const query = new URLSearchParams();
			if (params?.filter) {
				for (const [key, value] of Object.entries(params?.filter)) {
					if (value === undefined) continue;
					if (value instanceof Array) {
						value.forEach((elt) => {
							query.append(key, elt);
						});
						continue;
					}
					query.append(key, value);
				}
			}

			let options = {};
			if (params?.meta?.extraHeaders) {
				options = { headers: new Headers(params.meta.extraHeaders) };
			}

			const url = `${resource}/count?${query}`;

			const res = await fetchRoute(url, options);

			return res.json;
		},
		get: async (resource, params) => {
			return fetchRoute(`${resource}${params?.id || ''}`).then(({ json }) => ({ data: json }));
		},
		update: async (resource, params) => {
			return fetchRoute(`${resource}/${params.id}`, {
				method: 'PUT',
				body: JSON.stringify(params.data),
			}).then(({ json }) => ({ data: json }));
		},
		patch: async (resource, params) => {
			let url = `${resource}/${params.id}`;
			if (
				params?.meta?.queryParams &&
				params.meta.queryParams instanceof URLSearchParams &&
				params.meta.queryParams.size > 0
			) {
				url += `?${params.meta.queryParams.toString()}`;
			}
			return fetchRoute(url, {
				method: 'PATCH',
				body: params.data instanceof FormData ? params.data : JSON.stringify(params.data),
			}).then(({ json }) => ({ data: json }));
		},
		create: async (resource, params) => {
			const data = params.data instanceof FormData ? params.data : JSON.stringify(params.data);
			let url = `${resource}`;
			if (
				params?.meta?.queryParams &&
				params.meta.queryParams instanceof URLSearchParams &&
				params.meta.queryParams.size > 0
			) {
				url += `?${params.meta.queryParams.toString()}`;
			}
			return fetchRoute(url, {
				method: 'POST',
				body: data,
			}).then(async ({ headers, status, json }) => {
				if (status == 201) {
					const { json } = await fetchRoute(URL.parse(headers.get('Location') ?? '').pathname);
					return Promise.resolve({ data: json });
				}
				if (status == 204) {
					return Promise.resolve({ data: {} });
				}
				return Promise.reject(new HttpError(json && json.message, status, json));
			});
		},
		delete: async (resource, params) => {
			let url = `${resource}/${params.id}`;

			if (
				params?.meta?.queryParams &&
				params.meta.queryParams instanceof URLSearchParams &&
				params.meta.queryParams.size > 0
			) {
				url += `?${params.meta.queryParams.toString()}`;
			}

			return fetchRoute(url, {
				method: 'DELETE',
				body: JSON.stringify(params.data),
			}).then(({ json }) => ({ data: json }));
		},
	};
})();

export default dataProvider;