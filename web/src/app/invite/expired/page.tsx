import Link from "next/link"

import { Button } from "@/components/ui/button"

export default function InviteExpiredPage() {
    return (
        <div className="mx-auto mt-20 max-w-lg rounded-xl border bg-card p-8 text-center">
            <h1 className="text-2xl font-bold">Invite expired</h1>
            <p className="mt-3 text-muted-foreground">
                This invitation is no longer valid. Ask your workspace admin to send a new invite.
            </p>
            <div className="mt-6 flex justify-center">
                <Button asChild>
                    <Link href="/login">Request new invite</Link>
                </Button>
            </div>
        </div>
    )
}
