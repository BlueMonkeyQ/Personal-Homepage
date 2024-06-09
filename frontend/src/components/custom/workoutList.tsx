'use client'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Label } from "../ui/label";
import { getWorkouts, deleteWorkout } from "@/lib/api-methods";
import { useEffect, useState } from "react";
import { Button } from "../ui/button";
import { useToast } from "../ui/use-toast";
import { Copy } from "lucide-react";
import { Input } from "../ui/input";


export function WorkoutList() {
    const [data, setData] = useState([]);
    const { toast } = useToast()

    useEffect(() => {
        async function fetchData() {
            const result = await getWorkouts('2', "2024-06-09T09:00:00.000Z");
            setData(result);
        }
        fetchData();
    }, []);

    const handleDelete = async (id: string) => {

        try {
            const res = await deleteWorkout(id);
            if (res) {
                toast({
                    variant: "default",
                    title: "Workout Deleted.",
                    description: "Your Workout was deleted successfully.",
                });
                setData(data.filter((workout: any) => workout.id !== id));
            }
        } catch (err: any) {
            toast({
                variant: "destructive",
                title: "Validation Error",
                description: err.message,
            });
        }
    };

    return (
        <div className="border rounded-xl my-10">
            
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead className="w-[100px]">ID</TableHead>
                        <TableHead>Name</TableHead>
                        <TableHead>Duration</TableHead>
                        <TableHead>Date</TableHead>
                        <TableHead>Action</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {data.map((workout: any) => (
                        <TableRow key={workout.id}>
                            <TableCell>{workout.id}</TableCell>
                            <TableCell className="font-medium">{workout.name}</TableCell>
                            <TableCell>{workout.duration}hr(s)</TableCell>
                            <TableCell>{workout.date}</TableCell>
                            <TableCell className="flex gap-5">

                                <Dialog>
                                    <DialogTrigger asChild>
                                    <Button variant={"destructive"}>Delete</Button>
                                    </DialogTrigger>
                                    <DialogContent className="sm:max-w-md">
                                        <DialogHeader>
                                            <DialogTitle>Are you sure you want to delete this workout?</DialogTitle>
                                            <DialogDescription>
                                                You will not be able to restore this.
                                            </DialogDescription>
                                        </DialogHeader>
                                        <DialogFooter className="sm:justify-start">
                                            <DialogClose asChild>
                                                <Button onClick={() => handleDelete(workout.id)} type="button" variant={"destructive"}>
                                                    Delete Forever
                                                </Button>
                                            </DialogClose>
                                        </DialogFooter>
                                    </DialogContent>
                                </Dialog>

                                <Button variant={"default"}>Edit</Button>

                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    )
}
