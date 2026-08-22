import re

with open('frontend/src/components/Settings/Settings.vue', 'r') as f:
    content = f.read()

# Replace the layout logic
old_layout = """    <template #body>
      <div class="flex h-[calc(100vh_-_8rem)] bg-surface-gray-1">
        <div
          class="flex flex-col m-1 rounded-l-lg w-56 shrink-0 bg-surface-gray-1 overflow-y-auto"
        >"""

new_layout = """    <template #body>
      <div class="flex flex-col md:flex-row h-full max-h-[calc(100vh_-_4rem)] md:h-[calc(100vh_-_8rem)] bg-surface-gray-1">
        <div
          v-if="!isMobileView || showMobileMenu"
          class="flex flex-col md:m-1 md:rounded-l-lg w-full md:w-56 shrink-0 bg-surface-gray-1 overflow-y-auto"
        >"""
content = content.replace(old_layout, new_layout)

old_sidebar_click = """@click="activeSettingsPage = item.label\""""
new_sidebar_click = """@click="activeSettingsPage = item.label; showMobileMenu = false\""""
content = content.replace(old_sidebar_click, new_sidebar_click)

old_content_panel = """        <div
          class="flex flex-col flex-1 overflow-y-auto bg-surface-elevation-2"
        >
          <component :is="activeTab.component" v-if="activeTab" />
        </div>"""

new_content_panel = """        <div
          v-if="!isMobileView || !showMobileMenu"
          class="flex flex-col flex-1 overflow-y-auto bg-surface-elevation-2 relative"
        >
          <div v-if="isMobileView" class="sticky top-0 bg-surface-elevation-2 z-10 flex items-center p-3 border-b shrink-0">
            <Button icon="chevron-left" @click="showMobileMenu = true" variant="ghost" class="mr-2" />
            <span class="font-medium">{{ __(activeTab?.label) }}</span>
          </div>
          <component :is="activeTab.component" v-if="activeTab" />
        </div>"""
content = content.replace(old_content_panel, new_content_panel)

# Imports
import_block = """import { isMobileView } from '@/composables/settings'
import { Dialog, Avatar, SidebarItem, Button } from 'frappe-ui'"""
content = content.replace("import { Dialog, Avatar, SidebarItem } from 'frappe-ui'", import_block)

# Show mobile menu ref
script_setup = """const { isManager, getUser } = usersStore()

const showMobileMenu = ref(true)"""
content = content.replace("const { isManager, getUser } = usersStore()", script_setup)

with open('frontend/src/components/Settings/Settings.vue', 'w') as f:
    f.write(content)
