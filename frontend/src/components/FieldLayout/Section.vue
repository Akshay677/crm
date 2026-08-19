<template>
  <div
    v-if="!section.hidden"
    class="section"
    :class="[
      section.hideBorder
        ? 'pt-3'
        : 'border-t border-outline-elevation-2 mt-4 pt-4',
    ]"
  >
    <CollapsibleSection
      class="grid gap-4 text-lg-medium"
      :class="[
        hasTabs ? 'px-3 sm:px-5' : '',
        getColumnsGridClass(section.columns),
      ]"
      :labelClass="['text-base sm:text-lg font-medium', { 'px-3 sm:px-5': hasTabs }]"
      :label="section.label"
      :hideLabel="section.hideLabel || !section.label"
      :opened="section.opened"
      :collapsible="section.collapsible"
      collapseIconPosition="right"
    >
      <template v-for="column in section.columns" :key="column.name">
        <Column
          :class="{ 'mt-3': section.label && !section.hideLabel }"
          :column="column"
          :isSingleColumn="section.columns?.length <= 1"
          :data-name="column.name"
        />
      </template>
    </CollapsibleSection>
  </div>
</template>
<script setup>
import CollapsibleSection from '@/components/CollapsibleSection.vue'
import Column from '@/components/FieldLayout/Column.vue'
import { inject } from 'vue'

defineProps({
  section: { type: Object, required: true },
})

const hasTabs = inject('hasTabs')

function getColumnsGridClass(columns) {
  const count = columns?.length || 1
  if (count <= 1) return 'grid-cols-1'
  if (count === 2) return 'grid-cols-1 sm:grid-cols-2'
  return 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
}
</script>
