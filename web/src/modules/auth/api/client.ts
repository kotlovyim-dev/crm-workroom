"use client"

import axios from "axios"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8080"

export const authApiClient = axios.create({
    baseURL: API_BASE_URL,
    withCredentials: true,
})

let refreshRequest: Promise<unknown> | null = null

authApiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const status = error.response?.status
        const originalRequest = error.config
        const requestUrl = originalRequest?.url ?? ""

        if (
            status !== 401 ||
            !originalRequest ||
            originalRequest._retry ||
            requestUrl.includes("/api/v1/auth/refresh") ||
            requestUrl.includes("/api/v1/auth/login") ||
            requestUrl.includes("/api/v1/auth/register-workspace") ||
            requestUrl.includes("/api/v1/auth/logout")
        ) {
            return Promise.reject(error)
        }

        originalRequest._retry = true

        refreshRequest ??= authApiClient.post("/api/v1/auth/refresh").finally(() => {
            refreshRequest = null
        })

        await refreshRequest
        return authApiClient(originalRequest)
    }
)

export function getApiErrorMessage(error: unknown, fallbackMessage: string) {
    if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail
        if (typeof detail === "string" && detail.trim()) {
            return detail
        }
    }

    return fallbackMessage
}