import type { OnboardingDraft, OnboardingPayload, SignUpStep, TeamSize } from "@/modules/auth/types/onboarding"

export const TOTAL_SIGN_UP_STEPS = 4

export const ONBOARDING_STEPS: Array<{ step: SignUpStep; label: string }> = [
    { step: 1, label: "Valid your phone" },
    { step: 2, label: "Tell about yourself" },
    { step: 3, label: "Tell about your company" },
    { step: 4, label: "Invite Team Members" },
]

export const USAGE_PURPOSE_OPTIONS = ["Work", "Personal projects", "Agency", "Education"] as const

export const ROLE_DESCRIPTION_OPTIONS = [
    "Business Owner",
    "Team Lead",
    "Project Manager",
    "Operations Manager",
] as const

export const BUSINESS_DIRECTION_OPTIONS = [
    "IT and programming",
    "Marketing",
    "Design",
    "Consulting",
    "Sales",
] as const

export const TEAM_SIZE_OPTIONS: TeamSize[] = [
    "Only me",
    "2 - 5",
    "6 - 10",
    "11 - 20",
    "21 - 40",
    "41 - 50",
    "51 - 100",
    "101 - 500",
]

export const DEFAULT_ONBOARDING_DRAFT: OnboardingDraft = {
    country_code: "+1",
    phone_number: "",
    telegram_code: "",
    email: "",
    password: "",
    usage_purpose: "",
    role_description: "",
    additional_boolean_question: true,
    company_name: "",
    team_size: "",
    business_direction: "",
    invited_members: [""],
}

export function getSignUpStepHref(step: SignUpStep) {
    return `/signup/step-${step}`
}

export function parseSignUpStepSlug(step: string): SignUpStep | null {
    if (!/^step-[1-4]$/.test(step)) {
        return null
    }

    return Number(step.replace("step-", "")) as SignUpStep
}

export function formatPhoneNumber(countryCode: string, phoneNumber: string) {
    const normalizedCountryCode = countryCode.trim()
    const normalizedPhoneNumber = phoneNumber.replace(/[^\d]/g, "")

    return `${normalizedCountryCode}${normalizedPhoneNumber}`
}

export function buildTelegramBotUrl(phoneNumber: string) {
    const payload = phoneNumber.replace(/[^\d+]/g, "")

    return `https://t.me/workroom_verification_bot?start=${encodeURIComponent(payload)}`
}

export function toOnboardingPayload(draft: OnboardingDraft): OnboardingPayload {
    return {
        phone_number: formatPhoneNumber(draft.country_code, draft.phone_number),
        telegram_code: draft.telegram_code,
        email: draft.email,
        password: draft.password,
        usage_purpose: draft.usage_purpose,
        role_description: draft.role_description,
        additional_boolean_question: draft.additional_boolean_question,
        company_name: draft.company_name,
        team_size: draft.team_size,
        business_direction: draft.business_direction,
        invited_members: draft.invited_members.filter(Boolean),
    }
}