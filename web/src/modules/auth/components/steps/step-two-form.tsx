"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import {
    RadioGroup,
    RadioGroupItem,
} from "@/components/ui/radio-group"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import {
    ROLE_DESCRIPTION_OPTIONS,
    USAGE_PURPOSE_OPTIONS,
} from "@/modules/auth/lib/onboarding"
import {
    signUpStepTwoSchema,
    type SignUpStepTwoValues,
} from "@/modules/auth/lib/onboarding-schemas"
import { useOnboardingStore } from "@/modules/auth/store/onboarding-store"

type StepTwoFormProps = {
    formId: string
    onComplete: (values: SignUpStepTwoValues) => void
}

export function StepTwoForm({ formId, onComplete }: StepTwoFormProps) {
    const draft = useOnboardingStore((state) => state.draft)

    const form = useForm<SignUpStepTwoValues>({
        resolver: zodResolver(signUpStepTwoSchema),
        defaultValues: {
            usage_purpose: draft.usage_purpose,
            role_description: draft.role_description,
            additional_boolean_question: draft.additional_boolean_question,
        },
    })

    return (
        <Form {...form}>
            <form id={formId} onSubmit={form.handleSubmit(onComplete)} className="space-y-6 lg:space-y-5">
                <FormField
                    control={form.control}
                    name="usage_purpose"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel className="text-sm font-bold text-muted-foreground">Why will you use the service?</FormLabel>
                            <Select onValueChange={field.onChange} value={field.value}>
                                <FormControl>
                                    <SelectTrigger className="h-12 w-full rounded-2xl px-4 text-base">
                                        <SelectValue placeholder="Work" />
                                    </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                    {USAGE_PURPOSE_OPTIONS.map((option) => (
                                        <SelectItem key={option} value={option}>
                                            {option}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="role_description"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel className="text-sm font-bold text-muted-foreground">What describes you best?</FormLabel>
                            <Select onValueChange={field.onChange} value={field.value}>
                                <FormControl>
                                    <SelectTrigger className="h-12 w-full rounded-2xl px-4 text-base">
                                        <SelectValue placeholder="Business Owner" />
                                    </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                    {ROLE_DESCRIPTION_OPTIONS.map((option) => (
                                        <SelectItem key={option} value={option}>
                                            {option}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="additional_boolean_question"
                    render={({ field }) => (
                        <FormItem className="gap-4 sm:flex sm:flex-wrap sm:items-center sm:justify-between">
                            <FormLabel className="text-sm font-bold text-muted-foreground sm:pr-6">
                                Do you already have a team?
                            </FormLabel>
                            <FormControl>
                                <RadioGroup
                                    value={field.value ? "yes" : "no"}
                                    onValueChange={(value) => field.onChange(value === "yes")}
                                    className="flex items-center gap-8"
                                >
                                    <label className="flex items-center gap-3 text-xl text-foreground">
                                        <RadioGroupItem value="yes" className="size-5" />
                                        <span>Yes</span>
                                    </label>
                                    <label className="flex items-center gap-3 text-xl text-foreground">
                                        <RadioGroupItem value="no" className="size-5" />
                                        <span>No</span>
                                    </label>
                                </RadioGroup>
                            </FormControl>
                            <FormMessage className="sm:basis-full" />
                        </FormItem>
                    )}
                />
            </form>
        </Form>
    )
}