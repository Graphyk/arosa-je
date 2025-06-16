import { HttpError } from "$lib/error/httpError";
import { type Options } from "$lib/type/http/options";

const createHeadersFromOptions = (options: Options): Headers => {
	const requestHeaders = (options.headers ||
		new Headers({
			Accept: 'application/json',
		})) as Headers;
	const hasBody = options && options.body;
	const isContentTypeSet = requestHeaders.has('Content-Type');
	const isGetMethod = !options?.method || options?.method === 'GET';
	const isFormData = options?.body instanceof FormData;

	const shouldSetContentType = hasBody && !isContentTypeSet && !isGetMethod && !isFormData;
	if (shouldSetContentType) {
		requestHeaders.set('Content-Type', 'application/json');
	}

	if (options.user && options.user.authenticated && options.user.token) {
		requestHeaders.set('Authorization', options.user.token);
	}

	return requestHeaders;
};

export const customFetch = async (url: string | URL, options: Options = {}) => {
	const requestHeaders = createHeadersFromOptions(options);

	let timeoutId;
	if (options?.timeout) {
		const controller = new AbortController();
		timeoutId = setTimeout(() => controller.abort(), options.timeout);
		options.signal = controller.signal;
	}

	const response = await fetch(url, { ...options, headers: requestHeaders })
		.then((response) =>
			response.text().then((text) => ({
				status: response.status,
				statusText: response.statusText,
				headers: response.headers,
				body: text,
			})),
		)
		.then(({ status, statusText, headers, body }) => {
			let json;
			try {
				json = JSON.parse(body);
			} catch {
				// not json, no big deal
			}
			if (status < 200 || status >= 300) {
				return Promise.reject(
					new HttpError((json && json?.message) || json || statusText, status, json || body),
				);
			}
			return Promise.resolve({ status, headers, body, json });
		});
	if (timeoutId) clearTimeout(timeoutId);
	return response;
};
