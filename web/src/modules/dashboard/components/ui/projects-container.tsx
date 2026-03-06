import { Button } from "@/components/ui/button";
import { ChevronRightIcon } from "lucide-react";
import { ProjectCard } from "./project-card";

const PROJECTS = [
    {
        id: "PN0001265",
        icon: "/logo.svg",
        name: "Medical App (IOS native)",
        createdAt: new Date(),
        priority: "Medium",
        all_tasks: 12,
        active_tasks: 8,
        assignees: [
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
        ]

    },
    {
        id: "PN0001266",
        icon: "/logo.svg",
        name: "Medical App (IOS native)",
        createdAt: new Date(),
        priority: "Medium",
        all_tasks: 12,
        active_tasks: 8,
        assignees: [
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
        ]

    },
    {
        id: "PN0001267",
        icon: "/logo.svg",
        name: "Medical App (IOS native)",
        createdAt: new Date(),
        priority: "Medium",
        all_tasks: 12,
        active_tasks: 8,
        assignees: [
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
        ]

    }
]

export function ProjectsContainer() {
    return (
        <div className="w-full flex flex-col gap-4">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold">Projects</h2>
                <Button variant="link" size="sm">
                    View All <ChevronRightIcon className="size-5" />
                </Button>
            </div>
            <div className="flex flex-col gap-4">
                {PROJECTS.slice(0, 3).map((project) => (
                    <ProjectCard
                        id={project.id}
                        icon={project.icon}
                        name={project.name}
                        createdAt={project.createdAt}
                        priority={project.priority}
                        all_tasks={project.all_tasks}
                        active_tasks={project.active_tasks}
                        assignees={project.assignees}
                        key={project.id}
                    />

                ))}
            </div>
        </div>
    );
}
