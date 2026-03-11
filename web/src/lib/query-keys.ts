import type { QueryKeyParams, QueryKeyPrimitive } from "@/lib/api/contracts"

function normalizeQueryValue(value: QueryKeyPrimitive | readonly QueryKeyPrimitive[]) {
    if (Array.isArray(value)) {
        return value.map((item) => item ?? null)
    }

    return value ?? null
}

function normalizeQueryParams(params?: QueryKeyParams) {
    if (!params) {
        return undefined
    }

    const entries = Object.entries(params)
        .filter(([, value]) => {
            if (Array.isArray(value)) {
                return value.length > 0
            }

            return value !== undefined
        })
        .sort(([leftKey], [rightKey]) => leftKey.localeCompare(rightKey))
        .map(([key, value]) => [key, normalizeQueryValue(value)])

    return Object.fromEntries(entries)
}

export const queryKeys = {
    auth: {
        all: () => ["auth"] as const,
        session: () => ["auth", "session"] as const,
    },
    people: {
        all: () => ["people"] as const,
        employees: (params?: QueryKeyParams) => ["people", "employees", normalizeQueryParams(params)] as const,
        employeeActivity: (params?: QueryKeyParams) =>
            ["people", "employees", "activity", normalizeQueryParams(params)] as const,
        profileMe: () => ["people", "profile", "me"] as const,
        notificationSettings: () => ["people", "settings", "notifications"] as const,
        vacationBalances: (params?: QueryKeyParams) =>
            ["people", "vacations", "balances", normalizeQueryParams(params)] as const,
        vacationRequests: (params?: QueryKeyParams) =>
            ["people", "vacations", "requests", normalizeQueryParams(params)] as const,
        vacationTimeline: (params?: QueryKeyParams) =>
            ["people", "vacations", "timeline", normalizeQueryParams(params)] as const,
        calendarEvents: (params?: QueryKeyParams) =>
            ["people", "calendar", "events", normalizeQueryParams(params)] as const,
    },
    projects: {
        all: () => ["projects"] as const,
        list: (params?: QueryKeyParams) => ["projects", "list", normalizeQueryParams(params)] as const,
        detail: (projectId: string) => ["projects", "detail", projectId] as const,
        tasks: (projectId: string, params?: QueryKeyParams) =>
            ["projects", projectId, "tasks", normalizeQueryParams(params)] as const,
        task: (taskId: string) => ["projects", "task", taskId] as const,
        taskTimeLogs: (taskId: string, params?: QueryKeyParams) =>
            ["projects", "task", taskId, "time-logs", normalizeQueryParams(params)] as const,
    },
    infoPortal: {
        all: () => ["info-portal"] as const,
        folders: (params?: QueryKeyParams) => ["info-portal", "folders", normalizeQueryParams(params)] as const,
        folder: (folderId: string) => ["info-portal", "folder", folderId] as const,
        page: (pageId: string) => ["info-portal", "page", pageId] as const,
        shares: (params?: QueryKeyParams) => ["info-portal", "shares", normalizeQueryParams(params)] as const,
    },
    messenger: {
        all: () => ["messenger"] as const,
        conversations: (params?: QueryKeyParams) =>
            ["messenger", "conversations", normalizeQueryParams(params)] as const,
        conversation: (conversationId: string) => ["messenger", "conversation", conversationId] as const,
        messages: (conversationId: string, params?: QueryKeyParams) =>
            ["messenger", "conversation", conversationId, "messages", normalizeQueryParams(params)] as const,
        presence: (conversationId: string) => ["messenger", "conversation", conversationId, "presence"] as const,
    },
}