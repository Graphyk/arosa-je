export interface Options extends RequestInit {
	timeout?: number;
	user?: {
		authenticated?: boolean;
		token?: string;
	};
}