import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { NearEventCard } from "./near-event-card";
import { ChevronRightIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

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
                <h2 className="text-xl font-bold">Nearest Events</h2>
                <Button variant="link" size="sm">
                    View All <ChevronRightIcon className="size-5" />
                </Button>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
                {events.map((event, index) => (
                    <div key={index} className="flex flex-col items-center">
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
