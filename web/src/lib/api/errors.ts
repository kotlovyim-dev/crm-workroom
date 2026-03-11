import axios from "axios"

import type { ApiErrorResponse } from "@/lib/api/contracts"

export function getApiErrorMessage(error: unknown, fallbackMessage: string) {
    if (axios.isAxiosError<ApiErrorResponse>(error)) {
        const detail = error.response?.data?.detail
        if (typeof detail === "string" && detail.trim()) {
            return detail
        }
    }

    return fallbackMessage
}