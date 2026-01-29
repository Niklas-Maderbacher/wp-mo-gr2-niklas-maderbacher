import axios from "axios"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Sleep } from "@/components/types"

interface SleepCardProps {
    sleep: Sleep | null
    setSleep: (sleep: Sleep) => void
    sleepHours: number
    setSleepHours: (v: number) => void
    sleepMinutes: number
    setSleepMinutes: (v: number) => void
    apiUrl: string
}

export function SleepCard({
    sleep,
    setSleep,
    sleepHours,
    setSleepHours,
    sleepMinutes,
    setSleepMinutes,
    apiUrl
}: SleepCardProps) {
    const handleSubmit = async () => {
        const total = sleepHours * 60 + sleepMinutes

        const token = localStorage.getItem("access_token")
        if (!token) return

        try {
            if (!sleep) {
                const res = await axios.post(
                    `${apiUrl}/sleeps/`,
                    { duration: total },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                setSleep(res.data)
            } else {
                const res = await axios.put(
                    `${apiUrl}/sleeps/me`,
                    { duration: total },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                setSleep(res.data)
            }
        } catch (err) {
            console.error("Failed to update mood", err)
        }
    }

    return (
        <Card className="md:col-span-1">
            <CardHeader>
                <CardTitle>Sleep</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="flex gap-2">
                    <div className="flex flex-col gap-1">
                        <label className="text-sm">Hours</label>
                        <Input
                            type="number"
                            min={0}
                            value={sleepHours || ""}
                            onChange={(e) => setSleepHours(e.target.value === "" ? 0 : Number(e.target.value))}
                            placeholder={sleepHours !== 0 ? sleepHours.toString() : "0"}
                        />
                    </div>
                    <div className="flex flex-col gap-1">
                        <label className="text-sm">Minutes</label>
                        <Input
                            type="number"
                            min={0}
                            max={59}
                            value={sleepMinutes || ""}
                            onChange={(e) => setSleepMinutes(e.target.value === "" ? 0 : Number(e.target.value))}
                            placeholder={sleepMinutes !== 0 ? sleepMinutes.toString() : "0"}
                        />
                    </div>
                </div>
                <Button onClick={handleSubmit}>
                    Set sleep
                </Button>
            </CardContent>
        </Card>
    )
}