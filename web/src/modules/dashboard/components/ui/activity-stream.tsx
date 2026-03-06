import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
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
    "deleted": "text-red-500",
}

export function ActivityStream({ activities }: ActivityStreamProps) {
    return (
        <Card className="w-1/3 gap-0 pb-0" >
            <CardHeader className="py-0">
                <h2 className="text-2xl font-bold">Activity Stream</h2>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
                {activities.map((activity, index) => (
                    <div key={index} className="flex flex-col gap-3">
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
                            {activity.actions.map((action, index) => {
                                const Icon = actionIconIconMap[action.type];
                                return <div key={index} className="flex flex-row gap-2 p-4 bg-background rounded-lg">
                                    <Icon className={cn(actionColorMap[action.type], "size-6 shrink-0")} />
                                    <span>{action.description}</span>
                                </div>
                            })}
                        </div>

                    </div>
                ))}
                <Button variant="link" size="sm">
                    View All <ChevronRightIcon className="size-5" />
                </Button>
            </CardContent>
        </Card>
    );
}