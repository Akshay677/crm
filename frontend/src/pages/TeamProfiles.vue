<template>
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" routeName="Team Profiles" />
    </template>
    <template #right-header>
      <CustomActions
        v-if="teamProfilesListView?.customListActions"
        :actions="teamProfilesListView.customListActions"
      />
      <Button
        variant="solid"
        :label="__('Create')"
        iconLeft="plus"
        @click="showTeamProfileModal = true"
      />
    </template>
  </LayoutHeader>
  <ViewControls
    ref="viewControls"
    v-model="teamProfiles"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="Team Profile"
  />
  <TeamProfilesListView
    v-if="teamProfiles.data && rows.length"
    ref="teamProfilesListView"
    v-model="teamProfiles.data.page_length_count"
    v-model:list="teamProfiles"
    :rows="rows"
    :columns="columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: teamProfiles.data.row_count,
      totalCount: teamProfiles.data.total_count,
    }"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
    @applyFilter="(data) => viewControls.applyFilter(data)"
    @applyLikeFilter="(data) => viewControls.applyLikeFilter(data)"
    @likeDoc="(data) => viewControls.likeDoc(data)"
    @selectionsChanged="
      (selections) => viewControls.updateSelections(selections)
    "
  />
  <EmptyState
    v-else-if="teamProfiles.data && !rows.length"
    name="Team Profiles"
    :icon="OrganizationsIcon"
  />
  <TeamProfileModal
    v-if="showTeamProfileModal"
    v-model="showTeamProfileModal"
    @success="() => viewControls?.reload()"
  />
</template>
<script setup>
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import CustomActions from '@/components/CustomActions.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import TeamProfileModal from '@/components/Modals/TeamProfileModal.vue'
import TeamProfilesListView from '@/components/ListViews/TeamProfilesListView.vue'
import ViewControls from '@/components/ViewControls.vue'
import { getMeta } from '@/stores/meta'
import { formatDate, website } from '@/utils'
import { timestampCell } from '@/composables/useTimelinePreferences'
import { ref, computed } from 'vue'
import EmptyState from '../components/ListViews/EmptyState.vue'

const { getFormattedPercent, getFormattedFloat, getFormattedCurrency } =
  getMeta('Team Profile')

const teamProfilesListView = ref(null)
const showTeamProfileModal = ref(false)

// teamProfiles data is loaded in the ViewControls component
const teamProfiles = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

const rows = computed(() => {
  if (
    !teamProfiles.value?.data?.data ||
    !['list', 'group_by'].includes(teamProfiles.value.data.view_type)
  )
    return []
  return teamProfiles.value?.data.data.map((teamProfile) => {
    let _rows = { name: teamProfile.name }
    teamProfiles.value?.data.rows.forEach((row) => {
      _rows[row] = teamProfile[row]

      let fieldType = teamProfiles.value?.data.columns?.find(
        (col) => (col.key || col.value) == row,
      )?.type

      if (
        fieldType &&
        ['Date', 'Datetime'].includes(fieldType) &&
        !['modified', 'creation'].includes(row)
      ) {
        _rows[row] = formatDate(
          teamProfile[row],
          '',
          true,
          fieldType == 'Datetime',
        )
      }

      if (fieldType && fieldType == 'Currency') {
        _rows[row] = getFormattedCurrency(row, teamProfile)
      }

      if (fieldType && fieldType == 'Float') {
        _rows[row] = getFormattedFloat(row, teamProfile)
      }

      if (fieldType && fieldType == 'Percent') {
        _rows[row] = getFormattedPercent(row, teamProfile)
      }

      if (row === 'teamProfile_name') {
        _rows[row] = {
          label: teamProfile.teamProfile_name,
          logo: teamProfile.teamProfile_logo,
        }
      } else if (row === 'website') {
        _rows[row] = website(teamProfile.website)
      } else if (['modified', 'creation'].includes(row)) {
        _rows[row] = timestampCell(teamProfile[row])
      }
    })
    return _rows
  })
})

const columns = computed(() => {
  let _columns = teamProfiles.value?.data?.columns || []

  // Set align right for last column
  if (_columns.length) {
    _columns = _columns.map((col, index) => {
      if (index === _columns.length - 1) {
        return { ...col, align: 'right' }
      }
      return col
    })
  }

  return _columns
})
</script>
