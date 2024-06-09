'use client'
import React, { useEffect, useState } from "react";
import { DarkModeToggle } from "@/components/ui/darkmode-toggle";
import { getWorkouts } from "@/lib/api-methods";
import { FormAddWorkout } from "@/components/custom/formAddWorkout";

export default function Home() {
  const [data, setData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const result = await getWorkouts('2', "2024-06-09T09:00:00.000Z");
      setData(result);
    }
    fetchData();
  }, []);

  return (
    <main className="p-10">
      <div className="flex justify-between">
        <h1 className="font-black text-3xl">Personal Homepage</h1>
        <DarkModeToggle />
      </div>
        <h3>Workouts Today at 4AM</h3>
        <pre>{JSON.stringify(data, null, 3)}</pre>
      
      <FormAddWorkout />
    </main>
  );
}