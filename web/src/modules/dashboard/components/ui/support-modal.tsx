"use client";

import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTrigger, DialogTitle } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import Image from "next/image";

interface SupportModalProps {
    children: React.ReactNode;
}

export function SupportModal({ children }: SupportModalProps) {
    return (
        <Dialog>
            <DialogTrigger asChild>
                {children}
            </DialogTrigger>
            <DialogContent className="sm:max-w-xl p-0 border-none rounded-3xl overflow-hidden gap-0 bg-card">
                <DialogTitle className="sr-only">Support Request</DialogTitle>
                <div className="relative w-full h-64 flex items-center justify-center bg-secondary">
                    <Image src="/bg.svg" alt="Background decoration" fill className="absolute inset-0 object-cover opacity-50" />
                    <Image src="/illustration.svg" alt="Support Illustration" width={240} height={240} className="relative z-10" />
                </div>

                <div className="flex flex-col gap-6 p-10 pt-8">
                    <div className="flex flex-col gap-2">
                        <h2 className="text-2xl font-bold text-foreground">Need some Help?</h2>
                        <p className="text-base text-muted-foreground leading-relaxed">
                            Describe your question and our specialists will answer you within 24 hours.
                        </p>
                    </div>

                    <div className="flex flex-col gap-5">
                        <div className="flex flex-col gap-2">
                            <Label className="text-sm font-bold text-muted-foreground">Request Subject</Label>
                            <Select defaultValue="technical">
                                <SelectTrigger className="h-12 rounded-xl py-6 px-4 text-muted-foreground">
                                    <SelectValue placeholder="Technical difficulites" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="technical" className="py-3 px-2">Technical difficulties</SelectItem>
                                    <SelectItem value="billing" className="py-3 px-2">Billing issue</SelectItem>
                                    <SelectItem value="general" className="py-3 px-2">General inquiry</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="flex flex-col gap-2">
                            <Label className="text-sm font-bold text-muted-foreground">Description</Label>
                            <Textarea
                                placeholder="Add some description of the request"
                                className="min-h-32 rounded-xl resize-none"
                            />
                        </div>
                    </div>

                    <div className="flex justify-end pt-2">
                        <Button className="font-bold text-base h-12 w-36 rounded-xl shadow-md">
                            Send Request
                        </Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
}
