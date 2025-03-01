<script lang="ts" setup>
import { computed } from 'vue'

interface Props {
    modelValue: boolean
    title: string
    message: string
    confirmText?: string
    cancelText?: string
    confirmColor?: string
    itemName?: string
}

interface Emits {
    (e: 'update:modelValue', value: boolean): void
    (e: 'confirm'): void
    (e: 'cancel'): void
}

const props = withDefaults(defineProps<Props>(), {
    confirmText: 'Confirm',
    cancelText: 'Cancel',
    confirmColor: 'primary',
    itemName: '',
})

const emit = defineEmits<Emits>()

const dialogModel = computed({
    get: () => props.modelValue,
    set: (value: boolean) => emit('update:modelValue', value),
})

function cancel() {
    emit('cancel')
    emit('update:modelValue', false)
}

function confirm() {
    emit('confirm')
    emit('update:modelValue', false)
}
</script>

<template>
    <v-dialog v-model="dialogModel" max-width="500">
        <v-card>
            <v-card-title class="headline">{{ title }}</v-card-title>
            <v-card-text>
                {{ message }}
                <strong v-if="itemName">{{ itemName }}</strong
                >?
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text="" @click="cancel">{{ cancelText }}</v-btn>
                <v-btn :color="confirmColor" text="" @click="confirm">{{ confirmText }}</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
