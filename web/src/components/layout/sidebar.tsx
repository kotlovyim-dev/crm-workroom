"use client";

import { Card } from "@/components/ui/card";
import Image from "next/image";
import { NAV_ITEMS } from "@/config/sidebar-nav.config";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "../ui/button";
import { MessageCircleIcon } from "lucide-react";

export function Sidebar() {
    const pathname = usePathname();

    return (
        <nav>
            <Card className="sticky top-5 h-[calc(100vh-40px)] w-55 rounded-lg border px-4">
                <Image src="/logo.svg" alt="Logo" width={50} height={50} />
                <div className="flex flex-col justify-between h-full">
                    <div className="flex flex-col gap-2 w-full">
                        {NAV_ITEMS.map((item) => (
                            <Link
                                key={item.label}
                                href={item.href}
                                className={cn(
                                    "flex items-center w-full p-2 gap-4 rounded-md transition-colors duration-200",
                                    pathname === item.href
                                        ? "bg-primary/10 text-primary"
                                        : "text-foreground/70 hover:bg-secondary/50 hover:text-foreground",
                                )}
                            >
                                {item.icon && <item.icon size={24} />}
                                <span className="text-base ">{item.label}</span>
                            </Link>
                        ))}
                    </div>
                    <div className="w-full p-4 bg-background rounded-lg flex flex-col items-center gap-4">
                        <Image src="/illustration.svg" alt="Logo" width={140} height={124} />
                        <Button className="w-full"><MessageCircleIcon />Support</Button>
                    </div>
                </div>

            </Card>
        </nav>
    );
}
