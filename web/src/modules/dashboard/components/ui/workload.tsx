import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ChevronRightIcon } from "lucide-react";
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
        <Card className="w-full pt-6 gap-4">
            <CardHeader className="flex items-center justify-between">
                <h2 className="text-2xl font-bold">Workload</h2>
                <Button variant="link" size="sm">
                    View All <ChevronRightIcon className="size-5" />
                </Button>
            </CardHeader>
            <CardContent className="grid grid-cols-4 gap-4">
                {workloadData.map((employee, index) => (
                    <div key={index} className="flex flex-col items-center">
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
