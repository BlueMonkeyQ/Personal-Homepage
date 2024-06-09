import Link from "next/link";

export default function Navbar(){
    return(
        <header>
            <div>
                <h1>Welcome User</h1>
                <nav>
                    <ul>
                        <li>
                            <Link href='/fitness'>Fitness</Link>
                        </li>
                        <li>
                            <Link href='/'>Home</Link>
                        </li>
                        <li>
                            <Link href='/tasks'>Tasks</Link>
                        </li>
                        <li>
                            <Link href='/finances'>Finance</Link>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>
    )
}