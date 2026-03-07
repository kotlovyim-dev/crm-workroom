import { ArrowDown, ArrowUp, Building2, Clock, FileText, Gift, Tv, Users } from "lucide-react";
import { Event } from "@/modules/dashboard/types/events";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface EventCardProps {
    event: Event;
}

const TYPE_CONFIG = {
    presentation: {
        icon: Building2,
        lineClass: "bg-blue-500",
        iconClass: "text-blue-500",
    },
    birthday: {
        icon: Gift,
        lineClass: "bg-fuchsia-400",
        iconClass: "text-fuchsia-400",
    },
    meeting: {
        icon: Users,
        lineClass: "bg-amber-400",
        iconClass: "text-amber-400",
    },
    movie: {
        icon: Tv,
        lineClass: "bg-indigo-500",
        iconClass: "text-indigo-500",
    },
    other: {
        icon: FileText,
        lineClass: "bg-blue-500",
        iconClass: "text-blue-500",
    },
};

export function EventCard({ event }: EventCardProps) {
    const config = TYPE_CONFIG[event.type] || TYPE_CONFIG.other;
    const Icon = config.icon;

    return (
        <Card className="relative rounded-3xl p-7 shadow-sm w-full hover:shadow-md transition-shadow duration-300">
            <div
                className={`absolute left-0 top-1/2 -translate-y-1/2 w-1 h-3/5 ${config.lineClass} rounded-r-md`}
            />
            <div className="flex justify-between items-start pl-2">
                <div className="flex items-center gap-3">
                    <Icon className={`w-5 h-5 stroke-2 ${config.iconClass}`} />
                    <span className="text-foreground font-bold text-base">{event.title}</span>
                </div>
                {event.trend && (
                    <div className="flex-shrink-0 ml-4 pt-1">
                        {event.trend === "up" ? (
                            <ArrowUp className="w-5 h-5 text-amber-500 stroke-2" />
                        ) : (
                            <ArrowDown className="w-5 h-5 text-emerald-500 stroke-2" />
                        )}
                    </div>
                )}
            </div>

            <div className="flex justify-between items-center pl-2 pt-1">
                <div className="text-muted-foreground text-sm font-medium">
                    {event.dateLabel} | {event.time}
                </div>
                <Badge variant="secondary" className="px-3 py-1.5 rounded-xl font-semibold text-sm gap-1.5">
                    <Clock className="w-4 h-4 fill-muted-foreground stroke-secondary" />
                    {event.duration}
                </Badge>
            </div>
        </Card>
    );
}
