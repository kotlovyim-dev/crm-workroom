"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import {
    BUSINESS_DIRECTION_OPTIONS,
    TEAM_SIZE_OPTIONS,
} from "@/modules/auth/lib/onboarding"
import {
    signUpStepThreeSchema,
    type SignUpStepThreeValues,
} from "@/modules/auth/lib/onboarding-schemas"
import { useOnboardingStore } from "@/modules/auth/store/onboarding-store"
import { cn } from "@/lib/utils"

type StepThreeFormProps = {
    formId: string
    onComplete: (values: SignUpStepThreeValues) => void
}

export function StepThreeForm({ formId, onComplete }: StepThreeFormProps) {
    const draft = useOnboardingStore((state) => state.draft)

    const form = useForm<SignUpStepThreeValues>({
        resolver: zodResolver(signUpStepThreeSchema),
        defaultValues: {
            company_name: draft.company_name,
            business_direction: draft.business_direction,
            team_size: draft.team_size || undefined,
        },
    })

    return (
        <Form {...form}>
            <form id={formId} onSubmit={form.handleSubmit(onComplete)} className="space-y-6 lg:space-y-5">
                <FormField
                    control={form.control}
                    name="company_name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel className="text-sm font-bold text-muted-foreground">Your Company&apos;s Name</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="Company&apos;s Name"
                                    className="h-12 rounded-2xl px-4 text-base"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="business_direction"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel className="text-sm font-bold text-muted-foreground">Business Direction</FormLabel>
                            <Select onValueChange={field.onChange} value={field.value}>
                                <FormControl>
                                    <SelectTrigger className="h-12 w-full rounded-2xl px-4 text-base">
                                        <SelectValue placeholder="IT and programming" />
                                    </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                    {BUSINESS_DIRECTION_OPTIONS.map((option) => (
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
                    name="team_size"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel className="text-sm font-bold text-muted-foreground">How many people in your team?</FormLabel>
                            <FormControl>
                                <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                                    {TEAM_SIZE_OPTIONS.map((option) => {
                                        const isSelected = field.value === option

                                        return (
                                            <Button
                                                key={option}
                                                type="button"
                                                variant={isSelected ? "default" : "outline"}
                                                onClick={() => field.onChange(option)}
                                                className={cn(
                                                    "h-11 rounded-2xl px-4 text-sm font-semibold shadow-sm lg:h-12",
                                                    !isSelected && "text-muted-foreground"
                                                )}
                                            >
                                                {option}
                                            </Button>
                                        )
                                    })}
                                </div>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
            </form>
        </Form>
    )
}