"use client";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { CircularProgressbarWithChildren } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

interface EmployeeCardProps {
    name: string;
    position: string;
    level: string;
    activeTasks: number;
    totalTasks: number;
}

export function EmployeeCard({ name, position, level, activeTasks, totalTasks }: EmployeeCardProps) {
    const percentage = totalTasks > 0 ? (activeTasks / totalTasks) * 100 : 0;

    return (
        <Card className="w-full bg-transparent border-none shadow-none">
            <CardHeader className="flex items-center justify-center pb-4">
                <div className="w-24 h-24 [&_.CircularProgressbar-path]:stroke-primary [&_.CircularProgressbar-trail]:stroke-secondary">
                    <CircularProgressbarWithChildren
                        value={percentage}
                        strokeWidth={6}
                    >
                        <Avatar className="w-20 h-20">
                            <AvatarFallback className="text-xl">{name.substring(0, 2)}</AvatarFallback>
                        </Avatar>
                    </CircularProgressbarWithChildren>
                </div>
            </CardHeader>
            <CardContent className="flex flex-col gap-2 items-center">
                <div className="flex flex-col items-center">
                    <h3 className="text-lg font-semibold text-foreground text-center">
                        {name}
                    </h3>
                    <p className="text-sm text-muted-foreground whitespace-nowrap">
                        {position}
                    </p>
                </div>

                <Badge
                    variant="outline"
                    className="rounded-md text-muted-foreground border-muted-foreground mt-1"
                >
                    {level}
                </Badge>
            </CardContent>
        </Card>
    );
}
