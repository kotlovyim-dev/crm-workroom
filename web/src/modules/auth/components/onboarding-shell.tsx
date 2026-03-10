import { ArrowLeft, ArrowRight } from "lucide-react"

import { AuthLogoMark } from "@/modules/auth/components/auth-logo-mark"
import { AuthViewport } from "@/modules/auth/components/auth-viewport"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { OnboardingStepper } from "@/modules/auth/components/onboarding-stepper"
import type { SignUpStep } from "@/modules/auth/types/onboarding"

type OnboardingShellProps = {
    currentStep: SignUpStep
    title: string
    children: React.ReactNode
    formId: string
    onPrevious?: () => void
    nextLabel?: string
    isSubmitting?: boolean
}

export function OnboardingShell({
    currentStep,
    title,
    children,
    formId,
    onPrevious,
    nextLabel = "Next Step",
    isSubmitting = false,
}: OnboardingShellProps) {
    return (
        <AuthViewport>
            <div className="mx-auto flex h-full w-full max-w-7xl flex-col gap-4 lg:grid lg:h-[calc(100vh-2.5rem)] lg:grid-cols-[21.5rem_minmax(0,1fr)]">
                <aside className="h-full hidden md:block rounded-3xl bg-primary px-8 py-8 text-primary-foreground lg:px-9 lg:py-10">
                    <div className="mb-10 lg:mb-12">
                        <AuthLogoMark priority />
                    </div>

                    <div className="mb-8 space-y-3 lg:mb-10">
                        <h1 className="text-4xl font-bold tracking-tight lg:text-5xl">Get started</h1>
                    </div>

                    <OnboardingStepper currentStep={currentStep} />
                </aside>

                <Card className="h-full overflow-hidden rounded-3xl border-border/60 py-0 shadow-xl">
                    <div className="flex h-full flex-col">
                        <div className="flex flex-1 flex-col px-6 py-6 sm:px-10 lg:px-14 lg:py-8">
                            <div className="mx-auto flex w-full max-w-md flex-col">
                                <p className="text-center text-sm font-bold uppercase tracking-wide text-primary">
                                    Step {currentStep}/4
                                </p>
                                <h2 className="mt-2 text-center text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                                    {title}
                                </h2>

                                <div className="mt-6 flex flex-col lg:mt-8">{children}</div>
                            </div>
                        </div>

                        <Separator />

                        <div className="flex items-center justify-between gap-4 px-6 md:py-3 py-2 sm:px-10 lg:px-12">
                            {onPrevious ? (
                                <Button
                                    type="button"
                                    variant="ghost"
                                    onClick={onPrevious}
                                    className="h-12 rounded-2xl px-0 text-base font-semibold text-primary hover:bg-transparent hover:text-primary/90"
                                >
                                    <ArrowLeft className="size-5" />
                                    Previous
                                </Button>
                            ) : (
                                <span />
                            )}

                            <Button
                                type="submit"
                                form={formId}
                                size="lg"
                                disabled={isSubmitting}
                                className="h-11 rounded-2xl px-6 text-base font-bold shadow-lg lg:h-12"
                            >
                                {nextLabel}
                                <ArrowRight className="size-5" />
                            </Button>
                        </div>
                    </div>
                </Card>
            </div>
        </AuthViewport>
    )
}