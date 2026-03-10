import { Plus } from "lucide-react";
import { Event } from "@/modules/dashboard/types/events";
import { EventCard } from "@/modules/dashboard/components/ui/event-card";
import { Button } from "@/components/ui/button";
import { DashboardPageHeader } from "@/modules/dashboard/components/ui/dashboard-page-header";

interface NearestEventsViewProps {
    events: Event[];
}

export function NearestEventsView({ events }: NearestEventsViewProps) {
    return (
        <div className="flex flex-col w-full h-full max-w-8xl mx-auto pt-6 px-4 pb-10">
            <div className="mb-10">
                <DashboardPageHeader
                    title="Nearest Events"
                    backHref="/dashboard"
                    backLabel="Back to Dashboard"
                    action={
                        <Button className="rounded-xl px-6 h-12 shadow-lg shadow-primary/30 hover:shadow-primary/50 hover:-translate-y-0.5">
                            <Plus className="w-5 h-5 stroke-2" />
                            Add Event
                        </Button>
                    }
                />
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-x-8 gap-y-6">
                {events.map((event) => (
                    <EventCard key={event.id} event={event} />
                ))}
            </div>
        </div>
    );
}
