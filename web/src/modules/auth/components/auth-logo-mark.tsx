import Image from "next/image";

type AuthLogoMarkProps = {
    size?: number;
    className?: string;
    imageClassName?: string;
    priority?: boolean;
};

export function AuthLogoMark({
    size = 48,
    className = "flex size-14 items-center justify-center rounded-xl bg-card p-0 text-card-foreground",
    imageClassName,
    priority = false,
}: AuthLogoMarkProps) {
    return (
        <div className={className}>
            <Image
                src="/logo.svg"
                alt="Woorkroom logo"
                width={size}
                height={size}
                priority={priority}
                className={imageClassName}
            />
        </div>
    );
}