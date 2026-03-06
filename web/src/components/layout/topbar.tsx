"use client";

import {
    BellIcon,
    ChevronDownIcon,
    LogOutIcon,
    SearchIcon,
    SettingsIcon,
    UserIcon,
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";

const NOTIFICATIONS = [
    {
        id: 1,
        title: "New comment in project",
        description: "Ivan Petrenko left a comment on task #42",
        time: "5 min ago",
        read: false,
    },
    {
        id: 2,
        title: "Task assigned to you",
        description: 'Task "Update documentation" has been assigned to you',
        time: "1 hr ago",
        read: false,
    },
    {
        id: 3,
        title: "Meeting in 30 minutes",
        description: "Weekly team standup at 3:00 PM",
        time: "2 hr ago",
        read: true,
    },
];

export function Topbar() {
    const unreadCount = NOTIFICATIONS.filter((n) => !n.read).length;

    return (
        <header className="flex items-center justify-between gap-4 w-full px-1 pt-6">
            <div className="relative max-w-sm w-full">
                <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground pointer-events-none" />
                <Input
                    placeholder="Search..."
                    className="pl-9 bg-card border shadow-xs"
                />
            </div>

            <div className="flex items-center gap-2">
                <Popover>
                    <PopoverTrigger asChild>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="relative bg-card border shadow-xs"
                        >
                            <BellIcon className="size-5" />
                            {unreadCount > 0 && (
                                <span className="absolute top-1.5 right-1.5 size-2 rounded-full bg-destructive" />
                            )}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent align="end" className="w-80 p-0">
                        <div className="flex items-center justify-between px-4 py-3 border-b">
                            <span className="font-semibold text-sm">
                                Notifications
                            </span>
                            {unreadCount > 0 && (
                                <span className="text-xs text-muted-foreground">
                                    {unreadCount} unread
                                </span>
                            )}
                        </div>
                        <ul className="flex flex-col">
                            {NOTIFICATIONS.map((notification) => (
                                <li
                                    key={notification.id}
                                    className={`flex flex-col gap-1 px-4 py-3 border-b last:border-b-0 cursor-pointer hover:bg-muted/50 transition-colors ${
                                        !notification.read ? "bg-primary/5" : ""
                                    }`}
                                >
                                    <div className="flex items-center justify-between gap-2">
                                        <span className="text-sm font-medium leading-tight">
                                            {notification.title}
                                        </span>
                                        {!notification.read && (
                                            <span className="size-2 shrink-0 rounded-full bg-primary" />
                                        )}
                                    </div>
                                    <span className="text-xs text-muted-foreground">
                                        {notification.description}
                                    </span>
                                    <span className="text-xs text-muted-foreground/70">
                                        {notification.time}
                                    </span>
                                </li>
                            ))}
                        </ul>
                        <div className="px-4 py-2 border-t">
                            <Button
                                variant="ghost"
                                size="sm"
                                className="w-full text-xs text-muted-foreground"
                            >
                                View all
                            </Button>
                        </div>
                    </PopoverContent>
                </Popover>

                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button
                            variant="ghost"
                            className="flex items-center gap-2 px-3 bg-card border shadow-xs"
                        >
                            <Avatar size="sm">
                                <AvatarImage
                                    src="/avatar.png"
                                    alt="User avatar"
                                />
                                <AvatarFallback>IP</AvatarFallback>
                            </Avatar>
                            <span className="text-sm font-medium">
                                Ivan Petrenko
                            </span>
                            <ChevronDownIcon className="size-4 text-muted-foreground" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-52">
                        <DropdownMenuLabel>My account</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>
                            <UserIcon className="size-4" />
                            Profile
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                            <SettingsIcon className="size-4" />
                            Settings
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem variant="destructive">
                            <LogOutIcon className="size-4" />
                            Sign out
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </header>
    );
}
