export interface ApiErrorResponse {
    detail?: string
}

export interface PaginatedResponse<TItem> {
    items: TItem[]
    page: number
    limit: number
    total: number
}

export interface AttachmentMetadata {
    id: string
    object_key: string
    file_name: string
    content_type: string
    size_bytes: number
    download_url?: string | null
    uploaded_at?: string | null
}

export type QueryKeyPrimitive = string | number | boolean | null | undefined

export type QueryKeyParams = Record<
    string,
    QueryKeyPrimitive | readonly QueryKeyPrimitive[]
>