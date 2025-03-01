interface UserPreferences {
    timezone: string
}

export interface User {
    _id: string
    username: string
    password: string
    roles: string[]
    preferences: UserPreferences
    active: boolean
    updated_ts: number
    created_ts: number
}

export interface CreateUserDTO {
    username: string
    password: string
    roles: string[]
    preferences: UserPreferences
    active: boolean
}

export interface UpdateUserDTO extends Partial<User> {}
