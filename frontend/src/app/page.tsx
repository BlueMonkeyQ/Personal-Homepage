import { DarkModeToggle } from "@/components/ui/darkmode-toggle";
import { getWorkouts } from "@/api-methods";
import { FormAddWorkout } from "@/components/custom/formAddWorkout";

export default async function Home() {
  const data = await getWorkouts('1', "2001%2F01%2F02");
  return (
    <main className="p-10">
      <div className="flex justify-between">
        <h1 className="font-black text-3xl">Personal Homepage</h1>
        <DarkModeToggle></DarkModeToggle>
      </div>
      <pre>{JSON.stringify(data, null, 3)}</pre>
      <FormAddWorkout/>
    </main>
  );
}
