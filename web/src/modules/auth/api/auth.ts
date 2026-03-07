"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { toOnboardingPayload } from "@/modules/auth/lib/onboarding"
import type { OnboardingDraft } from "@/modules/auth/types/onboarding"

import { authApiClient } from "./client"
import type {
    AuthResponse,
    InitTelegramVerificationPayload,
    InitTelegramVerificationResponse,
    LoginPayload,
    SessionResponse,
    VerifyTelegramCodePayload,
    VerifyTelegramCodeResponse,
} from "@/modules/auth/types/auth"

const SESSION_QUERY_KEY = ["auth", "session"]

export async function login(payload: LoginPayload) {
    const response = await authApiClient.post<AuthResponse>("/api/v1/auth/login", payload)
    return response.data
}

export async function initTelegramVerification(payload: InitTelegramVerificationPayload) {
    const response = await authApiClient.post<InitTelegramVerificationResponse>(
        "/api/v1/auth/init-telegram-verification",
        payload
    )
    return response.data
}

export async function verifyTelegramCode(payload: VerifyTelegramCodePayload) {
    const response = await authApiClient.post<VerifyTelegramCodeResponse>(
        "/api/v1/auth/verify-telegram-code",
        payload
    )
    return response.data
}

export async function registerWorkspace(draft: OnboardingDraft) {
    const response = await authApiClient.post<AuthResponse>(
        "/api/v1/auth/register-workspace",
        toOnboardingPayload(draft)
    )
    return response.data
}

export async function getSession() {
    const response = await authApiClient.get<SessionResponse>("/api/v1/auth/me")
    return response.data
}

export async function logout() {
    await authApiClient.post("/api/v1/auth/logout")
}

export function useSessionQuery(enabled = true) {
    return useQuery({
        queryKey: SESSION_QUERY_KEY,
        queryFn: getSession,
        enabled,
    })
}

export function useLoginMutation() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: login,
        onSuccess: (data) => {
            queryClient.setQueryData(SESSION_QUERY_KEY, {
                authenticated: true,
                user: data.user,
                workspace: data.workspace,
            } satisfies SessionResponse)
        },
    })
}

export function useInitTelegramVerificationMutation() {
    return useMutation({
        mutationFn: initTelegramVerification,
    })
}

export function useVerifyTelegramCodeMutation() {
    return useMutation({
        mutationFn: verifyTelegramCode,
    })
}

export function useRegisterWorkspaceMutation() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: registerWorkspace,
        onSuccess: (data) => {
            queryClient.setQueryData(SESSION_QUERY_KEY, {
                authenticated: true,
                user: data.user,
                workspace: data.workspace,
            } satisfies SessionResponse)
        },
    })
}

export function useLogoutMutation() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: logout,
        onSuccess: () => {
            queryClient.setQueryData(SESSION_QUERY_KEY, {
                authenticated: false,
                user: null,
                workspace: null,
            } satisfies SessionResponse)
        },
    })
}