<template>
  <div v-if="attachments.length" class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
    <div
      v-for="attachment in attachments"
      :key="attachment.name"
      class="group relative flex cursor-pointer flex-col overflow-hidden rounded-lg border border-outline-elevation-2 bg-surface-base transition-shadow hover:shadow-sm"
      @click="openFile(attachment)"
    >
      <div class="relative flex aspect-square w-full items-center justify-center bg-surface-gray-2">
        <img
          v-if="isImage(attachment.file_type)"
          class="h-full w-full object-cover"
          :src="attachment.file_url"
          :alt="attachment.file_name"
        />
        <component
          :is="fileIcon(attachment.file_type)"
          v-else
          class="size-10 text-ink-gray-4"
        />
        
        <div class="absolute right-2 top-2 flex gap-1 opacity-100 transition-opacity group-hover:opacity-100 sm:opacity-0">
          <Button
            :tooltip="
              attachment.is_private ? __('Make Public') : __('Make Private')
            "
            class="!size-7 shadow-sm"
            @click.stop="togglePrivate(attachment.name, attachment.is_private)"
          >
            <template #icon>
              <FeatherIcon
                :name="attachment.is_private ? 'lock' : 'unlock'"
                class="size-3.5 text-ink-gray-7"
              />
            </template>
          </Button>
          <Button
            :tooltip="__('Delete Attachment')"
            class="!size-7 shadow-sm"
            @click.stop="() => deleteAttachment(attachment.name)"
          >
            <template #icon>
              <span
                class="lucide-trash-2 size-3.5 text-ink-gray-7"
                aria-hidden="true"
              />
            </template>
          </Button>
        </div>
      </div>
      
      <div class="flex flex-col border-t border-outline-elevation-2 p-2.5">
        <div class="truncate text-sm font-medium text-ink-gray-9" :title="attachment.file_name">
          {{ attachment.file_name }}
        </div>
        <div class="mt-0.5 flex items-center justify-between text-xs text-ink-gray-5">
          <span>{{ convertSize(attachment.file_size) }}</span>
          <TimelineTimestamp :date="attachment.creation" />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import FileAudioIcon from '@/components/Icons/FileAudioIcon.vue'
import FileTextIcon from '@/components/Icons/FileTextIcon.vue'
import FileVideoIcon from '@/components/Icons/FileVideoIcon.vue'
import { globalStore } from '@/stores/global'
import { call } from 'frappe-ui'
import TimelineTimestamp from '@/components/Activities/TimelineTimestamp.vue'
import { convertSize, isImage } from '@/utils'

defineProps({
  attachments: { type: Array, default: () => [] },
})

const emit = defineEmits(['reload'])

const { $dialog } = globalStore()

function openFile(attachment) {
  window.open(attachment.file_url, '_blank')
}

function togglePrivate(fileName, isPrivate) {
  let changeTo = isPrivate ? __('public') : __('private')
  let title = __('Make attachment {0}', [changeTo])
  let message = __('Are you sure you want to make this attachment {0}?', [
    changeTo,
  ])
  $dialog({
    title,
    message,
    actions: [
      {
        label: __('Make {0}', [changeTo]),
        variant: 'solid',
        onClick: async (close) => {
          await call('frappe.client.set_value', {
            doctype: 'File',
            name: fileName,
            fieldname: {
              is_private: !isPrivate,
            },
          })
          emit('reload')
          close()
        },
      },
    ],
  })
}

function deleteAttachment(fileName) {
  $dialog({
    title: __('Delete Attachment'),
    message: __('Are you sure you want to delete this attachment?'),
    actions: [
      {
        label: __('Delete'),
        variant: 'solid',
        theme: 'red',
        onClick: async (close) => {
          await call('frappe.client.delete', {
            doctype: 'File',
            name: fileName,
          })
          emit('reload')
          close()
        },
      },
    ],
  })
}

function fileIcon(type) {
  if (!type) return FileTextIcon
  let audioExtentions = ['wav', 'mp3', 'ogg', 'flac', 'aac']
  let videoExtentions = ['mp4', 'avi', 'mkv', 'flv', 'mov']
  if (audioExtentions.includes(type.toLowerCase())) {
    return FileAudioIcon
  } else if (videoExtentions.includes(type.toLowerCase())) {
    return FileVideoIcon
  }
  return FileTextIcon
}
</script>
