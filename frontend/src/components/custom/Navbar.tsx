import Link from "next/link";
import { DarkModeToggle } from "../ui/darkmode-toggle";

export default function Navbar() {
    return (
        <header className="p-10">
            <div className="flex justify-between">
                <h1 className="font-black text-3xl">Personal Homepage</h1>
                <DarkModeToggle></DarkModeToggle>
            </div>
            <h2 className="text-2xl font-bold">Welcome User</h2>
            <div className="container mx-auto px-0 py-0">
                <nav>
                    <ul className="flex space-x-4 mt-4">
                        <li className="text-black-300 hover:text-white hover:bg-gray-700 px-3 py-2 rounded-md">
                            <Link href='/'>Home</Link>
                        </li>
                        <li className="text-black-300 hover:text-white hover:bg-gray-700 px-3 py-2 rounded-md">
                            <Link href='/fitness'>Fitness</Link>
                        </li>
                        <li className="text-black-300 hover:text-white hover:bg-gray-700 px-3 py-2 rounded-md">
                            <Link href='/tasks'>Tasks</Link>
                        </li>
                        <li className="text-black-300 hover:text-white hover:bg-gray-700 px-3 py-2 rounded-md">
                            <Link href='/finance'>Finance</Link>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>
    )
}