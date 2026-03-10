import type { ReactNode } from "react";

type DashboardSectionHeaderProps = {
    title: string;
    action?: ReactNode;
    className?: string;
    titleClassName?: string;
};

export function DashboardSectionHeader({
    title,
    action,
    className = "flex items-center justify-between",
    titleClassName = "text-2xl font-bold",
}: DashboardSectionHeaderProps) {
    return (
        <div className={className}>
            <h2 className={titleClassName}>{title}</h2>
            {action}
        </div>
    );
}