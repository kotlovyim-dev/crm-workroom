import type { ReactNode } from "react";

type AuthViewportProps = {
    children: ReactNode;
    className?: string;
};

export function AuthViewport({ children, className = "px-4 py-4 lg:px-5 lg:py-5" }: AuthViewportProps) {
    return (
        <div className={`h-screen overflow-hidden bg-secondary ${className}`}>
            {children}
        </div>
    );
}