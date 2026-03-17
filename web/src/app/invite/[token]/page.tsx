"use client"

import { useState } from "react"
import { useParams, useRouter } from "next/navigation"

import { acceptInvitation } from "@/modules/auth/api/auth"
import { getApiErrorMessage } from "@/modules/auth/api/client"
import { Button } from "@/components/ui/button"

export default function InviteAcceptPage() {
    const params = useParams<{ token: string }>()
    const router = useRouter()

    const token = params?.token ?? ""
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [needsTransferConfirmation, setNeedsTransferConfirmation] = useState(false)

    async function submit(transfer_confirmed: boolean) {
        if (!token) {
            return
        }

        setIsLoading(true)
        setError(null)

        try {
            await acceptInvitation({ token, transfer_confirmed })
            router.replace("/dashboard")
            return
        } catch (caught) {
            const message = getApiErrorMessage(caught, "Could not accept invitation.")

            if (message.toLowerCase().includes("transfer confirmation required")) {
                setNeedsTransferConfirmation(true)
                setError("This account belongs to another workspace. Confirm transfer to continue.")
            } else if (message.toLowerCase().includes("expired")) {
                router.replace("/invite/expired")
                return
            } else {
                setError(message)
            }
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="mx-auto mt-20 max-w-xl rounded-xl border bg-card p-8">
            <h1 className="text-2xl font-bold">Join workspace</h1>
            <p className="mt-3 text-muted-foreground">
                Accept this invitation to join the workspace. You may be asked to confirm transfer if your account
                already belongs to another workspace.
            </p>

            {error ? <p className="mt-4 text-sm text-destructive">{error}</p> : null}

            <div className="mt-6 flex gap-3">
                <Button disabled={isLoading} onClick={() => submit(false)}>
                    {isLoading ? "Checking..." : "Accept invite"}
                </Button>
                {needsTransferConfirmation ? (
                    <Button variant="secondary" disabled={isLoading} onClick={() => submit(true)}>
                        Confirm transfer
                    </Button>
                ) : null}
            </div>
        </div>
    )
}
