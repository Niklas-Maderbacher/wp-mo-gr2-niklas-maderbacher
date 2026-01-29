import { ChevronDown } from "lucide-react"
import axios from "axios"
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuRadioGroup,
    DropdownMenuRadioItem
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { MoodEnum, Mood } from "@/components/types"

interface MoodSelectorProps {
    mood: Mood | null
    setMood: (mood: Mood) => void
    moods: MoodEnum[]
    apiUrl: string
}

export function MoodSelector({ mood, setMood, moods, apiUrl }: MoodSelectorProps) {
    const handleChange = async (value: string) => {
        const token = localStorage.getItem("access_token")
        if (!token) return

        try {
            if (!mood) {
                const res = await axios.post(
                    `${apiUrl}/moods/`,
                    { mood: value as MoodEnum },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                setMood(res.data)
            } else {
                const res = await axios.put(
                    `${apiUrl}/moods/me`,
                    { mood: value as MoodEnum },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                setMood(res.data)
            }
        } catch (err) {
            console.error("Failed to update mood", err)
        }
    }

    return (
        <Card className="md:col-span-1">
            <CardHeader>
                <CardTitle>Mood</CardTitle>
            </CardHeader>

            <CardContent>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button
                            variant="outline"
                            className="flex items-center justify-between gap-2 w-full"
                        >
                            {mood?.mood ?? "Set mood"}
                            <ChevronDown className="w-4 h-4" />
                        </Button>
                    </DropdownMenuTrigger>

                    <DropdownMenuContent>
                        <DropdownMenuRadioGroup
                            value={mood?.mood || ""}
                            onValueChange={handleChange}
                        >
                            {moods.map((m) => (
                                <DropdownMenuRadioItem key={m} value={m}>
                                    {m}
                                </DropdownMenuRadioItem>
                            ))}
                        </DropdownMenuRadioGroup>
                    </DropdownMenuContent>
                </DropdownMenu>
            </CardContent>
        </Card>
    )
}
