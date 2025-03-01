<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import UserService from '@/api/UserService'
import UserDialog from '@/components/UserDialog.vue'
import DeleteDialog from '@/components/DeleteDialog.vue'
import UsersTable from '@/components/UsersTable.vue'
import type { CreateUserDTO, UpdateUserDTO, User } from '@/userDTO'

const users = ref<User[]>([])

//  --> Open/Close Dialogs state management <--  //
const editCreateDialogVisible = ref<boolean>(false)
const selectedUser = ref<User | null>(null)
const deleteDialogVisible = ref<boolean>(false)
const userToDelete = ref<User | null>(null)

function openCreateDialog() {
    selectedUser.value = null
    editCreateDialogVisible.value = true
}

function openEditDialog(userId: string) {
    selectedUser.value = { ...users.value.find((u) => u._id === userId)! }
    editCreateDialogVisible.value = true
}

//  --> Create/Delete/Update users <--  //
async function updateUser(userData: UpdateUserDTO) {
    try {
        if (selectedUser.value) {
            await UserService.updateUser(selectedUser.value._id, userData)
            // Refresh users list
            users.value = await UserService.getUsers()
        }
        editCreateDialogVisible.value = false
    } catch (error) {
        console.error('Failed to update user:', error)
    }
}

async function createUser(userData: CreateUserDTO) {
    editCreateDialogVisible.value = false
    // UserService.createUser(userData)
    //     .then((newUser) => {
    //         users.value = [...users.value, newUser]
    //     })
    //     .catch((error) => {
    //         console.error('Failed to create user:', error)
    //     })
}

async function deleteUser() {
    if (userToDelete.value) {
        try {
            await UserService.deleteUser(userToDelete.value._id)
            users.value = users.value.filter((u) => u._id !== userToDelete.value!._id)
            deleteDialogVisible.value = false
        } catch (error) {
            console.error('Failed to delete user:', error)
        }
    }
}

function confirmDelete(userId: string) {
    userToDelete.value = users.value.find((u) => u._id === userId)!
    deleteDialogVisible.value = true
}

onMounted(async () => {
    try {
        users.value = await UserService.getUsers()
    } catch (error) {
        console.error('Failed to fetch users:', error)
    }
})
</script>

<template>
    <v-app>
        <v-container fluid>
            <UsersTable
                :users="users"
                @edit="openEditDialog"
                @delete="confirmDelete"
                @create="openCreateDialog"
            />

            <!-- Create/Edit User Dialog -->
            <UserDialog
                :model-value="editCreateDialogVisible"
                :user="selectedUser"
                @update:modelValue="(val) => (editCreateDialogVisible = val)"
                @updateUser="updateUser"
                @create="createUser"
            />

            <!-- Delete Confirmation Dialog -->
            <DeleteDialog
                v-model="deleteDialogVisible"
                :user="userToDelete"
                @confirm="deleteUser"
            />
        </v-container>
    </v-app>
</template>

<style scoped>
td {
    padding-inline: 1rem;
}
</style>
