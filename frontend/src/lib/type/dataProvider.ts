export type RecordType = Record<string, any>;
export type IdentifierType = number | string;

/**
 * dataProvider types
 */

export type DataProvider<ResourceType extends string = string> = {
	getList: <RecordType extends Record<string, any> = any>(
		resource: ResourceType,
		params?: GetListParams,
	) => Promise<GetListResult<RecordType>>;

	getCount: (resource: ResourceType, params?: GetCountParams) => Promise<GetCountResult>;

	get: <RecordType extends Record<string, any> = any>(
		resource: ResourceType,
		params?: GetParams,
	) => Promise<GetResult<RecordType>>;

	update: <RecordType extends Record<string, any> = any>(
		resource: ResourceType,
		params: UpdateParams,
	) => Promise<UpdateResult<RecordType>>;

	patch: <RecordType extends Record<string, any> = any>(
		resource: ResourceType,
		params: UpdateParams,
	) => Promise<UpdateResult<RecordType>>;

	create: <
		RecordType extends Omit<Record<string, any>, 'id'> = any,
		ResultRecordType extends Record<string, any> = RecordType & { id: IdentifierType },
	>(
		resource: ResourceType,
		params: CreateParams,
	) => Promise<CreateResult<ResultRecordType>>;

	delete: <RecordType extends Record<string, any> = any>(
		resource: ResourceType,
		params: DeleteParams,
	) => Promise<DeleteResult<RecordType>>;

	[key: string]: any;
};

export interface FilterPayload {
	[name: string]: unknown;
}

export interface PaginationPayload {
	offset?: number;
	limit?: number;
}

export interface SortPayload {
	field: string;
	order?: 'ASC' | 'DESC';
	nullFirst?: boolean;
}

export interface GetListParams {
	sort?: SortPayload[];
	filter?: FilterPayload;
	pagination?: PaginationPayload;
	meta?: unknown;
}

export interface GetListResult<RecordType = any> {
	data: RecordType[];
	count?: number;
	pageInfo?: {
		hasMore: boolean;
		previousOffset: number;
		nextOffset: number;
	};
}

export interface GetCountParams {
	filter?: FilterPayload;
	meta?: any;
}

export interface GetCountResult {
	count: number;
}

export interface GetParams {
	id: IdentifierType;
	meta?: any;
}
export interface GetResult<RecordType = any> {
	data: RecordType;
}

export interface UpdateParams<RecordType = any> {
	id: IdentifierType;
	data: Partial<RecordType> | FormData;
	meta?: any;
}
export interface UpdateResult<RecordType = any> {
	data: RecordType;
}

export interface CreateParams<RecordType = any> {
	data: Partial<RecordType> | FormData;
	meta?: any;
}
export interface CreateResult<RecordType = any> {
	data: RecordType;
}

export interface DeleteParams {
	id: IdentifierType;
	meta?: any;
}
export interface DeleteResult<RecordType = any> {
	data: RecordType;
}
