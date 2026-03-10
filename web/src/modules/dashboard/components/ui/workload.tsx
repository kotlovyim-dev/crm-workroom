import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ChevronRightIcon } from "lucide-react";
import { DashboardSectionHeader } from "./dashboard-section-header";
import { EmployeeCard } from "./employee-card";

const workloadData = [
    {
        name: "Shawn Stone",
        position: "UI/UX Designer",
        level: "Middle",
        activeTasks: 18,
        totalTasks: 24,
    },
    {
        name: "Randy Delgado",
        position: "UI/UX Designer",
        level: "Junior",
        activeTasks: 10,
        totalTasks: 35,
    },
    {
        name: "Emily Tyler",
        position: "Copywriter",
        level: "Middle",
        activeTasks: 20,
        totalTasks: 20,
    },
    {
        name: "Louis Castor",
        position: "Copywriter",
        level: "Senior",
        activeTasks: 32,
        totalTasks: 32,
    },
    {
        name: "Blake Silva",
        position: "iOS Developer",
        level: "Senior",
        activeTasks: 12,
        totalTasks: 30,
    },
    {
        name: "Joel Phillips",
        position: "UI/UX Designer",
        level: "Middle",
        activeTasks: 35,
        totalTasks: 40,
    },
    {
        name: "Wayne Marsh",
        position: "Copywriter",
        level: "Junior",
        activeTasks: 5,
        totalTasks: 20,
    },
    {
        name: "Oscar Holloway",
        position: "UI/UX Designer",
        level: "Middle",
        activeTasks: 25,
        totalTasks: 28,
    },
];

export function Workload() {
    return (
        <Card className="w-full pt-6 gap-4 border-none shadow-sm pb-6">
            <CardHeader className="flex items-center justify-between py-2">
                <DashboardSectionHeader
                    title="Workload"
                    action={
                        <Button variant="link" size="sm" className="text-primary hover:text-primary/80 font-semibold text-base py-0">
                            View all <ChevronRightIcon className="w-5 h-5 ml-1" />
                        </Button>
                    }
                />
            </CardHeader>
            <CardContent className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-2">
                {workloadData.map((employee) => (
                    <div key={`${employee.name}-${employee.position}`} className="flex flex-col items-center bg-muted/50 rounded-2xl p-4">
                        <EmployeeCard
                            name={employee.name}
                            position={employee.position}
                            level={employee.level}
                            activeTasks={employee.activeTasks}
                            totalTasks={employee.totalTasks}
                        />
                    </div>
                ))}
            </CardContent>
        </Card>
    );
}
