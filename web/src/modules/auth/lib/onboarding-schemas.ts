import { z } from "zod"

import { TEAM_SIZE_OPTIONS } from "@/modules/auth/lib/onboarding"

const optionalEmailSchema = z.string().trim().superRefine((value, context) => {
    if (!value) {
        return
    }

    if (!z.email().safeParse(value).success) {
        context.addIssue({
            code: "custom",
            message: "Please enter a valid email address.",
        })
    }
})

export const signUpStepOneSchema = z.object({
    country_code: z.string().min(2, { message: "Select a country code." }),
    phone_number: z
        .string()
        .trim()
        .min(7, { message: "Please enter your phone number." })
        .regex(/^[\d\s()-]+$/, { message: "Use numbers only." }),
    telegram_code: z
        .string()
        .trim()
        .length(6, { message: "Enter the 6-digit Telegram code." }),
    email: z.email({ message: "Please enter a valid email address." }),
    password: z.string().min(8, { message: "Password must be at least 8 characters." }),
})

export const signUpStepTwoSchema = z.object({
    usage_purpose: z.string().min(1, { message: "Select how you will use the service." }),
    role_description: z.string().min(1, { message: "Select what describes you best." }),
    additional_boolean_question: z.boolean(),
})

export const signUpStepThreeSchema = z.object({
    company_name: z.string().trim().min(2, { message: "Enter your company name." }),
    business_direction: z.string().min(1, { message: "Select a business direction." }),
    team_size: z.enum(TEAM_SIZE_OPTIONS, {
        message: "Choose how many people are in your team.",
    }),
})

export const signUpStepFourSchema = z.object({
    invited_members: z.array(optionalEmailSchema).min(1),
})

export type SignUpStepOneValues = z.infer<typeof signUpStepOneSchema>
export type SignUpStepTwoValues = z.infer<typeof signUpStepTwoSchema>
export type SignUpStepThreeValues = z.infer<typeof signUpStepThreeSchema>
export type SignUpStepFourValues = z.infer<typeof signUpStepFourSchema>