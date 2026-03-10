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
    "High": "text-destructive",
    "Medium": "text-amber-500",
    "Low": "text-emerald-500",
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
        <div className="flex flex-col md:flex-row w-full bg-card rounded-2xl shadow-sm border overflow-hidden">
            <div className="md:w-1/2 p-6 flex flex-col justify-between min-h-36">
                <div className="flex flex-row gap-4">
                    <Image src={icon} alt={name} width={48} height={48} className="rounded-xl object-contain" />
                    <div className="flex flex-col justify-center">
                        <h3 className="text-sm text-muted-foreground">{id}</h3>
                        <p className="font-bold text-lg text-foreground">{name}</p>
                    </div>
                </div>
                <div className="flex flex-row items-center justify-between mt-4">
                    <div className="flex items-center text-sm text-muted-foreground gap-2 font-medium">
                        Created {formatDate(createdAt)}
                    </div>
                    <div className={`flex items-center font-bold text-sm gap-1 capitalize ${priorityMap[priority] || "text-foreground"}`}>
                        <ArrowDownIcon className="w-4 h-4" /> {priority}
                    </div>
                </div>
            </div>

            <div className="hidden md:block w-px bg-border my-6" />

            <div className="md:w-1/2 p-6 flex flex-col justify-between min-h-36 bg-transparent">
                <h3 className="text-lg font-bold text-foreground">Project Data</h3>

                <div className="grid grid-cols-3 gap-4 pt-4">
                    <div className="flex flex-col gap-1">
                        <p className="text-sm text-muted-foreground">All tasks</p>
                        <p className="font-bold text-lg text-foreground">{all_tasks}</p>
                    </div>
                    <div className="flex flex-col gap-1">
                        <p className="text-sm text-muted-foreground">Active tasks</p>
                        <p className="font-bold text-lg text-foreground">{active_tasks}</p>
                    </div>
                    <div className="flex flex-col gap-1">
                        <p className="text-sm text-muted-foreground">Assignees</p>
                        <div className="flex -space-x-2 mt-1">
                            {assignees.slice(0, 3).map((assignee, index) => (
                                <Avatar key={index} className="w-8 h-8 border-2 border-background">
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
            </div>
        </div>
    );
}