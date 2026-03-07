import { create } from "zustand"

import {
    buildTelegramBotUrl,
    DEFAULT_ONBOARDING_DRAFT,
    formatPhoneNumber,
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
    requestTelegramVerification: (countryCode: string, phoneNumber: string) => void
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
    requestTelegramVerification: (countryCode, phoneNumber) => {
        const fullPhoneNumber = formatPhoneNumber(countryCode, phoneNumber)

        set((state) => ({
            draft: {
                ...state.draft,
                country_code: countryCode,
                phone_number: phoneNumber,
            },
            telegramBotUrl: buildTelegramBotUrl(fullPhoneNumber),
            verificationExpiresAt: Date.now() + 5 * 60_000,
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