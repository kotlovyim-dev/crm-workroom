export type AuthAwareSession = {
    authenticated: boolean
} | null | undefined

export function isAuthAwareQueryEnabled(session: AuthAwareSession, enabled = true) {
    return enabled && session?.authenticated === true
}