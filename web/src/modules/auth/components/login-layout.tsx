import { GuestGuard } from "@/modules/auth/components/guest-guard"
import { AuthLogoMark } from "@/modules/auth/components/auth-logo-mark"
import { AuthViewport } from "@/modules/auth/components/auth-viewport"
import Image from "next/image"

export const LoginLayout = ({ children }: { children: React.ReactNode }) => {
    return (
        <GuestGuard>
            <AuthViewport className="relative flex items-center justify-center p-4 lg:p-8">
                <div className="flex w-full max-w-7xl h-auto min-h-[770px] bg-card rounded-3xl shadow-xl overflow-hidden flex-col md:flex-row">

                    <div className="hidden md:flex flex-col flex-1 max-w-2xl bg-primary p-10 lg:p-16 relative overflow-hidden">

                        <div className="flex items-center gap-3 mb-16 z-10">
                            <AuthLogoMark
                                size={32}
                                className="flex bg-card rounded-xl p-2 w-12 h-12 justify-center items-center"
                            />
                            <span className="text-primary-foreground text-3xl font-bold tracking-tight">Woorkroom</span>
                        </div>

                        <div className="z-10 mt-4">
                            <h1 className="text-primary-foreground text-4xl leading-snug font-bold">
                                Your place to work<br />
                                <span className="opacity-90">Plan. Create. Control.</span>
                            </h1>
                        </div>

                        <div className="mt-10 flex flex-1 items-center justify-center w-full h-full pb-4 opacity-95 pointer-events-none">
                            <div className="relative w-full max-w-lg h-96">
                                <Image
                                    src="/auth-Illustration.svg"
                                    alt="Auth Illustration"
                                    fill
                                    className="object-contain"
                                    priority
                                />
                            </div>
                        </div>

                    </div>

                    <div className="flex-1 flex flex-col justify-center items-center p-8 md:p-16 lg:p-24 relative overflow-y-auto">
                        <div className="w-full max-w-md mx-auto">
                            {children}
                        </div>
                    </div>

                </div>
            </AuthViewport>
        </GuestGuard>
    )
}
