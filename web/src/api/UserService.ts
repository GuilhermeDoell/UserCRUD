import type { User, CreateUserDTO, UpdateUserDTO } from '@/userDTO'
import { API_BASE_URL } from '@/api/api'

async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || 'An error occurred')
    }

    return response.json()
}

export async function getUsers(): Promise<User[]> {
    const response = await fetch(`${API_BASE_URL}/users`)
    return handleResponse<User[]>(response)
}

export async function getUser(id: string): Promise<User | undefined> {
    const response = await fetch(`${API_BASE_URL}/users/${id}`)
    return handleResponse<User>(response)
}

export async function createUser(userData: CreateUserDTO): Promise<{ inserted_id: string }> {
    const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    return handleResponse<{ inserted_id: string }>(response)
}

export async function updateUser(
    id: string,
    userData: UpdateUserDTO,
): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/users/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    return handleResponse<{ message: string }>(response)
}

export async function deleteUser(id: string): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/users/${id}`, {
        method: 'DELETE',
    })
    return handleResponse<{ message: string }>(response)
}

export default {
    getUsers,
    getUser,
    createUser,
    updateUser,
    deleteUser,
}
