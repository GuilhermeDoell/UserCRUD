<script lang="ts" setup>
import type { User } from '@/userDTO'
import { computed } from 'vue'
import ConfirmDialog from './ConfirmDialog.vue'

interface Props {
    modelValue: boolean
    user: User | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void
    (e: 'confirm'): void
}>()

const dialogVisible = computed({
    get: () => props.modelValue,
    set: (value: boolean) => emit('update:modelValue', value)
})
</script>

<template>
    <ConfirmDialog
        :model-value="dialogVisible"
        title="Confirm Delete"
        message="Are you sure you want to delete user"
        confirm-text="Delete"
        confirm-color="error"
        :item-name="user?.username"
        @update:model-value="(val) => emit('update:modelValue', val)"
        @confirm="emit('confirm')"
    />
</template>
