import { computed, ref } from 'vue'
import { useWindowSize } from '@vueuse/core'

export const mobileSidebarOpened = ref(false)

const { width } = useWindowSize()
export const isMobileView = computed(() => width.value < 1024)

export const showSettings = ref(false)

export const disableSettingModalOutsideClick = ref(false)

export const activeSettingsPage = ref('')
