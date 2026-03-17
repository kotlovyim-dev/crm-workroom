import Link from "next/link"

import { Button } from "@/components/ui/button"

export default function AccessDeniedPage() {
    return (
        <div className="mx-auto mt-16 max-w-xl rounded-xl border bg-card p-8 text-center">
            <h1 className="text-2xl font-bold">Access denied</h1>
            <p className="mt-3 text-muted-foreground">
                You do not have permission to perform this action in this workspace.
            </p>
            <div className="mt-6">
                <Button asChild>
                    <Link href="/dashboard">Back to dashboard</Link>
                </Button>
            </div>
        </div>
    )
}
