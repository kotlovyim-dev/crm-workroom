import { LoginLayout } from "@/modules/auth/components/login-layout"
import { SignInCard } from "@/modules/auth/components/sign-in-card"

export const metadata = {
    title: "Sign In | CRM Workroom",
    description: "Sign in to your CRM Workroom account.",
}

type LoginPageProps = {
    searchParams?: Promise<{
        reason?: string
    }>
}

export default async function LoginPage({ searchParams }: LoginPageProps) {
    const resolvedSearchParams = await searchParams
    const isSessionExpired = resolvedSearchParams?.reason === "session-expired"

    return (
        <LoginLayout>
            {isSessionExpired ? (
                <p className="mb-4 rounded-md border border-amber-400/30 bg-amber-100/40 px-3 py-2 text-sm text-amber-900">
                    Session expired. Please sign in again.
                </p>
            ) : null}
            <SignInCard />
        </LoginLayout>
    )
}
