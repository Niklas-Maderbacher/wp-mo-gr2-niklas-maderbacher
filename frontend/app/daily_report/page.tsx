'use client'

import { useEffect, useState } from "react"
import axios, { AxiosResponse } from "axios"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuTrigger,
    DropdownMenuRadioGroup,
    DropdownMenuRadioItem,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

import { ActivityCategory, Activity, MoodEnum, Mood, moods, Sleep } from "@/components/types"
import { SERVER_API_URL } from "@/next.config"

import { MoodSelector } from "@/components/MoodSelector"
import { SleepCard } from "@/components/SleepCard"
import { ActivitiesList } from "@/components/ActivityTableView"

export default function DailyReport() {
    const [activityCategories, setActivityCategories] = useState<ActivityCategory[]>([])
    const [activities, setActivities] = useState<Activity[]>([])
    const [mood, setMood] = useState<Mood | null>(null)
    const [sleep, setSleep] = useState<Sleep | null>(null)

    const [sleepHours, setSleepHours] = useState(0)
    const [sleepMinutes, setSleepMinutes] = useState(0)

    const fetchActivityCategories = async () => {
        try {
            const response = await axios.get(
                `${SERVER_API_URL}/activity-categories/`
            )

            setActivityCategories(response.data)
        } catch {
            console.log(
                "Could not fetch Activities Category, this could be because none exist yet"
            )
        }
    }

    const fetchActivities = async () => {
        try {
            const token = localStorage.getItem("access_token")

            const response = await axios.get(
                `${SERVER_API_URL}/activities/me`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                },
            )

            setActivities(response.data)
        } catch {
            console.log(
                "Could not fetch Activities, this could be because none exist yet"
            )
        }
    }

    const fetchMood = async () => {
        try {
            const token = localStorage.getItem("access_token")

            const response = await axios.get(
                `${SERVER_API_URL}/moods/me`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                },
            )

            setMood(response.data)
        } catch {
            console.log(
                "Could not fetch Moods, this could be because none exist yet"
            )
        }
    }

    const fetchSleep = async () => {
        try {
            const token = localStorage.getItem("access_token")

            const response = await axios.get(
                `${SERVER_API_URL}/sleeps/me`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                },
            )

            const totalMinutes = response.data.duration || 0;
            const hours = Math.floor(totalMinutes / 60);
            const minutes = totalMinutes % 60;

            setSleep(response.data);
            setSleepHours(hours);
            setSleepMinutes(minutes);
        } catch {
            console.log(
                "Could not fetch Sleep, this could be because none exist yet"
            )
        }
    }

    useEffect(() => {
        fetchActivities()
        fetchActivityCategories()
        fetchSleep()
        fetchMood()
    }, [])


    return (
        <div>
            <h1 className="text-center text-xl md:text-5xl font-bold tracking-tight text-blue-900">
                Health-Log
            </h1>

            <div className="grid grid-cols-2">
                <MoodSelector
                    mood={mood}
                    setMood={setMood}
                    moods={moods}
                    apiUrl={SERVER_API_URL}
                />

                <SleepCard
                    sleep={sleep}
                    setSleep={setSleep}
                    sleepHours={sleepHours}
                    setSleepHours={setSleepHours}
                    sleepMinutes={sleepMinutes}
                    setSleepMinutes={setSleepMinutes}
                    apiUrl={SERVER_API_URL}
                />
            </div>

            <div>
                <ActivitiesList
                    activities={activities}
                    activityCategories={activityCategories}
                    onActivityAdded={fetchActivities} // This will refresh the activities list
                    serverApiUrl={SERVER_API_URL}
                />
            </div>
        </div>
    );
}