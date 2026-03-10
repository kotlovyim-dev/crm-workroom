import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { DashboardSectionHeader } from "@/modules/dashboard/components/ui/dashboard-section-header";
import { cn } from "@/lib/utils";
import { ChevronRightIcon, CloudUpload, LucideIcon, PaperclipIcon, TrashIcon } from "lucide-react";

type ActionType = "attached" | "updated" | "deleted";

type AuthorType = {
    name: string;
    position: string;
}

type Action = {
    type: ActionType;
    description: string;
}
export type Activity = {
    author: AuthorType;
    actions: Action[];
}

interface ActivityStreamProps {
    activities: Activity[];
}

const actionIconIconMap: Record<ActionType, LucideIcon> = {
    "attached": PaperclipIcon,
    "updated": CloudUpload,
    "deleted": TrashIcon,
}

const actionColorMap: Record<ActionType, string> = {
    "attached": "text-purple-500",
    "updated": "text-primary",
    "deleted": "text-destructive",
}

export function ActivityStream({ activities }: ActivityStreamProps) {
    const visibleActivities = activities.slice(0, 3);

    return (
        <Card className="flex flex-col w-full h-full gap-0 pb-4" >
            <CardHeader className="py-0 shrink-0">
                <DashboardSectionHeader title="Activity Stream" />
            </CardHeader>
            <CardContent className="flex flex-col gap-3 mt-4 flex-1 overflow-y-auto pr-2">
                {visibleActivities.map((activity) => (
                    <div key={`${activity.author.name}-${activity.author.position}`} className="flex flex-col gap-3">
                        <div className="flex flex-row items-center gap-2">
                            <Avatar className="size-12">
                                <AvatarFallback>{activity.author.name.charAt(0)}</AvatarFallback>
                            </Avatar>
                            <div>
                                <p className="font-medium">{activity.author.name}</p>
                                <p className="text-sm text-muted-foreground">{activity.author.position}</p>
                            </div>
                        </div>
                        <div className="flex flex-col gap-3">
                            {activity.actions.map((action) => {
                                const Icon = actionIconIconMap[action.type];
                                return <div key={`${action.type}-${action.description}`} className="flex flex-row gap-2 p-4 bg-background rounded-lg">
                                    <Icon className={cn(actionColorMap[action.type], "size-6 shrink-0")} />
                                    <span>{action.description}</span>
                                </div>;
                            })}
                        </div>

                    </div>
                ))}
            </CardContent>
            <div className="shrink-0 flex justify-center pt-2">
                <Button variant="link" size="sm">
                    View All <ChevronRightIcon className="size-5" />
                </Button>
            </div>
        </Card>
    );
}