"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { useToast } from "@/components/ui/use-toast"

import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { addWorkout } from "@/lib/api-methods"
import { DateInput } from "./dateInput"
import React, { useEffect } from "react"
import { TimeSelector } from "./timeSelector"

const formSchema = z.object({
    workoutName: z.string().min(5, {
        message: "Workout name must be at least 5 characters.",
    }),
    date: z.string({
        required_error: "Date is required.",
    }),
    startTime: z.string({
        required_error: "Start time is required."
    }),
    duration: z.string().min(1, {
        message: "Duration must be at least 1 character.",
    }),
});

export function FormAddWorkout() {
    const [date, setDate] = React.useState<Date>()
    const [startTime, setStartTime] = React.useState<string>()

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            workoutName: '',
            date: undefined,
            startTime: undefined,
            duration: ''
        },
    })

    useEffect(() => {
        if (date) {
            console.log("Setting form value for date")
            form.setValue("date", date.toDateString())
            form.clearErrors("date")
        }
    }, [date, form])

    useEffect(() => {
        if (startTime) {
            console.log("Setting form value for date")
            form.setValue("startTime", startTime)
            form.clearErrors("startTime")
        }
    }, [startTime, form])

    const { toast } = useToast()

    async function onSubmit(values: z.infer<typeof formSchema>) {
        const combinedDateTime = combineDateTime(values.date, values.startTime);
        values.date = combinedDateTime;
      
        try {
          const res = await addWorkout(values);
          if (res) {
            toast({
              variant: "default",
              title: "Created.",
              description: "Your Workout was created successfully.",
            });
          }
        } catch (err: any) {
            toast({
              variant: "destructive",
              title: "Validation Error",
              description: err.message,
            });
        }
      }

    function combineDateTime(dateString: string, startTime: string): string {
        const date = new Date(dateString);

        const [hours, minutes] = startTime.split(':').map(Number);

        date.setHours(hours);
        date.setMinutes(minutes);

        return date.toISOString();
    }

    return (
        <div className="border rounded-xl p-10 max-w-[500px]">
            <Form {...form}>
                <h3 className="text-xl font-semibold mb-5">Add a new workout</h3>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                    <FormField
                        control={form.control}
                        name="workoutName"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Workout Name</FormLabel>
                                <FormControl>
                                    <Input placeholder="Hunkfest 29" {...field} />

                                </FormControl>

                                <FormDescription>
                                    This is the name of your workout.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="date"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Date</FormLabel>
                                <FormControl>
                                    <DateInput date={date} setDate={setDate} />

                                </FormControl>

                                <FormDescription>
                                    This is when you did the workout.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="startTime"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Start Time</FormLabel>
                                <FormControl>
                                    <TimeSelector setStartTime={setStartTime} />
                                </FormControl>

                                <FormDescription>
                                    This is when you started the workout.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="duration"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Duration</FormLabel>
                                <FormControl>
                                    <Input placeholder="1" {...field} />
                                </FormControl>

                                <FormDescription>
                                    This is how long your workout lasted in hours.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <Button type="submit">Submit</Button>
                </form>
            </Form>
        </div>
    )
}
