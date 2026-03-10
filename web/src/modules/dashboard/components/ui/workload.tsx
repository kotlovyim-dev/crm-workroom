import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ChevronRightIcon } from "lucide-react";
import { DashboardSectionHeader } from "./dashboard-section-header";
import { EmployeeCard } from "./employee-card";

const workloadData = [
    {
        name: "John Doe",
        position: "Software Engineer",
        level: "Senior",
    },
    {
        name: "Jane Smith",
        position: "Product Manager",
        level: "Middle",
    },
    {
        name: "Alice Johnson",
        position: "UX Designer",
        level: "Junior",
    },
    {
        name: "Bob Brown",
        position: "QA Engineer",
        level: "Middle",
    },
    {
        name: "Charlie Davis",
        position: "DevOps Engineer",
        level: "Senior",
    },
    {
        name: "Eve Wilson",
        position: "Data Scientist",
        level: "Middle",
    },
    {
        name: "Frank Miller",
        position: "Technical Writer",
        level: "Junior",
    },
    {
        name: "Grace Lee",
        position: "HR Specialist",
        level: "Middle",
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
                        />
                    </div>
                ))}
            </CardContent>
        </Card>
    );
}
