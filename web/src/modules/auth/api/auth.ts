"use client"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import axios from "axios"

import { queryKeys } from "@/lib/query-keys"
import { toOnboardingPayload } from "@/modules/auth/lib/onboarding"
import type { OnboardingDraft } from "@/modules/auth/types/onboarding"

import { authApiClient } from "./client"
import type {
    AuthResponse,
    Invitation,
    InvitationAcceptPayload,
    InvitationCreatePayload,
    InvitationListResponse,
    InvitationTokenResponse,
    InitTelegramVerificationPayload,
    InitTelegramVerificationResponse,
    LoginPayload,
    SessionResponse,
    VerifyTelegramCodePayload,
    VerifyTelegramCodeResponse,
} from "@/modules/auth/types/auth"

const SESSION_QUERY_KEY = queryKeys.auth.session()

type RetryCount = number

function shouldRetryAuthQueries(failureCount: RetryCount, error: unknown) {
    if (!axios.isAxiosError(error)) {
        return failureCount < 1
    }

    const status = error.response?.status
    if (status === 401 || status === 403) {
        return false
    }

    return failureCount < 1
}

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

export async function createInvitation(payload: InvitationCreatePayload) {
    const response = await authApiClient.post<InvitationTokenResponse>("/api/v1/auth/invitations", payload)
    return response.data
}

export async function getInvitations() {
    const response = await authApiClient.get<InvitationListResponse>("/api/v1/auth/invitations")
    return response.data
}

export async function resendInvitation(invitationId: string) {
    const response = await authApiClient.post<InvitationTokenResponse>(
        `/api/v1/auth/invitations/${invitationId}/resend`
    )
    return response.data
}

export async function updateInvitationRole(invitationId: string, role_description: Invitation["role_description"]) {
    const response = await authApiClient.patch<Invitation>(`/api/v1/auth/invitations/${invitationId}`, {
        role_description,
    })
    return response.data
}

export async function revokeInvitation(invitationId: string) {
    await authApiClient.delete(`/api/v1/auth/invitations/${invitationId}`)
}

export async function acceptInvitation(payload: InvitationAcceptPayload) {
    const response = await authApiClient.post<AuthResponse>("/api/v1/auth/invitations/accept", payload)
    return response.data
}

export function useSessionQuery(enabled = true) {
    return useQuery({
        queryKey: SESSION_QUERY_KEY,
        queryFn: getSession,
        enabled,
        retry: shouldRetryAuthQueries,
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