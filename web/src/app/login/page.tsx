import { LoginLayout } from "@/modules/auth/components/login-layout"
import { SignInCard } from "@/modules/auth/components/sign-in-card"

export const metadata = {
    title: "Sign In | CRM Workroom",
    description: "Sign in to your CRM Workroom account.",
}

export default function LoginPage() {
    return (
        <LoginLayout>
            <SignInCard />
        </LoginLayout>
    )
}
