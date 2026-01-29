export interface Activity {
    id: number,
    name: string,
    duration: number,
    category_id: number,
}

export interface ActivityCategory {
    id: number,
    name: string,
}

export type MoodEnum = "excellent" | "good" | "okay" | "bad" | "very bad"

export const moods: MoodEnum[] = ["excellent", "good", "okay", "bad", "very bad"]

export interface Mood {
    mood: MoodEnum
}

export interface Sleep {
    duration: number
}

export interface User {
    id: number,
    username: string,
    email: string,
    is_superuser: boolean,
}