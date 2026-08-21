<template>
  <Dialog
    :options="{
      title: __('Create Team Profile'),
      actions: [
        {
          label: __('Create'),
          variant: 'solid',
          onClick: submit,
          loading: isSubmitting,
        },
      ],
    }"
    v-model="show"
  >
    <template #body-content>
      <div class="flex flex-col gap-4">
        <ErrorMessage v-if="error" :message="error" @remove="error = null" />
        <FormControl
          v-for="field in fields"
          :key="field.fieldname"
          :type="field.fieldtype"
          :label="__(field.label)"
          :reqd="field.reqd"
          :options="field.options"
          v-model="doc[field.fieldname]"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ErrorMessage, Dialog, FormControl, call } from 'frappe-ui'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  options: { type: Object, default: () => ({}) },
})
const emit = defineEmits(['update:modelValue', 'success'])

const show = ref(props.modelValue)
const isSubmitting = ref(false)
const error = ref(null)

const doc = reactive({
  user: '',
  full_name: '',
  role_type: '',
  daily_capacity: 10,
  is_active: 1
})

const fields = [
  { fieldname: 'user', fieldtype: 'Link', label: 'User', options: 'User', reqd: 1 },
  { fieldname: 'full_name', fieldtype: 'Data', label: 'Full Name' },
  { fieldname: 'role_type', fieldtype: 'Select', label: 'Role', options: ['Management', 'Project Manager', 'Editor', 'Executor', 'Ops', 'Finance'] },
  { fieldname: 'daily_capacity', fieldtype: 'Int', label: 'Daily Capacity' },
  { fieldname: 'is_active', fieldtype: 'Check', label: 'Active' },
]

async function submit() {
  isSubmitting.value = true
  error.value = null
  try {
    const res = await call('frappe.client.insert', {
      doc: {
        doctype: 'Team Profile',
        ...doc
      }
    })
    emit('success', res)
    props.options?.afterInsert?.(res)
    show.value = false
  } catch (err) {
    error.value = err.message || err
  } finally {
    isSubmitting.value = false
  }
}
</script>
