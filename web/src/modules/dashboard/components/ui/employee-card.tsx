import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

interface EmployeeCardProps {
    name: string;
    position: string;
    level: string;
}

export function EmployeeCard({ name, position, level }: EmployeeCardProps) {
    return (
        <Card className="w-full bg-background border-none shadow-none">
            <CardHeader className="flex items-center justify-center">
                <Avatar className="w-14 h-14">
                    <AvatarFallback>{name.substring(0, 2)}</AvatarFallback>
                </Avatar>
            </CardHeader>
            <CardContent className="flex flex-col gap-2 items-center">
                <div className="flex flex-col items-center">
                    <h3 className="text-lg font-semibold text-foreground">
                        {name}
                    </h3>
                    <p className="text-sm text-secondary-foreground">
                        {position}
                    </p>
                </div>

                <Badge
                    variant="outline"
                    className="rounded-md text-muted-foreground border-muted-foreground"
                >
                    {level}
                </Badge>
            </CardContent>
        </Card>
    );
}
