"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

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
import { addWorkout } from "@/api-methods"
import { DateInput } from "./dateInput"
import React, { useEffect } from "react"
import { TimeSelector } from "./timeSelector"

const formSchema = z.object({
    reps: z.string({
        required_error: "Reps are required",
    }).refine(value => /^\d+$/.test(value), {
        message: "Reps must be a number.",
    }),
    weight: z.string({
        required_error: "Weight is required",
    }).refine(value => /^\d+$/.test(value), {
        message: "Weight must be a number.",
    }),
    date: z.string({
        required_error: "Date is required.",
    }),
    startTime: z.string({
        required_error: "Start time is required."
    })
});

export function FormAddWorkout() {
    const [date, setDate] = React.useState<Date>()
    const [startTime, setStartTime] = React.useState<string>()

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            reps: '',
            weight: '',
            date: undefined,
            startTime: undefined
        },
    })

    useEffect(() => {
        if (date) {
            console.log("Setting form value for date")
            form.setValue("date", date.toDateString())
            form.clearErrors("date")
        }
    }, [date])

    useEffect(() => {
        if (startTime) {
            console.log("Setting form value for date")
            form.setValue("startTime", startTime)
            form.clearErrors("startTime")
        }
    }, [startTime])

    async function onSubmit(values: z.infer<typeof formSchema>) {
        const combinedDateTime = combineDateTime(values.date, values.startTime);
        values.date = combinedDateTime;
        const { startTime, ...newValues } = values;
        console.log(newValues)
        // TODO: Integrate with BE when ready
        //const res = await addWorkout(values)
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
                        name="reps"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Reps</FormLabel>
                                <FormControl>
                                    <Input placeholder="0" {...field} />
                                </FormControl>
                                <FormDescription>
                                    This is your amount of repitions.
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="weight"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Weight</FormLabel>
                                <FormControl>
                                    <Input placeholder="0" {...field} />
                                </FormControl>
                                <FormDescription>
                                    This is your max weight in lbs.
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
                                <DateInput date={date} setDate={setDate}/>
                                    
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
                    <Button type="submit">Submit</Button>
                </form>
            </Form>
        </div>
    )
}
