import { Download, File, FileArchive, FileImage, FileText } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import type { AttachmentMetadata } from "@/lib/api/contracts"
import { cn } from "@/lib/utils"

export type AttachmentListProps = {
    attachments: AttachmentMetadata[]
    className?: string
    emptyMessage?: string
    showObjectKey?: boolean
}

function formatFileSize(sizeBytes: number) {
    if (sizeBytes < 1024) {
        return `${sizeBytes} B`
    }

    const units = ["KB", "MB", "GB", "TB"]
    let value = sizeBytes / 1024
    let unitIndex = 0

    while (value >= 1024 && unitIndex < units.length - 1) {
        value /= 1024
        unitIndex += 1
    }

    const maximumFractionDigits = value >= 100 ? 0 : 1
    return `${value.toFixed(maximumFractionDigits)} ${units[unitIndex]}`
}

function formatUploadedAt(uploadedAt?: string | null) {
    if (!uploadedAt) {
        return null
    }

    const parsedDate = new Date(uploadedAt)
    if (Number.isNaN(parsedDate.getTime())) {
        return null
    }

    return new Intl.DateTimeFormat("en", {
        month: "short",
        day: "numeric",
        year: "numeric",
    }).format(parsedDate)
}

function AttachmentIcon({ contentType }: { contentType: string }) {
    if (contentType.startsWith("image/")) {
        return <FileImage className="size-4 text-primary" />
    }

    if (contentType.includes("pdf") || contentType.startsWith("text/")) {
        return <FileText className="size-4 text-primary" />
    }

    if (contentType.includes("zip") || contentType.includes("tar") || contentType.includes("compressed")) {
        return <FileArchive className="size-4 text-primary" />
    }

    return <File className="size-4 text-primary" />
}

export function AttachmentList({
    attachments,
    className,
    emptyMessage = "No attachments yet.",
    showObjectKey = false,
}: AttachmentListProps) {
    if (attachments.length === 0) {
        return (
            <Card className={className}>
                <CardContent className="py-6 text-sm text-muted-foreground">{emptyMessage}</CardContent>
            </Card>
        )
    }

    return (
        <Card className={className}>
            <CardContent className="px-0 py-0">
                <ul className="divide-y divide-border/60">
                    {attachments.map((attachment) => {
                        const uploadedAt = formatUploadedAt(attachment.uploaded_at)

                        return (
                            <li
                                key={attachment.id}
                                className="flex items-start justify-between gap-4 px-6 py-4"
                            >
                                <div className="flex min-w-0 items-start gap-3">
                                    <div className="mt-0.5 rounded-full bg-primary/10 p-2">
                                        <AttachmentIcon contentType={attachment.content_type} />
                                    </div>
                                    <div className="min-w-0 space-y-1">
                                        <div className="truncate text-sm font-semibold text-foreground">
                                            {attachment.file_name}
                                        </div>
                                        <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                                            <Badge variant="outline">{formatFileSize(attachment.size_bytes)}</Badge>
                                            <span>{attachment.content_type}</span>
                                            {uploadedAt ? <span>Uploaded {uploadedAt}</span> : null}
                                        </div>
                                        {showObjectKey ? (
                                            <div className="truncate text-xs text-muted-foreground">
                                                {attachment.object_key}
                                            </div>
                                        ) : null}
                                    </div>
                                </div>
                                <div className="shrink-0">
                                    {attachment.download_url ? (
                                        <Button asChild size="sm" variant="outline">
                                            <a href={attachment.download_url} rel="noreferrer" target="_blank">
                                                <Download className="size-4" />
                                                Download
                                            </a>
                                        </Button>
                                    ) : (
                                        <div className={cn("text-xs text-muted-foreground")}>Unavailable</div>
                                    )}
                                </div>
                            </li>
                        )
                    })}
                </ul>
            </CardContent>
        </Card>
    )
}