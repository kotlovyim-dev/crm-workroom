import { Event } from "@/modules/dashboard/types/events";
import { NearestEventsView } from "@/modules/dashboard/components/views/nearest-events-view";

export const metadata = {
    title: "Nearest Events | CRM Dashboard",
    description: "Nearest Events page for tracking all upcoming tasks and meetings.",
};

const MOCK_EVENTS: Event[] = [
    {
        id: "1",
        title: "Presentation of the new department",
        dateLabel: "Today",
        time: "6:00 PM",
        duration: "4h",
        type: "presentation",
        trend: "up"
    },
    {
        id: "2",
        title: "Anna's Birthday",
        dateLabel: "Today",
        time: "5:00 PM",
        duration: "2h",
        type: "birthday",
        trend: "down"
    },
    {
        id: "3",
        title: "Meeting with Development Team",
        dateLabel: "Tomorrow",
        time: "5:00 PM",
        duration: "4h",
        type: "meeting",
        trend: "up"
    },
    {
        id: "4",
        title: "Ray's Birthday",
        dateLabel: "Tomorrow",
        time: "2:00 PM",
        duration: "1h 30m",
        type: "birthday",
        trend: "down"
    },
    {
        id: "5",
        title: "Meeting with CEO",
        dateLabel: "Sep 14",
        time: "5:00 PM",
        duration: "1h",
        type: "other",
        trend: "up"
    },
    {
        id: "6",
        title: "Movie night (Tenet)",
        dateLabel: "Sep 15",
        time: "5:00 PM",
        duration: "3h",
        type: "movie",
        trend: "down"
    },
    {
        id: "7",
        title: "Lucas's Birthday",
        dateLabel: "Sep 29",
        time: "5:30 PM",
        duration: "2h",
        type: "birthday",
        trend: "down"
    },
    {
        id: "8",
        title: "Meeting with CTO",
        dateLabel: "Sep 30",
        time: "12:00",
        duration: "1h",
        type: "presentation",
        trend: "up"
    }
];

export default function NearestEventsPage() {
    return <NearestEventsView events={MOCK_EVENTS} />;
}
