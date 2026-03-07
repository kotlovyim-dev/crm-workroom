export type SignUpStep = 1 | 2 | 3 | 4

export type TeamSize =
    | "Only me"
    | "2 - 5"
    | "6 - 10"
    | "11 - 20"
    | "21 - 40"
    | "41 - 50"
    | "51 - 100"
    | "101 - 500"

export interface OnboardingPayload {
    phone_number: string
    telegram_code: string
    email: string
    password: string
    usage_purpose: string
    role_description: string
    additional_boolean_question: boolean
    company_name: string
    team_size: TeamSize | ""
    business_direction: string
    invited_members: string[]
}

export interface OnboardingDraft extends Omit<OnboardingPayload, "phone_number"> {
    country_code: string
    phone_number: string
}