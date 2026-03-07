export type EventType = "presentation" | "birthday" | "meeting" | "movie" | "other";

export type EventTrend = "up" | "down";

export interface Event {
    id: string;
    title: string;
    dateLabel: string;
    time: string;
    duration: string;
    type: EventType;
    trend?: EventTrend;
}
