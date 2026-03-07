"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

import { useSessionQuery } from "@/modules/auth/api/auth"

type SessionGuardProps = {
    children: React.ReactNode
}

export function SessionGuard({ children }: SessionGuardProps) {
    const router = useRouter()
    const { data, isLoading, isError } = useSessionQuery()

    useEffect(() => {
        if (isLoading) {
            return
        }

        if (isError || !data?.authenticated) {
            router.replace("/login")
        }
    }, [data?.authenticated, isError, isLoading, router])

    if (isLoading) {
        return null
    }

    if (!data?.authenticated) {
        return null
    }

    return <>{children}</>
}