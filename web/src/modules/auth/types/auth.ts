export interface LoginPayload {
    email: string
    password: string
}

export interface InitTelegramVerificationPayload {
    phone_number: string
}

export interface VerifyTelegramCodePayload {
    phone_number: string
    code: string
}

export interface AuthUser {
    id: string
    email: string
    phone_number: string
    role_description: string
    is_verified: boolean
    workspace_id: string
}

export interface AuthWorkspace {
    id: string
    company_name: string
    business_direction: string
    usage_purpose: string
    team_size: string
    has_team: boolean
}

export interface AuthResponse {
    user: AuthUser
    workspace: AuthWorkspace
}

export interface SessionResponse {
    authenticated: boolean
    user: AuthUser | null
    workspace: AuthWorkspace | null
}

export interface InitTelegramVerificationResponse {
    bot_url: string
    expires_at: string
}

export interface VerifyTelegramCodeResponse {
    verified: boolean
    status: string
    expires_at: string | null
}