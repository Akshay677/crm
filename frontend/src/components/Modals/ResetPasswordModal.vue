<template>
  <Dialog
    :options="{
      title: __('Reset Password'),
      actions: [
        {
          label: __('Update Password'),
          variant: 'solid',
          onClick: submit,
          loading: isSubmitting,
          disabled: !newPassword
        },
      ],
    }"
    v-model:open="show"
  >
    <template #body-content>
      <div class="flex flex-col gap-4">
        <ErrorMessage v-if="error" :message="error" @remove="error = null" />
        <Password
          :label="__('New Password')"
          :required="1"
          v-model="newPassword"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ErrorMessage, Dialog, call, toast } from 'frappe-ui'
import Password from '@/components/Controls/Password.vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  users: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:modelValue', 'reload'])

const show = ref(props.modelValue)

watch(
  () => show.value,
  (val) => {
    emit('update:modelValue', val)
  },
)

const isSubmitting = ref(false)
const error = ref(null)
const newPassword = ref('')

async function submit() {
  isSubmitting.value = true
  error.value = null

  if (!newPassword.value) {
    error.value = __('Password is required')
    isSubmitting.value = false
    return
  }

  try {
    for (const user of props.users) {
      await call('crm.api.user.reset_user_password', {
        user: user,
        new_password: newPassword.value,
      })
    }
    
    toast.success(__('Password changed successfully'))
    emit('reload')
    show.value = false
  } catch (err) {
    error.value = err.message || err
  } finally {
    isSubmitting.value = false
  }
}
</script>
