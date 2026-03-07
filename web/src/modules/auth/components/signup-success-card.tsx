"use client"

import Image from "next/image"
import { useRouter } from "next/navigation"
import { ArrowRight } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { useOnboardingStore } from "@/modules/auth/store/onboarding-store"

export function SignupSuccessCard() {
    const router = useRouter()
    const reset = useOnboardingStore((state) => state.reset)

    const handleStart = () => {
        reset()
        router.push("/dashboard")
    }

    return (
        <div className="h-screen overflow-hidden bg-secondary px-4 py-4 lg:px-5 lg:py-5">
            <Card className="mx-auto h-full w-full max-w-7xl rounded-3xl border-border/60 py-0 shadow-xl">
                <div className="flex h-full flex-col items-center px-6 py-8 text-center sm:px-10 lg:px-12 lg:py-10">
                    <div className="flex flex-1 flex-col items-center justify-center">
                        <div className="relative mb-8 aspect-5/4 w-full max-w-md lg:mb-10 lg:max-w-xl">
                        <Image
                            src="/auth-Illustration.svg"
                            alt="Registration complete illustration"
                            fill
                            priority
                            className="object-contain"
                        />
                        </div>

                        <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                            You are successfully registered!
                        </h1>
                    </div>

                    <Button onClick={handleStart} size="lg" className="mt-6 h-11 rounded-2xl px-6 text-base font-bold shadow-lg lg:h-12">
                        Let&apos;s Start
                        <ArrowRight className="size-5" />
                    </Button>
                </div>
            </Card>
        </div>
    )
}