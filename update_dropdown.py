import re

with open('frontend/src/components/UserDropdown.vue', 'r') as f:
    content = f.read()

# Import mobileSidebarOpened
import_line = "import { showSettings, isMobileView } from '@/composables/settings'"
new_import = "import { showSettings, isMobileView, mobileSidebarOpened } from '@/composables/settings'"
content = content.replace(import_line, new_import)

# Update onClick for settings
old_click = """        onClick: () => {
          showSettings.value = true
        },"""

new_click = """        onClick: () => {
          showSettings.value = true
          if (isMobileView.value) mobileSidebarOpened.value = false
        },"""
content = content.replace(old_click, new_click)

with open('frontend/src/components/UserDropdown.vue', 'w') as f:
    f.write(content)
