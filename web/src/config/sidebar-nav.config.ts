import {
    CalendarIcon,
    FolderOpenIcon,
    LayersIcon,
    LayoutGridIcon,
    LucideIcon,
    MessageCircleIcon,
    PlaneIcon,
    UsersIcon,
} from "lucide-react";
import type { CanonicalRole } from "@/modules/auth/types/auth";

interface NavItem {
    label: string;
    href: string;
    icon?: LucideIcon;
    requiredRoles?: CanonicalRole[];
}

export const NAV_ITEMS: NavItem[] = [
    {
        label: "Dashboard",
        href: "/dashboard",
        icon: LayoutGridIcon,
    },
    {
        label: "Projects",
        href: "/projects",
        icon: LayersIcon,
    },
    {
        label: "Calendar",
        href: "/calendar",
        icon: CalendarIcon,
    },
    {
        label: "Vacations",
        href: "/vacations",
        icon: PlaneIcon,
    },
    {
        label: "Employees",
        href: "/employees",
        icon: UsersIcon,
        requiredRoles: ["Admin/Owner", "PM/Team Lead"],
    },
    {
        label: "Messanger",
        href: "/messanger",
        icon: MessageCircleIcon,
    },
    {
        label: "Info Portal",
        href: "/info-portal",
        icon: FolderOpenIcon,
    },
];
