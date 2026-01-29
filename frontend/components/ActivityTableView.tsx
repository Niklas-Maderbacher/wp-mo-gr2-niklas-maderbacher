import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { useState } from "react"
import axios from "axios"

import { Activity, ActivityCategory } from "@/components/types"

interface ActivitiesListProps {
    activities: Activity[]
    activityCategories: ActivityCategory[]
    onActivityAdded: () => void
    serverApiUrl: string
}

export function ActivitiesList({
    activities,
    activityCategories,
    onActivityAdded,
    serverApiUrl
}: ActivitiesListProps) {
    const [name, setName] = useState("")
    const [duration, setDuration] = useState<number>(0)
    const [categoryId, setCategoryId] = useState<string>("")
    const [isSubmitting, setIsSubmitting] = useState(false)

    const getCategoryName = (categoryId: number): string => {
        const category = activityCategories.find(cat => cat.id === categoryId)
        return category ? category.name : "Unknown"
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!name || !categoryId || duration <= 0) {
            return
        }

        setIsSubmitting(true)
        try {
            const token = localStorage.getItem("access_token")
            await axios.post(
                `${serverApiUrl}/activities/`,
                {
                    name,
                    duration,
                    category_id: Number(categoryId)
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )

            // Reset form
            setName("")
            setDuration(0)
            setCategoryId("")

            // Refresh activities list
            onActivityAdded()
        } catch (error) {
            console.error("Could not add activity:", error)
        } finally {
            setIsSubmitting(false)
        }
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Activities</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                {/* Add Activity Form */}
                <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-lg">
                    <h3 className="font-semibold">Add New Activity</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="flex flex-col gap-1">
                            <label className="text-sm">Name</label>
                            <Input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="Activity name"
                                required
                            />
                        </div>
                        <div className="flex flex-col gap-1">
                            <label className="text-sm">Category</label>
                            <Select value={categoryId} onValueChange={setCategoryId} required>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select category" />
                                </SelectTrigger>
                                <SelectContent>
                                    {activityCategories.map((category) => (
                                        <SelectItem key={category.id} value={category.id.toString()}>
                                            {category.name}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="flex flex-col gap-1">
                            <label className="text-sm">Duration (min)</label>
                            <Input
                                type="number"
                                min={1}
                                value={duration || ""}
                                onChange={(e) => setDuration(e.target.value === "" ? 0 : Number(e.target.value))}
                                placeholder="0"
                                required
                            />
                        </div>
                    </div>
                    <Button type="submit" disabled={isSubmitting}>
                        {isSubmitting ? "Adding..." : "Add Activity"}
                    </Button>
                </form>

                {/* Activities Table */}
                {activities.length === 0 ? (
                    <p className="text-sm text-muted-foreground text-center py-4">
                        No activities found
                    </p>
                ) : (
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Category</TableHead>
                                <TableHead>Duration</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {activities.map((activity) => (
                                <TableRow key={activity.id}>
                                    <TableCell>{activity.name}</TableCell>
                                    <TableCell>{getCategoryName(activity.category_id)}</TableCell>
                                    <TableCell>{activity.duration} min</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                )}
            </CardContent>
        </Card>
    )
}