<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import UserService from '@/api/UserService'
import type { User, UpdateUserDTO } from '@/userDTO'
import UserDialog from '@/components/UserDialog.vue'
import DeleteDialog from '@/components/DeleteDialog.vue'

const route = useRoute()
const router = useRouter()
const userId = route.params.id as string
const user = ref<User | null>(null)
const loading = ref(true)

// Dialog controls
const editDialogVisible = ref(false)
const deleteDialogVisible = ref(false)

const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
}

async function handleUpdate(updatedUser: UpdateUserDTO) {
    try {
        await UserService.updateUser(userId, updatedUser)
        user.value = (await UserService.getUser(userId)) as User
        editDialogVisible.value = false
    } catch (error) {
        console.error('Failed to update user:', error)
    }
}

async function handleDelete() {
    try {
        await UserService.deleteUser(userId)
        router.push('/')
    } catch (error) {
        console.error('Failed to delete user:', error)
    }
}

onMounted(async () => {
    try {
        user.value = (await UserService.getUser(userId)) as User
    } catch (error) {
        console.error('Failed to fetch user:', error)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <v-container v-if="user">
        <v-row v-if="loading" justify="center" align="center">
            <v-progress-circular
                indeterminate
                color="primary"
                size="64"
            ></v-progress-circular>
        </v-row>
        <v-card v-else-if="user">
            <v-card-title class="d-flex justify-space-between align-center">
                <h1>User Details</h1>
                <div>
                    <v-btn color="primary" class="mr-2" @click="editDialogVisible = true">
                        <v-icon>mdi-pencil</v-icon>
                        Edit
                    </v-btn>
                    <v-btn color="error" @click="deleteDialogVisible = true">
                        <v-icon>mdi-delete</v-icon>
                        Delete
                    </v-btn>
                </div>
            </v-card-title>

            <v-card-text>
                <v-list>
                    <v-list-item>
                        <v-list-item-title>Username</v-list-item-title>
                        <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Roles</v-list-item-title>
                        <v-list-item-subtitle>
                            <v-chip v-for="role in user.roles" :key="role" class="mr-2">
                                {{ role }}
                            </v-chip>
                        </v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Timezone</v-list-item-title>
                        <v-list-item-subtitle>{{ user.preferences.timezone }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Status</v-list-item-title>
                        <v-list-item-subtitle>
                            <v-chip :color="user.active ? 'success' : 'error'">
                                {{ user.active ? 'Active' : 'Inactive' }}
                            </v-chip>
                        </v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Last Updated</v-list-item-title>
                        <v-list-item-subtitle>{{
                            formatDate(user.updated_ts)
                        }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Created At</v-list-item-title>
                        <v-list-item-subtitle>{{
                            formatDate(user.created_ts)
                        }}</v-list-item-subtitle>
                    </v-list-item>
                </v-list>
            </v-card-text>
        </v-card>

        <!-- Edit User Dialog -->
        <UserDialog
            v-model="editDialogVisible"
            :user="user"
            @update:modelValue="(val) => (editDialogVisible = val)"
            @updateUser="handleUpdate"
        />

        <!-- Delete Confirmation Dialog -->
        <DeleteDialog v-model="deleteDialogVisible" :user="user" @confirm="handleDelete" />
    </v-container>
    <v-container v-else>
        <v-alert type="error">User not found</v-alert>
    </v-container>
</template>

<style scoped>
.v-list-item-title {
    font-weight: bold;
    color: rgba(0, 0, 0, 0.6);
}
</style>
