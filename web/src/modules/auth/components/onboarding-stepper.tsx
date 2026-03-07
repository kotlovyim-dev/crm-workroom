import { Check } from "lucide-react"

import { ONBOARDING_STEPS } from "@/modules/auth/lib/onboarding"
import type { SignUpStep } from "@/modules/auth/types/onboarding"
import { cn } from "@/lib/utils"

type OnboardingStepperProps = {
    currentStep: SignUpStep
}

export function OnboardingStepper({ currentStep }: OnboardingStepperProps) {
    return (
        <ol className="space-y-6">
            {ONBOARDING_STEPS.map((item, index) => {
                const isCompleted = item.step < currentStep
                const isCurrent = item.step === currentStep
                const isLastItem = index === ONBOARDING_STEPS.length - 1

                return (
                    <li key={item.step} className="flex gap-4">
                        <div className="flex w-6 flex-col items-center">
                            <span
                                className={cn(
                                    "flex size-6 items-center justify-center rounded-full border transition-colors",
                                    isCompleted && "border-primary-foreground bg-primary-foreground text-primary",
                                    isCurrent && "border-primary-foreground bg-transparent text-primary-foreground",
                                    !isCompleted && !isCurrent && "border-primary-foreground/60 bg-transparent text-transparent"
                                )}
                            >
                                {isCompleted ? <Check className="size-4" /> : <span className="size-2 rounded-full bg-current" />}
                            </span>
                            {!isLastItem ? (
                                <span
                                    className={cn(
                                        "mt-2 h-8 w-px rounded-full",
                                        item.step < currentStep ? "bg-primary-foreground" : "bg-primary-foreground/35"
                                    )}
                                />
                            ) : null}
                        </div>

                        <span
                            className={cn(
                                "pt-0.5 text-xl font-semibold leading-7",
                                isCurrent || isCompleted ? "text-primary-foreground" : "text-primary-foreground/55"
                            )}
                        >
                            {item.label}
                        </span>
                    </li>
                )
            })}
        </ol>
    )
}