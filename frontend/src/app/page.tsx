import { DarkModeToggle } from "@/components/ui/darkmode-toggle";

export default function Home() {
  return (
    <main className="p-10">
      <div className="flex justify-between">
        <h1 className="font-black text-3xl">Personal Homepage</h1>
        <DarkModeToggle></DarkModeToggle>
      </div>
    </main>
  );
}
