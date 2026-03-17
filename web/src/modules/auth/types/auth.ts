export interface LoginPayload {
    email: string
    password: string
    remember_me?: boolean
}

export type CanonicalRole = "Admin/Owner" | "PM/Team Lead" | "Team Member"

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
    role_description: CanonicalRole
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

export interface Invitation {
    id: string
    workspace_id: string
    email: string
    invited_by_user_id: string
    role_description: CanonicalRole
    status: string
    expires_at: string
    accepted_at: string | null
    revoked_at: string | null
    created_at: string
}

export interface InvitationTokenResponse {
    invitation: Invitation
    token: string
}

export interface InvitationListResponse {
    items: Invitation[]
}

export interface InvitationAcceptPayload {
    token: string
    transfer_confirmed: boolean
}

export interface InvitationCreatePayload {
    email: string
    role_description: CanonicalRole
}