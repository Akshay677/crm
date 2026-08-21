<template>
  <FormControl
    v-if="filter.fieldtype == 'Check'"
    v-model="filter.value"
    :label="filter.label"
    type="checkbox"
    @change.stop="updateFilter(filter, $event.target.checked)"
  />
  <FormControl
    v-else-if="filter.fieldtype === 'Select'"
    v-model="filter.value"
    class="form-control cursor-pointer [&_select]:cursor-pointer"
    type="select"
    :options="formattedOptions"
    :placeholder="filter.label"
    side="bottom"
    :offset="4"
    @update:modelValue="updateFilter(filter, $event)"
  />
  <Link
    v-else-if="filter.fieldtype === 'Link'"
    :value="filter.value"
    :doctype="filter.options"
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
import { FormControl, DatePicker, DateTimePicker } from 'frappe-ui'
import { useDebounceFn } from '@vueuse/core'
import { reactive, watch, computed } from 'vue'

const props = defineProps({
  filter: { type: Object, required: true },
})

const filter = reactive(props.filter)

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
      
    // Add empty option so users can clear the select filter
    if (props.filter.fieldtype === 'Select') {
      options.unshift({ label: 'Clear', value: '' })
    }
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
