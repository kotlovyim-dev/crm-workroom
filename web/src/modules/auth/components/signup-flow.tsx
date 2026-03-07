"use client"

import { startTransition, useEffect } from "react"
import { useRouter } from "next/navigation"

import { OnboardingShell } from "@/modules/auth/components/onboarding-shell"
import { StepFourForm } from "@/modules/auth/components/steps/step-four-form"
import { StepOneForm } from "@/modules/auth/components/steps/step-one-form"
import { StepThreeForm } from "@/modules/auth/components/steps/step-three-form"
import { StepTwoForm } from "@/modules/auth/components/steps/step-two-form"
import { getSignUpStepHref, TOTAL_SIGN_UP_STEPS } from "@/modules/auth/lib/onboarding"
import type {
    SignUpStepFourValues,
    SignUpStepOneValues,
    SignUpStepThreeValues,
    SignUpStepTwoValues,
} from "@/modules/auth/lib/onboarding-schemas"
import { useOnboardingStore } from "@/modules/auth/store/onboarding-store"
import type { SignUpStep } from "@/modules/auth/types/onboarding"

type SignUpFlowProps = {
    step: SignUpStep
}

export function SignUpFlow({ step }: SignUpFlowProps) {
    const router = useRouter()
    const completedStep = useOnboardingStore((state) => state.completedStep)
    const completeStep = useOnboardingStore((state) => state.completeStep)
    const setCurrentStep = useOnboardingStore((state) => state.setCurrentStep)

    useEffect(() => {
        const allowedStep = Math.min(completedStep + 1, TOTAL_SIGN_UP_STEPS) as SignUpStep

        if (step > allowedStep) {
            router.replace(getSignUpStepHref(allowedStep))
            return
        }

        setCurrentStep(step)
    }, [completedStep, router, setCurrentStep, step])

    const goToStep = (nextStep: SignUpStep) => {
        startTransition(() => {
            router.push(getSignUpStepHref(nextStep))
        })
    }

    const goToSuccess = () => {
        startTransition(() => {
            router.push("/signup/success")
        })
    }

    const handleStepOneComplete = (values: SignUpStepOneValues) => {
        completeStep(1, values)
        goToStep(2)
    }

    const handleStepTwoComplete = (values: SignUpStepTwoValues) => {
        completeStep(2, values)
        goToStep(3)
    }

    const handleStepThreeComplete = (values: SignUpStepThreeValues) => {
        completeStep(3, values)
        goToStep(4)
    }

    const handleStepFourComplete = (values: SignUpStepFourValues) => {
        completeStep(4, {
            invited_members: values.invited_members.map((item) => item.trim()).filter(Boolean),
        })
        goToSuccess()
    }

    if (step === 1) {
        return (
            <OnboardingShell currentStep={1} title="Valid your phone" formId="signup-step-1-form">
                <StepOneForm formId="signup-step-1-form" onComplete={handleStepOneComplete} />
            </OnboardingShell>
        )
    }

    if (step === 2) {
        return (
            <OnboardingShell
                currentStep={2}
                title="Tell about yourself"
                formId="signup-step-2-form"
                onPrevious={() => goToStep(1)}
            >
                <StepTwoForm formId="signup-step-2-form" onComplete={handleStepTwoComplete} />
            </OnboardingShell>
        )
    }

    if (step === 3) {
        return (
            <OnboardingShell
                currentStep={3}
                title="Tell about your company"
                formId="signup-step-3-form"
                onPrevious={() => goToStep(2)}
            >
                <StepThreeForm formId="signup-step-3-form" onComplete={handleStepThreeComplete} />
            </OnboardingShell>
        )
    }

    return (
        <OnboardingShell
            currentStep={4}
            title="Invite Team Members"
            formId="signup-step-4-form"
            onPrevious={() => goToStep(3)}
        >
            <StepFourForm formId="signup-step-4-form" onComplete={handleStepFourComplete} />
        </OnboardingShell>
    )
}