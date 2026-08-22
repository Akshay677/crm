import re

with open('frontend/src/components/Layouts/AppSidebar.vue', 'r') as f:
    sidebar = f.read()

# Remove Settings from AppSidebar
sidebar = sidebar.replace('<Settings />\n', '')
sidebar = sidebar.replace("import Settings from '@/components/Settings/Settings.vue'\n", "")
with open('frontend/src/components/Layouts/AppSidebar.vue', 'w') as f:
    f.write(sidebar)

with open('frontend/src/components/Modals/GlobalModals.vue', 'r') as f:
    modals = f.read()

# Add Settings to GlobalModals
modals = modals.replace('</template>', '  <Settings />\n</template>')
modals = modals.replace("import AboutModal from '@/components/Modals/AboutModal.vue'", "import AboutModal from '@/components/Modals/AboutModal.vue'\nimport Settings from '@/components/Settings/Settings.vue'")

with open('frontend/src/components/Modals/GlobalModals.vue', 'w') as f:
    f.write(modals)

