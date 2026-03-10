import Link from "next/link";
import type { ReactNode } from "react";
import { ArrowLeft } from "lucide-react";

type DashboardPageHeaderProps = {
    title: string;
    eyebrow?: string;
    action?: ReactNode;
    backHref?: string;
    backLabel?: string;
};

export function DashboardPageHeader({
    title,
    eyebrow,
    action,
    backHref,
    backLabel,
}: DashboardPageHeaderProps) {
    return (
        <div className="flex flex-col gap-3">
            {backHref && backLabel ? (
                <Link
                    href={backHref}
                    className="flex items-center gap-2 text-primary hover:text-primary/90 transition-colors text-sm font-semibold max-w-fit"
                >
                    <ArrowLeft className="w-4 h-4" />
                    {backLabel}
                </Link>
            ) : null}

            <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
                <div className="flex flex-col gap-2">
                    {eyebrow ? (
                        <h4 className="text-base text-secondary-foreground">{eyebrow}</h4>
                    ) : null}
                    <h1 className="text-4xl font-bold text-foreground">{title}</h1>
                </div>
                {action}
            </div>
        </div>
    );
}