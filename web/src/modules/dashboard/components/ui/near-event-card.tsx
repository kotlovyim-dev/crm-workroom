import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { ClockIcon } from "lucide-react";

type eventTypes =
    | "birthday"
    | "meeting"
    | "presentation"
    | "movie"
    | "building";

const colorMap: Record<string, string> = {
    birthday: "border-pink-500",
    meeting: "border-blue-500",
    presentation: "border-green-500",
    movie: "border-purple-500",
    building: "border-yellow-500",
};

interface NearEventCardProps {
    title: string;
    time: string;
    duration: string;
    type: eventTypes;
}

export function NearEventCard({
    title,
    time,
    duration,
    type,
}: NearEventCardProps) {
    return (
        <div
            className={cn(
                "border-l-4 px-4 w-full flex flex-col justify-between gap-10 py-3",
                colorMap[type],
            )}
        >
            <div className="flex flex-row items-center justify-between">
                <h3 className="text-lg font-semibold text-foreground">
                    {title}
                </h3>
            </div>
            <div className="flex flex-row items-center justify-between">
                <p className="text-sm text-muted-foreground">{time}</p>
                <Badge
                    variant="secondary"
                    className="rounded-md p-2 text-muted-foreground [&>svg]:size-5"
                >
                    <ClockIcon className="size-5" />
                    {duration}
                </Badge>
            </div>
        </div>
    );
}
