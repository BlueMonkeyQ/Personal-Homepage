import next from "next";
import Navbar from "@/components/Navbar";
import Fitness from "./fitness/page";
import Link from "next/link";
export default function Home() {
  return (
   <main>
    <Navbar />
    <h1>Hello World</h1>
   </main>
  );
}
