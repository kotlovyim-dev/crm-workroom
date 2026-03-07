"use client"

import { useEffect, useState } from "react"

function formatTime(timeLeft: number) {
    const minutes = Math.floor(timeLeft / 60_000)
    const seconds = Math.floor((timeLeft % 60_000) / 1_000)

    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`
}

export function useVerificationCountdown(expiresAt: number | null) {
    const [timeLeft, setTimeLeft] = useState(() => {
        if (!expiresAt) {
            return 0
        }

        return Math.max(0, expiresAt - Date.now())
    })

    useEffect(() => {
        if (!expiresAt) {
            return
        }

        const updateTimeLeft = () => {
            setTimeLeft(Math.max(0, expiresAt - Date.now()))
        }

        updateTimeLeft()

        const timer = window.setInterval(updateTimeLeft, 1_000)

        return () => window.clearInterval(timer)
    }, [expiresAt])

    const resolvedTimeLeft = expiresAt ? timeLeft : 0

    return {
        formattedTimeLeft: formatTime(resolvedTimeLeft),
        hasActiveCode: resolvedTimeLeft > 0,
    }
}