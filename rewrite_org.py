import re

with open('frontend/src/pages/Organization.vue', 'r') as f:
    content = f.read()

# 1. Update main flex container
content = content.replace('class="flex h-full"', 'class="flex h-full flex-col md:flex-row"')

# 2. Update Resizer v-if
content = content.replace('<Resizer\n      v-if="organization.doc"', '<Resizer\n      v-if="organization.doc && !isMobileView"')

# 3. Add Details tab panel
details_content = """<div v-if="tab?.label == 'Details'" class="flex flex-col flex-1 overflow-y-auto">
        <div class="border-b">
          <FileUploader
            :validateFile="validateIsImageFile"
            @success="changeOrganizationImage"
          >
            <template #default="{ openFileSelector, error }">
              <div class="flex flex-col items-start justify-start gap-4 p-5">
                <div class="flex gap-4 items-center">
                  <div class="group relative h-15.5 w-15.5">
                    <Avatar
                      size="3xl"
                      class="h-15.5 w-15.5"
                      :label="organization.doc.organization_name"
                      :image="organization.doc.organization_logo"
                    />
                    <component
                      :is="organization.doc.organization_logo ? Dropdown : 'div'"
                      v-bind="
                        organization.doc.organization_logo
                          ? {
                              options: [
                                {
                                  icon: 'upload',
                                  label: organization.doc.organization_logo
                                    ? __('Change Image')
                                    : __('Upload Image'),
                                  onClick: openFileSelector,
                                },
                                {
                                  icon: 'trash-2',
                                  label: __('Remove Image'),
                                  onClick: () => changeOrganizationImage(''),
                                },
                              ],
                            }
                          : { onClick: openFileSelector }
                      "
                      class="!absolute bottom-0 left-0 right-0"
                    >
                      <div
                        class="z-1 absolute bottom-0 left-0 right-0 flex h-14 cursor-pointer items-center justify-center rounded-b-full bg-black bg-opacity-40 pt-5 opacity-0 duration-300 ease-in-out group-hover:opacity-100"
                        style="
                          -webkit-clip-path: inset(22px 0 0 0);
                          clip-path: inset(22px 0 0 0);
                        "
                      >
                        <CameraIcon class="h-6 w-6 cursor-pointer text-white" />
                      </div>
                    </component>
                  </div>
                  <div class="flex flex-col gap-2 truncate">
                    <div class="truncate text-3xl-medium text-ink-gray-9">
                      <span>{{ organization.doc.name }}</span>
                    </div>
                    <div
                      v-if="organization.doc.website"
                      class="flex items-center gap-1.5 text-base text-ink-gray-8"
                    >
                      <WebsiteIcon class="size-4" />
                      <span>{{ website(organization.doc.website) }}</span>
                    </div>
                    <ErrorMessage :message="__(error)" />
                  </div>
                </div>
                <div class="flex gap-1.5">
                  <Button
                    v-if="canDelete"
                    :label="__('Delete')"
                    theme="red"
                    size="sm"
                    iconLeft="trash-2"
                    @click="deleteOrganization()"
                  />
                  <Button
                    :tooltip="__('Open Website')"
                    icon="lucide-link"
                    @click="openWebsite"
                  />
                </div>
              </div>
            </template>
          </FileUploader>
        </div>
        <div
          v-if="sections.data"
          class="flex flex-1 flex-col justify-between overflow-hidden"
        >
          <SidePanelLayout
            :sections="sections.data"
            doctype="CRM Organization"
            :docname="organization.doc.name"
            @reload="sections.reload"
            @beforeFieldChange="beforeFieldChange"
          />
        </div>
      </div>
"""
content = content.replace('<template #tab-panel="{ tab }">', '<template #tab-panel="{ tab }">\n      ' + details_content)

# 4. Imports
import_block = """import ErrorPage from '@/components/ErrorPage.vue'
import DetailsIcon from '@/components/Icons/DetailsIcon.vue'
import { isMobileView } from '@/composables/settings'
"""
content = content.replace("import ErrorPage from '@/components/ErrorPage.vue'", import_block)

# 5. Make tabs computed
tabs_original = """const tabs = [
  {
    label: 'Deals',
    icon: DealsIcon,
    count: computed(() => deals.data?.length),
  },
  {
    label: 'Contacts',
    icon: ContactsIcon,
    count: computed(() => contacts.data?.length),
  },
]"""

tabs_new = """const tabs = computed(() => {
  let tabOptions = [
    {
      label: 'Details',
      icon: DetailsIcon,
      condition: () => isMobileView.value,
    },
    {
      label: 'Deals',
      icon: DealsIcon,
      count: computed(() => deals.data?.length),
    },
    {
      label: 'Contacts',
      icon: ContactsIcon,
      count: computed(() => contacts.data?.length),
    },
  ]
  return tabOptions.filter((tab) => (tab.condition ? tab.condition() : true))
})"""
content = content.replace(tabs_original, tabs_new)

with open('frontend/src/pages/Organization.vue', 'w') as f:
    f.write(content)
