import { create } from "zustand"

import {
    DEFAULT_ONBOARDING_DRAFT,
} from "@/modules/auth/lib/onboarding"
import type { OnboardingDraft, SignUpStep } from "@/modules/auth/types/onboarding"

type OnboardingStore = {
    draft: OnboardingDraft
    currentStep: SignUpStep
    completedStep: number
    telegramBotUrl: string | null
    verificationExpiresAt: number | null
    setCurrentStep: (step: SignUpStep) => void
    updateDraft: (values: Partial<OnboardingDraft>) => void
    completeStep: (step: SignUpStep, values: Partial<OnboardingDraft>) => void
    setTelegramVerification: (payload: {
        countryCode: string
        phoneNumber: string
        botUrl: string
        expiresAt: string
    }) => void
    reset: () => void
}

export const useOnboardingStore = create<OnboardingStore>((set) => ({
    draft: DEFAULT_ONBOARDING_DRAFT,
    currentStep: 1,
    completedStep: 0,
    telegramBotUrl: null,
    verificationExpiresAt: null,
    setCurrentStep: (step) => set({ currentStep: step }),
    updateDraft: (values) =>
        set((state) => ({
            draft: {
                ...state.draft,
                ...values,
            },
        })),
    completeStep: (step, values) =>
        set((state) => ({
            draft: {
                ...state.draft,
                ...values,
            },
            currentStep: step,
            completedStep: Math.max(state.completedStep, step),
        })),
    setTelegramVerification: ({ countryCode, phoneNumber, botUrl, expiresAt }) => {
        set((state) => ({
            draft: {
                ...state.draft,
                country_code: countryCode,
                phone_number: phoneNumber,
            },
            telegramBotUrl: botUrl,
            verificationExpiresAt: new Date(expiresAt).getTime(),
        }))
    },
    reset: () =>
        set({
            draft: DEFAULT_ONBOARDING_DRAFT,
            currentStep: 1,
            completedStep: 0,
            telegramBotUrl: null,
            verificationExpiresAt: null,
        }),
}))