export class HttpError extends Error {
	constructor(
		public readonly message: string,
		public readonly status: number,
		public readonly body = null,
	) {
		super(message);
		Object.setPrototypeOf(this, HttpError.prototype);
		this.name = this.constructor.name;
		this.stack = new Error(message).stack;
	}
}