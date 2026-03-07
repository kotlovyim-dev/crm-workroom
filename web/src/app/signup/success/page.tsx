import type { Metadata } from "next"

import { SignupSuccessCard } from "@/modules/auth/components/signup-success-card"

export const metadata: Metadata = {
    title: "Registration Complete | CRM Workroom",
    description: "Your CRM Workroom workspace has been created successfully.",
}

export default function SignupSuccessPage() {
    return <SignupSuccessCard />
}