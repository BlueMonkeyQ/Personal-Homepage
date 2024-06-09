import { DarkModeToggle } from "@/components/ui/darkmode-toggle";
import { WorkoutList } from "@/components/custom/workoutList";
import { FormAddWorkout } from "@/components/custom/formAddWorkout";

export default function Home() {
  

  return (
    <main className="p-10">
      <div className="flex justify-between">
        <h1 className="font-black text-3xl">Personal Homepage</h1>
        <DarkModeToggle />
      </div>

      <WorkoutList />
      <FormAddWorkout />
    </main>
  );
}