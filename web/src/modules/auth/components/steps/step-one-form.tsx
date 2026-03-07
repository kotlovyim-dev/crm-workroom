"use client"

import { useState } from "react"
import Link from "next/link"
import { zodResolver } from "@hookform/resolvers/zod"
import { ExternalLink, Eye, EyeOff, Info } from "lucide-react"
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
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { useVerificationCountdown } from "@/modules/auth/hooks/use-verification-countdown"
import {
    signUpStepOneSchema,
    type SignUpStepOneValues,
} from "@/modules/auth/lib/onboarding-schemas"
import { useOnboardingStore } from "@/modules/auth/store/onboarding-store"

const COUNTRY_CODES = ["+1", "+44", "+49", "+380"] as const

type StepOneFormProps = {
    formId: string
    onComplete: (values: SignUpStepOneValues) => void
}

export function StepOneForm({ formId, onComplete }: StepOneFormProps) {
    const [showPassword, setShowPassword] = useState(false)
    const draft = useOnboardingStore((state) => state.draft)
    const telegramBotUrl = useOnboardingStore((state) => state.telegramBotUrl)
    const verificationExpiresAt = useOnboardingStore((state) => state.verificationExpiresAt)
    const requestTelegramVerification = useOnboardingStore((state) => state.requestTelegramVerification)
    const { formattedTimeLeft, hasActiveCode } = useVerificationCountdown(verificationExpiresAt)

    const form = useForm<SignUpStepOneValues>({
        resolver: zodResolver(signUpStepOneSchema),
        defaultValues: {
            country_code: draft.country_code,
            phone_number: draft.phone_number,
            telegram_code: draft.telegram_code,
            email: draft.email,
            password: draft.password,
        },
    })

    const handleOpenTelegramBot = async () => {
        const isValid = await form.trigger(["country_code", "phone_number"])

        if (!isValid) {
            return
        }

        const { country_code, phone_number } = form.getValues()
        requestTelegramVerification(country_code, phone_number)
    }

    return (
        <Form {...form}>
            <form id={formId} onSubmit={form.handleSubmit(onComplete)} className="space-y-5 lg:space-y-4">
                <div className="space-y-2">
                    <FormLabel className="text-sm font-bold text-muted-foreground">Mobile Number</FormLabel>
                    <div className="grid grid-cols-[7rem_minmax(0,1fr)] items-start gap-3">
                        <FormField
                            control={form.control}
                            name="country_code"
                            render={({ field }) => (
                                <FormItem className="gap-0">
                                    <Select onValueChange={field.onChange} value={field.value}>
                                        <FormControl>
                                            <SelectTrigger className="h-12 min-h-12 rounded-2xl px-4 text-base leading-none">
                                                <SelectValue placeholder="Code" />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                            {COUNTRY_CODES.map((countryCode) => (
                                                <SelectItem key={countryCode} value={countryCode}>
                                                    {countryCode}
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
                            name="phone_number"
                            render={({ field }) => (
                                <FormItem className="gap-0">
                                    <FormControl>
                                        <Input
                                            placeholder="345 567-23-56"
                                            className="h-12 rounded-2xl px-4 text-base"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                    </div>
                </div>

                <div className="space-y-2">
                    <FormLabel className="text-sm font-bold text-muted-foreground">Code from Telegram bot</FormLabel>
                    <FormField
                        control={form.control}
                        name="telegram_code"
                        render={({ field }) => (
                            <FormItem>
                                <FormControl>
                                    <InputOTP
                                        maxLength={6}
                                        value={field.value}
                                        onChange={field.onChange}
                                        containerClassName="justify-start"
                                    >
                                        <InputOTPGroup className="gap-3">
                                            {Array.from({ length: 6 }).map((_, index) => (
                                                <InputOTPSlot
                                                    key={index}
                                                    index={index}
                                                    className="h-11 w-11 rounded-2xl border border-border shadow-xs first:rounded-2xl first:border last:rounded-2xl lg:h-12 lg:w-12"
                                                />
                                            ))}
                                        </InputOTPGroup>
                                    </InputOTP>
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                </div>

                <div className="rounded-2xl bg-secondary px-4 py-3 text-primary lg:px-5 lg:py-4">
                    <div className="flex items-start gap-3">
                        <Info className="mt-0.5 size-5 shrink-0" />
                        <div className="space-y-2">
                            <p className="text-sm font-semibold leading-5">
                                Open the Telegram bot, share your contact and paste the 6-digit code here.
                                {hasActiveCode ? ` The code will be valid for ${formattedTimeLeft}.` : " The code remains active for 05:00 after it is issued."}
                            </p>

                            <div className="flex flex-wrap items-center gap-2">
                                <Button
                                    type="button"
                                    variant="link"
                                    onClick={handleOpenTelegramBot}
                                    className="h-auto px-0 text-sm font-bold text-primary"
                                >
                                    Generate Telegram link
                                </Button>

                                {telegramBotUrl ? (
                                    <Button asChild variant="link" className="h-auto px-0 text-sm font-bold text-primary">
                                        <Link href={telegramBotUrl} target="_blank" rel="noreferrer" className="p-0"> 
                                            Open Telegram bot
                                            <ExternalLink className="size-4" />
                                        </Link>
                                    </Button>
                                ) : null}
                            </div>
                        </div>
                    </div>
                </div>

                <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel className="text-sm font-bold text-muted-foreground">Email Address</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="youremail@gmail.com"
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
                    name="password"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel className="text-sm font-bold text-muted-foreground">Create Password</FormLabel>
                            <FormControl>
                                <div className="relative">
                                    <Input
                                        type={showPassword ? "text" : "password"}
                                        placeholder="••••••••"
                                        className="h-12 rounded-2xl px-4 pr-12 text-base"
                                        {...field}
                                    />
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        size="icon-sm"
                                        onClick={() => setShowPassword((current) => !current)}
                                        className="absolute top-1/2 right-3 -translate-y-1/2 rounded-full text-muted-foreground"
                                        aria-label={showPassword ? "Hide password" : "Show password"}
                                    >
                                        {showPassword ? <EyeOff className="size-5" /> : <Eye className="size-5" />}
                                    </Button>
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