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
import { Check, X, Pencil, Search } from "lucide-react"

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

    // Edit state
    const [editingId, setEditingId] = useState<number | null>(null)
    const [editName, setEditName] = useState("")
    const [editDuration, setEditDuration] = useState<number>(0)
    const [editCategoryId, setEditCategoryId] = useState<string>("")

    // Search state
    const [searchQuery, setSearchQuery] = useState("")

    const getCategoryName = (categoryId: number): string => {
        const category = activityCategories.find(cat => cat.id === categoryId)
        return category ? category.name : "Unknown"
    }

    // Filter activities based on search query
    const filteredActivities = activities.filter(activity =>
        activity.name.toLowerCase().includes(searchQuery.toLowerCase())
    )

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

    const handleEditClick = (activity: Activity) => {
        setEditingId(activity.id)
        setEditName(activity.name)
        setEditDuration(activity.duration)
        setEditCategoryId(activity.category_id.toString())
    }

    const handleCancelEdit = () => {
        setEditingId(null)
        setEditName("")
        setEditDuration(0)
        setEditCategoryId("")
    }

    const handleSaveEdit = async (activityId: number) => {
        if (!editName || !editCategoryId || editDuration <= 0) {
            return
        }

        try {
            const token = localStorage.getItem("access_token")
            await axios.put(
                `${serverApiUrl}/activities/${activityId}`,
                {
                    name: editName,
                    duration: editDuration,
                    category_id: Number(editCategoryId)
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )

            setEditingId(null)
            onActivityAdded() // Refresh the list
        } catch (error) {
            console.error("Could not update activity:", error)
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

                {/* Search Bar */}
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                        type="text"
                        placeholder="Search activities by name..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-10"
                    />
                </div>

                {/* Activities Table */}
                {filteredActivities.length === 0 ? (
                    <p className="text-sm text-muted-foreground text-center py-4">
                        {searchQuery ? "No activities found matching your search" : "No activities found"}
                    </p>
                ) : (
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Category</TableHead>
                                <TableHead>Duration</TableHead>
                                <TableHead className="w-[100px]">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredActivities.map((activity) => (
                                <TableRow key={activity.id}>
                                    {editingId === activity.id ? (
                                        <>
                                            <TableCell>
                                                <Input
                                                    type="text"
                                                    value={editName}
                                                    onChange={(e) => setEditName(e.target.value)}
                                                    className="h-8"
                                                />
                                            </TableCell>
                                            <TableCell>
                                                <Select value={editCategoryId} onValueChange={setEditCategoryId}>
                                                    <SelectTrigger className="h-8">
                                                        <SelectValue />
                                                    </SelectTrigger>
                                                    <SelectContent>
                                                        {activityCategories.map((category) => (
                                                            <SelectItem key={category.id} value={category.id.toString()}>
                                                                {category.name}
                                                            </SelectItem>
                                                        ))}
                                                    </SelectContent>
                                                </Select>
                                            </TableCell>
                                            <TableCell>
                                                <Input
                                                    type="number"
                                                    min={1}
                                                    value={editDuration}
                                                    onChange={(e) => setEditDuration(Number(e.target.value))}
                                                    className="h-8 w-24"
                                                />
                                            </TableCell>
                                            <TableCell>
                                                <div className="flex gap-2">
                                                    <Button
                                                        size="icon"
                                                        variant="ghost"
                                                        className="h-8 w-8"
                                                        onClick={() => handleSaveEdit(activity.id)}
                                                    >
                                                        <Check className="h-4 w-4" />
                                                    </Button>
                                                    <Button
                                                        size="icon"
                                                        variant="ghost"
                                                        className="h-8 w-8"
                                                        onClick={handleCancelEdit}
                                                    >
                                                        <X className="h-4 w-4" />
                                                    </Button>
                                                </div>
                                            </TableCell>
                                        </>
                                    ) : (
                                        <>
                                            <TableCell>{activity.name}</TableCell>
                                            <TableCell>{getCategoryName(activity.category_id)}</TableCell>
                                            <TableCell>{activity.duration} min</TableCell>
                                            <TableCell>
                                                <Button
                                                    size="icon"
                                                    variant="ghost"
                                                    className="h-8 w-8"
                                                    onClick={() => handleEditClick(activity)}
                                                >
                                                    <Pencil className="h-4 w-4" />
                                                </Button>
                                            </TableCell>
                                        </>
                                    )}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                )}
            </CardContent>
        </Card>
    )
}