import { Button } from "./ui/button"
import Link from "next/link"
import { LogOut } from "lucide-react"
import { useRouter } from "next/navigation"

export function NavBar() {
    const router = useRouter()

    const handleLogout = () => {
        localStorage.removeItem("access_token")
        router.push("/login")
    }

    return (
        <div className="mb-8">
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-blue-900">
                    Health Log
                </h1>
                <Button variant="outline" onClick={handleLogout} className="gap-2">
                    <LogOut className="h-4 w-4" />
                    Logout
                </Button>
            </div>

            <div className="flex gap-3">
                <Button asChild variant="default">
                    <Link href="/activities">Activities</Link>
                </Button>
                <Button asChild variant="default">
                    <Link href="/sleep">Sleep</Link>
                </Button>
                <Button asChild variant="default">
                    <Link href="/mood">Mood</Link>
                </Button>
            </div>
        </div>
    )
}