"use client"

import { useState } from "react"
import Link from "next/link"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { ArrowRight, Eye, EyeOff } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"

const signInSchema = z.object({
    email: z.email({ message: "Please enter a valid email address." }),
    password: z.string().min(6, { message: "Password must be at least 6 characters." }),
    rememberMe: z.boolean().default(false).optional(),
})

type SignInFormValues = z.infer<typeof signInSchema>

export const SignInCard = () => {
    const [showPassword, setShowPassword] = useState(false)

    const form = useForm<SignInFormValues>({
        resolver: zodResolver(signInSchema),
        defaultValues: {
            email: "",
            password: "",
            rememberMe: false,
        },
    })

    function onSubmit(data: SignInFormValues) {
        alert(JSON.stringify(data, null, 2))
    }

    return (
        <div className="w-full">
            <div className="text-center mb-10">
                <h2 className="text-foreground text-2xl font-bold tracking-tight">
                    Sign In to Woorkroom
                </h2>
            </div>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <FormField
                        control={form.control}
                        name="email"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel className="text-sm font-bold text-muted-foreground">
                                    Email Address
                                </FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="youremail@gmail.com"
                                        className="h-12 rounded-xl px-4"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel className="text-sm font-bold text-muted-foreground">
                                    Password
                                </FormLabel>
                                <FormControl>
                                    <div className="relative">
                                        <Input
                                            type={showPassword ? "text" : "password"}
                                            placeholder="••••••••"
                                            className="h-12 rounded-xl px-4 pr-12"
                                            {...field}
                                        />
                                        <Button
                                            type="button"
                                            variant="ghost"
                                            size="icon-sm"
                                            onClick={() => setShowPassword((current) => !current)}
                                            className="absolute top-1/2 right-3 -translate-y-1/2 rounded-full text-muted-foreground"
                                            aria-label={showPassword ? "Hide password" : "Show password"}
                                        >
                                            {showPassword ? (
                                                <EyeOff className="h-5 w-5" />
                                            ) : (
                                                <Eye className="h-5 w-5" />
                                            )}
                                        </Button>
                                    </div>
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <div className="flex items-center justify-between pt-2">
                        <FormField
                            control={form.control}
                            name="rememberMe"
                            render={({ field }) => (
                                <FormItem className="flex flex-row items-center space-x-3 space-y-0">
                                    <FormControl>
                                        <Checkbox
                                            checked={field.value}
                                            onCheckedChange={field.onChange}
                                            className="size-5 rounded-sm"
                                        />
                                    </FormControl>
                                    <FormLabel className="cursor-pointer text-base font-normal text-muted-foreground">
                                        Remember me
                                    </FormLabel>
                                </FormItem>
                            )}
                        />

                        <Link
                            href="/forgot-password"
                            className="text-muted-foreground font-normal hover:text-primary transition-colors"
                        >
                            Forgot Password?
                        </Link>
                    </div>

                    <div className="pt-6 pb-2">
                        <Button
                            type="submit"
                            className="h-12 w-full rounded-xl font-bold shadow-md cursor-pointer" 
                        >
                            Sign In
                            <ArrowRight className="size-5" />
                        </Button>
                    </div>

                    <div className="text-center pt-4">
                        <Link
                            href="/signup/step-1"
                            className="text-primary font-semibold hover:underline decoration-2 underline-offset-4"
                        >
                            Don&apos;t have an account?
                        </Link>
                    </div>

                </form>
            </Form>

        </div>
    )
}
