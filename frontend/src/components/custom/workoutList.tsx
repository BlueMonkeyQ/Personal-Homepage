'use client'
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { getWorkouts } from "@/lib/api-methods";
import { useEffect, useState } from "react";


export function WorkoutList() {
    const [data, setData] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const result = await getWorkouts('2', "2024-06-09T09:00:00.000Z");
            setData(result);
        }
        fetchData();
    }, []);
    return (
        <div className="border rounded-xl">
            <h3 className="text-lg font-regular p-5 mb-5">A list of your workouts, today at 4AM.</h3>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead className="w-[100px]">ID</TableHead>
                        <TableHead>Name</TableHead>
                        <TableHead>Duration</TableHead>
                        <TableHead>Date</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {data.map((workout: any) => (
                        <TableRow key={workout.id}>
                            <TableCell>{workout.id}</TableCell>
                            <TableCell className="font-medium">{workout.name}</TableCell>
                            <TableCell>{workout.duration}hr(s)</TableCell>
                            <TableCell>{workout.date}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    )
}
