<script lang="ts" setup>
import type { CreateUserDTO, UpdateUserDTO, User } from '@/userDTO'
import { ref, watch, computed } from 'vue'

const props = defineProps<{
    modelValue: boolean
    user: User | null
}>()

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'updateUser', userData: UpdateUserDTO): void
    (e: 'create', userData: CreateUserDTO): void
}>()

const allRoles = ['admin', 'manager', 'editor', 'user']
const isEditMode = computed<boolean>(() => !!props.user?._id)
const confirmDialogVisible = ref(false)
const updateOrNewUser = ref<UpdateUserDTO | CreateUserDTO | null>(null)

// Local copy of the dialog visibility
const localVisible = ref<boolean>(props.modelValue)

watch(localVisible, (val) => {
    emit('update:modelValue', val)
})

const baseUserData: CreateUserDTO = {
    username: '',
    password: '',
    roles: [],
    preferences: { timezone: '' },
    active: true,
}

// Local copy of user data (for both create and update)
const localUser = ref<UpdateUserDTO | CreateUserDTO>(
    props.user ? JSON.parse(JSON.stringify(props.user)) : { ...baseUserData },
)

// Watcher to define localUser value
watch(
    () => props.modelValue,
    (val) => {
        localVisible.value = val
        if (val && props.user) {
            localUser.value = JSON.parse(JSON.stringify(props.user))
        } else if (val) {
            localUser.value = { ...baseUserData }
        }
    },
    { immediate: true },
)

function close(): void {
    localVisible.value = false
}

function submit(): void {
    if (isEditMode.value) {
        updateOrNewUser.value = {
            username: localUser.value.username,
            roles: localUser.value.roles,
            preferences: localUser.value.preferences,
            active: localUser.value.active,
        }
    } else {
        updateOrNewUser.value = {
            username: localUser.value.username,
            password: localUser.value.password,
            roles: localUser.value.roles,
            preferences: localUser.value.preferences,
            active: true,
        } as CreateUserDTO
    }
    confirmDialogVisible.value = true
}

function confirmSubmit(): void {
    if (!updateOrNewUser.value) return

    if (isEditMode.value) {
        emit('updateUser', updateOrNewUser.value as UpdateUserDTO)
    } else {
        emit('create', updateOrNewUser.value as CreateUserDTO)
    }
    confirmDialogVisible.value = false
    close()
}
</script>

<template>
    <v-dialog v-model="localVisible" max-width="600">
        <v-card>
            <v-card-title>
                <span class="text-h6">{{ isEditMode ? 'Edit User' : 'Create User' }}</span>
            </v-card-title>
            <v-card-text>
                <v-form ref="userForm" lazy-validation>
                    <v-text-field
                        v-model="localUser.username"
                        label="Username"
                        required
                    ></v-text-field>
                    <v-text-field
                        v-if="!isEditMode"
                        v-model="localUser.password"
                        label="Password"
                        type="password"
                        required
                    ></v-text-field>
                    <v-combobox
                        v-model="localUser.roles"
                        :items="allRoles"
                        label="Roles"
                        multiple
                        chips
                    ></v-combobox>
                    <v-text-field
                        v-model="localUser.preferences!.timezone"
                        label="Timezone"
                    ></v-text-field>
                    <v-checkbox
                        v-model="localUser.active"
                        label="Active"
                        color="primary"
                        hide-details
                    ></v-checkbox>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text="" @click="close">Cancel</v-btn>
                <v-btn color="primary" text="" @click="submit"> Save </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>

    <ConfirmDialog
        v-model="confirmDialogVisible"
        :title="`Confirm ${isEditMode ? 'Update' : 'Creation'}`"
        :message="`Are you sure you want to ${isEditMode ? 'update' : 'create'} user`"
        :confirm-text="isEditMode ? 'Update' : 'Create'"
        :confirm-color="isEditMode ? 'primary' : 'success'"
        :item-name="updateOrNewUser?.username"
        @confirm="confirmSubmit"
        @cancel="confirmDialogVisible = false"
    />
</template>
