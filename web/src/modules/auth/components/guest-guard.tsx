"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

import { useSessionQuery } from "@/modules/auth/api/auth"

type GuestGuardProps = {
    children: React.ReactNode
}

export function GuestGuard({ children }: GuestGuardProps) {
    const router = useRouter()
    const { data, isLoading } = useSessionQuery()

    useEffect(() => {
        if (isLoading) {
            return
        }

        if (data?.authenticated) {
            router.replace("/dashboard")
        }
    }, [data?.authenticated, isLoading, router])

    if (isLoading) {
        return null
    }

    if (data?.authenticated) {
        return null
    }

    return <>{children}</>
}
