import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ArrowDownIcon } from "lucide-react";
import Image from "next/image";

interface ProjectCardProps {
    id: string;
    icon: string;
    name: string;
    createdAt: Date;
    priority: string;
    all_tasks: number;
    active_tasks: number;
    assignees: {
        name: string;
        position: string;
        level: string;
    }[];
}

const priorityMap: Record<string, string> = {
    "High": "text-red-500",
    "Medium": "text-yellow-500",
    "Low": "text-green-500",
}

function formatDate(date: Date) {
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
    });
}

export function ProjectCard({ id, icon, name, createdAt, priority, all_tasks, active_tasks, assignees }: ProjectCardProps) {
    return (
        <div className="flex flex-row w-full">
            <Card className="w-1/2 rounded-r-none shadow-r-none p-6 flex flex-col">
                <div className="flex flex-row gap-4">
                    <Image src={icon} alt={name} width={48} height={48} />
                    <div className="flex flex-col">
                        <h3 className="text-sm text-muted-foreground">{id}</h3>
                        <p className="font-bold text-lg">{name}</p>
                    </div>
                </div>
                <div className="flex flex-row items-center justify-between">
                    <div className="flex items-center font-semibold text-sm text-muted-foreground gap-2"><CalendarIcon /> Created {formatDate(createdAt)}</div>
                    <div className={`flex items-center font-bold text-sm text-muted-foreground gap-2 capitalize ${priorityMap[priority]}`}><ArrowDownIcon /> {priority}</div>
                </div>
            </Card>
            <Card className="w-1/2 rounded-l-none shadow-l-none p-6 flex flex-col">

                <h3 className="text-lg font-bold">Project Data</h3>

                <div className="grid grid-cols-3 gap-4">
                    <div>
                        <p className="text-sm text-muted-foreground">All Tasks</p>
                        <p className="font-bold text-lg">{all_tasks}</p>
                    </div>
                    <div>
                        <p className="text-sm text-muted-foreground">Active Tasks</p>
                        <p className="font-bold text-lg">{active_tasks}</p>
                    </div>
                    <div>
                        <p className="text-sm text-muted-foreground">Assignees</p>
                        <div className="flex -space-x-2 mt-1">
                            {assignees.slice(0, 3).map((assignee) => (
                                <Avatar key={`${assignee.name}-${assignee.position}`} className="w-8 h-8 border-2 border-background">
                                    <AvatarFallback className="bg-secondary text-secondary-foreground text-xs font-semibold">
                                        {assignee.name.substring(0, 2)}
                                    </AvatarFallback>
                                </Avatar>
                            ))}
                            {assignees.length > 3 && (
                                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-xs font-bold border-2 border-background z-10 relative">
                                    +{assignees.length - 3}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </Card >
        </div >
    );
}