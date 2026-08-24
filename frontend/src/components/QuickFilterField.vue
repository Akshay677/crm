<template>
  <FormControl
    v-if="filter.fieldtype == 'Check'"
    v-model="filter.value"
    :label="filter.label"
    type="checkbox"
    @change.stop="updateFilter(filter, $event.target.checked)"
  />
  <Autocomplete
    v-else-if="filter.fieldtype === 'Select'"
    :modelValue="filter.value ? { label: filter.value, value: filter.value } : null"
    :options="formattedOptions"
    :placeholder="filter.label"
    size="sm"
    @update:modelValue="(val) => updateFilter(filter, val?.value || '')"
  >
    <template #footer="{ togglePopover }">
      <div>
        <Button
          variant="ghost"
          class="w-full !justify-start"
          :label="__('Clear')"
          iconLeft="x"
          @click="
            () => {
              updateFilter(filter, '')
              togglePopover()
            }
          "
        />
      </div>
    </template>
  </Autocomplete>
  <Link
    v-else-if="filter.fieldtype === 'Link'"
    :value="filter.value"
    :doctype="filter.options"
    :filters="linkFilters"
    :placeholder="filter.label"
    @change="(data) => updateFilter(filter, data)"
  />
  <component
    :is="filter.fieldtype === 'Date' ? DatePicker : DateTimePicker"
    v-else-if="['Date', 'Datetime'].includes(filter.fieldtype)"
    class="border-none"
    :value="filter.value"
    :placeholder="filter.label"
    @change="(v) => updateFilter(filter, v)"
  />
  <FormControl
    v-else
    v-model="filter.value"
    type="text"
    :placeholder="filter.label"
    @input.stop="debouncedFn(filter, $event.target.value)"
  />
</template>
<script setup>
import Link from '@/components/Controls/Link.vue'
import { usersStore } from '@/stores/users'
import {
  FormControl,
  DatePicker,
  DateTimePicker,
  Autocomplete,
  Button,
} from 'frappe-ui'
import { useDebounceFn } from '@vueuse/core'
import { reactive, watch, computed } from 'vue'

const props = defineProps({
  filter: { type: Object, required: true },
})

const { users } = usersStore()
const filter = reactive(props.filter)

const linkFilters = computed(() => {
  if (props.filter.fieldtype === 'Link' && props.filter.options === 'User') {
    let allowedUsers = users.data?.crmUsers?.map((user) => user.name) || []
    if (
      props.filter.fieldname === 'project_manager' ||
      props.filter.fieldname === 'custom_project_manager'
    ) {
      allowedUsers =
        users.data?.crmUsers
          ?.filter(
            (u) =>
              u.roles?.includes('Project Manager') ||
              u.role === 'Project Manager',
          )
          .map((u) => u.name) || []
    } else if (
      props.filter.fieldname === 'editor' ||
      props.filter.fieldname === 'custom_editor'
    ) {
      allowedUsers =
        users.data?.crmUsers
          ?.filter((u) => u.roles?.includes('Editor') || u.role === 'Editor')
          .map((u) => u.name) || []
    } else if (
      props.filter.fieldname === 'executor' ||
      props.filter.fieldname === 'custom_executor'
    ) {
      allowedUsers =
        users.data?.crmUsers
          ?.filter(
            (u) =>
              u.roles?.includes('Executor') ||
              u.role === 'Executor',
          )
          .map((u) => u.name) || []
    }
    return {
      name: ['in', allowedUsers],
      ignore_user_type: 1,
    }
  }
  return []
})

const formattedOptions = computed(() => {
  let opts = props.filter.options
  if (!opts) return []

  if (typeof opts === 'string') {
    opts = opts.split('\n')
  }

  if (Array.isArray(opts)) {
    let options = opts
      .map((opt) => {
        if (typeof opt === 'string') {
          const trimmed = opt.trim()
          return trimmed ? { label: trimmed, value: trimmed } : null
        } else if (opt && typeof opt === 'object') {
          const label = (opt.label ?? opt.value ?? '').toString().trim()
          const value = opt.value ?? opt.label ?? ''
          return label !== '' || value !== ''
            ? { ...opt, label: label || value, value }
            : null
        }
        return null
      })
      .filter(Boolean)
      
    return options
  }
  return opts
})

const emit = defineEmits(['applyQuickFilter'])

watch(
  () => props.filter,
  (newFilter) => Object.assign(filter, newFilter),
  { deep: true },
)

const debouncedFn = useDebounceFn((f, value) => {
  emit('applyQuickFilter', f, value)
}, 500)

function updateFilter(f, value) {
  emit('applyQuickFilter', f, value)
}
</script>
