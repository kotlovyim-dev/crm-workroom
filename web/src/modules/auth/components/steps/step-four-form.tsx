"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { Plus } from "lucide-react"
import { useForm, useWatch } from "react-hook-form"

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
    signUpStepFourSchema,
    type SignUpStepFourValues,
} from "@/modules/auth/lib/onboarding-schemas"
import { useOnboardingStore } from "@/modules/auth/store/onboarding-store"

type StepFourFormProps = {
    formId: string
    onComplete: (values: SignUpStepFourValues) => void
}

export function StepFourForm({ formId, onComplete }: StepFourFormProps) {
    const draft = useOnboardingStore((state) => state.draft)

    const form = useForm<SignUpStepFourValues>({
        resolver: zodResolver(signUpStepFourSchema),
        defaultValues: {
            invited_members: draft.invited_members.length > 0 ? draft.invited_members : [""],
        },
    })

    const invitedMembers = useWatch({
        control: form.control,
        name: "invited_members",
    }) ?? []

    return (
        <Form {...form}>
            <form id={formId} onSubmit={form.handleSubmit(onComplete)} className="space-y-5 lg:space-y-4">
                {invitedMembers.map((_, index) => (
                    <FormField
                        key={index}
                        control={form.control}
                        name={`invited_members.${index}`}
                        render={({ field: emailField }) => (
                            <FormItem>
                                <FormLabel className="text-sm font-bold text-muted-foreground">
                                    Member&apos;s Email
                                </FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="memberemail@gmail.com"
                                        className="h-12 rounded-2xl px-4 text-base"
                                        {...emailField}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                ))}

                <Button
                    type="button"
                    variant="link"
                    onClick={() =>
                        form.setValue("invited_members", [...invitedMembers, ""], {
                            shouldDirty: true,
                        })
                    }
                    className="h-auto px-0 text-base font-semibold text-primary"
                >
                    <Plus className="size-5" />
                    Add another Member
                </Button>
            </form>
        </Form>
    )
}