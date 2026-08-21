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
    v-model:open="show"
  >
    <template #body-content>
      <div class="flex flex-col gap-4">
        <ErrorMessage v-if="error" :message="error" @remove="error = null" />
        <div v-for="field in fields" :key="field.fieldname">
          <Link
            v-if="field.fieldtype === 'Link'"
            v-model="doc[field.fieldname]"
            :doctype="field.options"
            :label="__(field.label)"
            :onCreate="
              field.options === 'User'
                ? (value, close) => createNewUser(value, close, field)
                : null
            "
          />
          <FormControl
            v-else-if="field.fieldtype === 'Select'"
            :type="'select'"
            :label="__(field.label)"
            :reqd="field.reqd"
            :options="field.options.map(o => ({ label: o, value: o }))"
            v-model="doc[field.fieldname]"
          />
          <FormControl
            v-else
            :type="field.fieldtype === 'Check' ? 'checkbox' : field.fieldtype.toLowerCase()"
            :label="__(field.label)"
            :reqd="field.reqd"
            v-model="doc[field.fieldname]"
          />
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ErrorMessage, Dialog, FormControl, call } from 'frappe-ui'
import Link from '@/components/Controls/Link.vue'
import { createDocument } from '@/composables/document'
import { usersStore } from '@/stores/users'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  options: { type: Object, default: () => ({}) },
})
const emit = defineEmits(['update:modelValue', 'success'])

const show = ref(props.modelValue)

watch(() => show.value, (val) => {
  emit('update:modelValue', val)
})

const isSubmitting = ref(false)
const error = ref(null)

const doc = reactive({
  user: '',
  full_name: '',
  role_type: '',
  daily_capacity: 10,
  is_active: true
})

const fields = [
  { fieldname: 'user', fieldtype: 'Link', label: 'User', options: 'User', reqd: 1 },
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
    usersStore().users.reload()
    show.value = false
  } catch (err) {
    error.value = err.message || err
  } finally {
    isSubmitting.value = false
  }
}

function createNewUser(value, close, field) {
  createDocument('User', { first_name: value, email: value }, close, (newDoc) => {
    if (newDoc) {
      doc[field.fieldname] = newDoc.name
    }
  })
}
</script>
