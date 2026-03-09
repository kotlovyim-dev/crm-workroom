import { Activity, ActivityStream } from "../ui/activity-stream";
import { NearestEvents } from "../ui/nearest-events";
import { ProjectsContainer } from "../ui/projects-container";
import { Workload } from "../ui/workload";

const activityStreamData: Activity[] = [
    {
        author: {
            name: "John Doe",
            position: "Software Engineer",
        },
        actions: [{
            type: "updated",
            description: "Updated the status of Mind Map task to In Progress",
        },
        {
            type: "attached",
            description: "Attached a file to the task",
        },
        ],
    },
    {
        author: {
            name: "Jane Smith",
            position: "Product Manager",
        },
        actions: [{
            type: "updated",
            description: "Updated the status of Mind Map task to In Progress",
        }],
    },
    {
        author: {
            name: "Jane Smith",
            position: "Product Manager",
        },
        actions: [{
            type: "updated",
            description: "Updated the status of Mind Map task to In Progress",
        }],
    },
    {
        author: {
            name: "Jane Smith",
            position: "Product Manager",
        },
        actions: [{
            type: "updated",
            description: "Updated the status of Mind Map task to In Progress",
        }],
    },
    {
        author: {
            name: "Jane Smith",
            position: "Product Manager",
        },
        actions: [{
            type: "updated",
            description: "Updated the status of Mind Map task to In Progress",
        }],
    },
    {
        author: {
            name: "Jane Smith",
            position: "Product Manager",
        },
        actions: [{
            type: "updated",
            description: "Updated the status of Mind Map task to In Progress",
        }],
    },
]

export function DashboardView() {
    return (
        <div className="flex flex-col gap-6 w-full">
            <div className="flex flex-col gap-2">
                <h4 className="text-base text-secondary-foreground">
                    Welcome back, John!
                </h4>
                <h1 className="text-4xl font-bold text-foreground">
                    Dashboard
                </h1>
            </div>
            <div className="flex flex-row gap-6 items-stretch">
                <div className="flex-1 min-w-0">
                    <Workload />
                </div>
                <div className="w-1/4 shrink-0">
                    <NearestEvents />
                </div>
            </div>
            <div className="flex flex-row gap-6 items-stretch">
                <div className="flex-1 min-w-0">
                    <ProjectsContainer />
                </div>
                <div className="w-1/4 relative shrink-0">
                    <div className="absolute inset-0 h-full">
                        <ActivityStream activities={activityStreamData} />
                    </div>
                </div>
            </div>
        </div>
    );
}
