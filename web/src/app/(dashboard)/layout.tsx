import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";

export default function DashboardLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className="flex flex-row w-full gap-7.5 p-5">
            <Sidebar />
            <div className="flex flex-col flex-1 min-w-0 gap-5">
                <Topbar />
                {children}
            </div>
        </div>
    );
}
