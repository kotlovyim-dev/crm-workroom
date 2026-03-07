import Link from "next/link";
import { ArrowLeft, Plus } from "lucide-react";
import { Event } from "@/modules/dashboard/types/events";
import { EventCard } from "@/modules/dashboard/components/ui/event-card";
import { Button } from "@/components/ui/button";

interface NearestEventsViewProps {
    events: Event[];
}

export function NearestEventsView({ events }: NearestEventsViewProps) {
    return (
        <div className="flex flex-col w-full h-full max-w-8xl mx-auto pt-6 px-4 pb-10">
            <div className="flex flex-col mb-10 gap-3">
                <Link
                    href="/dashboard"
                    className="flex items-center gap-2 text-primary hover:text-primary/90 transition-colors text-sm font-semibold max-w-fit"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Back to Dashboard
                </Link>
                <div className="flex justify-between items-end">
                    <h1 className="text-3xl font-bold text-foreground leading-none">Nearest Events</h1>
                    <Button className="rounded-xl px-6 h-12 shadow-lg shadow-primary/30 hover:shadow-primary/50 hover:-translate-y-0.5">
                        <Plus className="w-5 h-5 stroke-2" />
                        Add Event
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-x-8 gap-y-6">
                {events.map(event => (
                    <EventCard key={event.id} event={event} />
                ))}
            </div>
        </div>
    );
}
