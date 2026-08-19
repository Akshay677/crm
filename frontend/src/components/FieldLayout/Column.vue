<template>
  <div class="column flex flex-col gap-4 min-w-0 flex-1">
    <div
      v-if="column.label && !column.hideLabel"
      class="text-ink-gray-9 max-w-fit text-base"
    >
      {{ column.label }}
    </div>
    <div :class="gridClass">
      <template v-for="field in column.fields" :key="field.fieldname">
        <Field
          :field="field"
          :data-name="field.fieldname"
          :class="isFullWidth(field) ? 'col-span-1 md:col-span-2' : 'col-span-1'"
        />
      </template>
    </div>
  </div>
</template>
<script setup>
import Field from '@/components/FieldLayout/Field.vue'
import { computed } from 'vue'

const props = defineProps({
  column: { type: Object, required: true },
  isSingleColumn: { type: Boolean, default: true },
})

const gridClass = computed(() => {
  if (props.isSingleColumn) {
    return 'grid grid-cols-1 md:grid-cols-2 gap-4'
  }
  return 'flex flex-col gap-4'
})

function isFullWidth(field) {
  return [
    'Table',
    'Text Editor',
    'Text',
    'Small Text',
    'Long Text',
    'Code',
    'HTML',
    'JSON',
  ].includes(field.fieldtype)
}
</script>
