import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { NearEventCard } from "./near-event-card";
import { ChevronRightIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { DashboardSectionHeader } from "./dashboard-section-header";

const events = [
    {
        name: "Team Meeting",
        time: "Today | 10:00 AM",
        duration: "1h",
        type: "meeting" as const,
    },
    {
        name: "Client Call",
        time: "Today | 11:30 AM",
        duration: "1h",
        type: "meeting" as const,
    },
    {
        name: "Project Review",
        time: "Today | 2:00 PM",
        duration: "4h",
        type: "presentation" as const,
    },
];

export function NearestEvents() {
    return (
        <Card className="w-1/3">
            <CardHeader className="flex items-center justify-between">
                <DashboardSectionHeader
                    title="Nearest Events"
                    titleClassName="text-xl font-bold"
                    action={
                        <Link href="/dashboard/nearest-events">
                            <Button variant="link" size="sm">
                                View All <ChevronRightIcon className="size-5" />
                            </Button>
                        </Link>
                    }
                />
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
                {events.slice(0, 4).map((event) => (
                    <div key={`${event.name}-${event.time}`} className="flex flex-col items-center">
                        <NearEventCard
                            title={event.name}
                            time={event.time}
                            duration={event.duration}
                            type={event.type}
                        />
                    </div>
                ))}
            </CardContent>
        </Card>
    );
}
