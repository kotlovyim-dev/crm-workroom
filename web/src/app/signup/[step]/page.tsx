import type { Metadata } from "next"
import { notFound } from "next/navigation"

import { SignUpFlow } from "@/modules/auth/components/signup-flow"
import { parseSignUpStepSlug } from "@/modules/auth/lib/onboarding"

export const metadata: Metadata = {
    title: "Sign Up | CRM Workroom",
    description: "Create your CRM Workroom account and set up your team.",
}

type SignupStepPageProps = {
    params: Promise<{
        step: string
    }>
}

export default async function SignupStepPage({ params }: SignupStepPageProps) {
    const { step } = await params
    const parsedStep = parseSignUpStepSlug(step)

    if (!parsedStep) {
        notFound()
    }

    return <SignUpFlow step={parsedStep} />
}