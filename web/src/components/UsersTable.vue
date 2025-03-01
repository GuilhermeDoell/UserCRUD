<script lang="ts" setup>
import type { User } from '@/userDTO'

interface Props {
    users: User[]
}

interface Emits {
    (e: 'edit', userId: string): void
    (e: 'delete', userId: string): void
    (e: 'create'): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const headers = [
    { title: 'Username', key: 'username' },
    { title: 'Roles', key: 'roles' },
    { title: 'Timezone', key: 'preferences.timezone' },
    { title: 'Is Active?', key: 'active' },
    { title: 'Last Updated At', key: 'updated_at' },
    { title: 'Created At', key: 'created_ts' },
    { title: 'Actions', key: 'actions', sortable: false },
]
</script>

<template>
    <v-data-table :items="users" :headers="headers" item-key="_id">
        <template v-slot:top>
            <v-row>
                <v-col cols="12">
                    <v-btn color="primary" @click="emit('create')">Create User</v-btn>
                </v-col>
            </v-row>
        </template>
        <template v-slot:item="{ item }">
            <tr>
                <td>
                    <RouterLink :to="{ name: 'userDetails', params: { id: item._id } }">
                        {{ item.username }}
                    </RouterLink>
                </td>
                <td>{{ item.roles }}</td>
                <td>{{ item.preferences.timezone }}</td>
                <td>{{ item.active ? '✅' : '❌' }}</td>
                <td>{{ new Date(item.updated_ts * 1000).toLocaleString() }}</td>
                <td>{{ new Date(item.created_ts * 1000).toLocaleString() }}</td>
                <td>
                    <v-icon @click="emit('edit', item._id)" class="mr-2" color="primary">
                        mdi-pencil
                    </v-icon>
                    <v-icon @click="emit('delete', item._id)" color="red"> mdi-delete </v-icon>
                </td>
            </tr>
        </template>
    </v-data-table>
</template>

<style scoped>
td {
    padding-inline: 1rem;
}
</style>
