<template>
  <Dialog v-model:open="show" :size="'4xl'">
    <template #body>
      <div class="bg-surface-elevation-1 p-4 sm:p-6 overflow-x-hidden">
        <!-- Modal Header -->
        <div class="flex items-start justify-between pb-3 sm:pb-4 border-b border-outline-gray-1">
          <div class="flex items-center gap-2.5 sm:gap-3">
            <div class="flex items-center justify-center size-8 sm:size-10 rounded-xl bg-purple-50 text-purple-600 dark:bg-purple-950/40 dark:text-purple-400 shrink-0">
              <LucideBriefcase class="size-4 sm:size-5" />
            </div>
            <div>
              <h3 class="text-base sm:text-2xl font-bold text-ink-gray-9">
                {{ __('Team Capacity & Bandwidth') }}
              </h3>
              <p class="text-[11px] sm:text-sm text-ink-gray-5">
                {{ __('Workload scores, available bandwidth, and workflow bottlenecks') }}
              </p>
            </div>
          </div>
          <Button variant="ghost" icon="lucide-x" class="w-8" @click="show = false" />
        </div>

        <div class="max-h-[72vh] overflow-y-auto overflow-x-hidden py-4 space-y-6">
          <!-- Top 3 Insight Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5">
            <!-- 1. Who can take next campaign -->
            <div class="p-3.5 rounded-xl border border-outline-gray-1 bg-surface-base flex flex-col gap-2">
              <div class="flex items-center gap-2 text-xs font-semibold text-green-700 dark:text-green-400 uppercase tracking-wide">
                <LucideUserCheck class="size-4" />
                <span>{{ __('Who Takes Next Campaign') }}</span>
              </div>
              <div
                v-if="whoCanTake.data?.length"
                class="space-y-1 max-h-[76px] overflow-y-auto pr-1"
              >
                <div
                  v-for="person in whoCanTake.data"
                  :key="person.user"
                  class="flex items-center justify-between text-xs py-0.5"
                >
                  <span class="font-medium text-ink-gray-8 truncate">
                    <span class="text-ink-gray-5">{{ person.role_type }}:</span> {{ person.full_name }}
                  </span>
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-green-50 text-green-700 font-bold shrink-0">
                    {{ person.band }}
                  </span>
                </div>
              </div>
              <div v-else class="text-xs text-ink-gray-5">
                {{ __('No available team members found') }}
              </div>
            </div>

            <!-- 2. Where work is stuck (Top Stuck Campaigns) -->
            <div class="p-3.5 rounded-xl border border-outline-gray-1 bg-surface-base flex flex-col gap-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2 text-xs font-semibold text-amber-700 dark:text-amber-400 uppercase tracking-wide">
                  <LucideClock class="size-4" />
                  <span>{{ __('Where Work Is Stuck') }}</span>
                </div>
                <button
                  class="text-[10px] text-amber-600 dark:text-amber-400 hover:underline font-semibold"
                  @click="activeView = activeView === 'stuck' ? 'capacity' : 'stuck'"
                >
                  {{ activeView === 'stuck' ? __('View Capacity') : __('View All') }}
                </button>
              </div>
              <div v-if="stuckCampaigns.data?.length" class="space-y-1">
                <div
                  v-for="cmp in stuckCampaigns.data.slice(0, 2)"
                  :key="cmp.name"
                  class="flex items-center justify-between text-xs cursor-pointer hover:bg-surface-gray-2 p-1 rounded transition-colors group"
                  @click="openCampaign(cmp.name)"
                >
                  <div class="flex flex-col min-w-0 pr-1">
                    <span class="font-semibold text-ink-gray-9 truncate max-w-[125px] group-hover:text-primary-600">
                      {{ cmp.song }}
                    </span>
                    <span class="text-[10px] text-ink-gray-5">
                      {{ cmp.stage }} • {{ cmp.responsible }}
                    </span>
                  </div>
                  <span
                    class="px-1.5 py-0.5 rounded text-[10px] bg-amber-50 text-amber-700 font-bold shrink-0"
                    :title="`${cmp.hours_in_stage} total hours in ${cmp.stage}`"
                  >
                    {{ formatTimeInStage(cmp.hours_in_stage) }} in stage
                  </span>
                </div>
              </div>
              <div v-else-if="timeInStage.data?.length" class="space-y-1">
                <div
                  v-for="stg in timeInStage.data.slice(0, 2)"
                  :key="stg.stage"
                  class="flex items-center justify-between text-xs"
                >
                  <span class="font-medium text-ink-gray-8 truncate max-w-[120px]">{{ stg.stage }}</span>
                  <span class="text-ink-gray-5 text-[11px] font-medium">
                    avg {{ stg.avg_hours }} hrs
                  </span>
                </div>
              </div>
              <div v-else class="text-xs text-ink-gray-5">
                {{ __('No stage bottleneck data yet') }}
              </div>
            </div>

            <!-- 3. Rework Leaderboard (Edits bouncing) -->
            <div class="p-3.5 rounded-xl border border-outline-gray-1 bg-surface-base flex flex-col gap-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2 text-xs font-semibold text-red-700 dark:text-red-400 uppercase tracking-wide">
                  <LucideAlertTriangle class="size-4" />
                  <span>{{ __('Rework Leaderboard') }}</span>
                </div>
              </div>
              <div v-if="reworkLeaderboard.data?.by_campaign?.length" class="space-y-1">
                <div
                  v-for="cmp in reworkLeaderboard.data.by_campaign.slice(0, 2)"
                  :key="cmp.name || cmp.campaign"
                  class="flex items-center justify-between text-xs cursor-pointer hover:bg-surface-gray-2 p-1 rounded transition-colors group"
                  @click="openCampaign(cmp.name || cmp.campaign)"
                >
                  <span class="font-medium text-ink-gray-8 truncate max-w-[120px] group-hover:text-primary-600">{{ cmp.song || cmp.campaign }}</span>
                  <span class="px-1.5 py-0.5 rounded text-[11px] bg-red-50 text-red-700 font-semibold shrink-0">
                    {{ cmp.rework_rounds }} {{ __('rounds') }}
                  </span>
                </div>
              </div>
              <div v-else class="text-xs text-ink-gray-5">
                {{ __('No rework rounds recorded') }}
              </div>
            </div>
          </div>

          <!-- Navigation / Mode Tabs -->
          <div class="flex items-center justify-between flex-wrap gap-2 pt-2">
            <div class="flex items-center gap-1.5 bg-surface-gray-2 p-1 rounded-lg">
              <button
                class="px-3 py-1 text-xs font-medium rounded-md transition-all"
                :class="activeView === 'capacity' ? 'bg-surface-base text-ink-gray-9 shadow-sm' : 'text-ink-gray-5 hover:text-ink-gray-8'"
                @click="activeView = 'capacity'"
              >
                {{ __('Team Capacity Table') }}
              </button>
              <button
                class="px-3 py-1 text-xs font-medium rounded-md transition-all flex items-center gap-1"
                :class="activeView === 'stuck' ? 'bg-surface-base text-ink-gray-9 shadow-sm' : 'text-ink-gray-5 hover:text-ink-gray-8'"
                @click="activeView = 'stuck'"
              >
                <span>{{ __('Stuck Campaigns List') }}</span>
                <span v-if="stuckCampaigns.data?.length" class="px-1.5 py-0.2 rounded-full text-[10px] bg-amber-100 text-amber-800 font-bold">
                  {{ stuckCampaigns.data.length }}
                </span>
              </button>
            </div>

            <!-- Role Filter Tabs (Only in capacity view) -->
            <div v-if="activeView === 'capacity'" class="flex items-center gap-1.5 bg-surface-gray-2 p-1 rounded-lg">
              <button
                v-for="role in ['All', 'Project Manager', 'Editor', 'Executor']"
                :key="role"
                class="px-2.5 py-1 text-xs font-medium rounded-md transition-all"
                :class="selectedRole === role ? 'bg-surface-base text-ink-gray-9 shadow-sm' : 'text-ink-gray-5 hover:text-ink-gray-8'"
                @click="selectedRole = role"
              >
                {{ __(role) }}
              </button>
            </div>
          </div>

          <!-- VIEW 1: Team Capacity Table -->
          <div v-if="activeView === 'capacity'" class="border border-outline-gray-1 rounded-xl overflow-hidden bg-surface-base">
            <div v-if="teamCapacity.loading" class="p-8 text-center text-sm text-ink-gray-5">
              {{ __('Loading capacity data...') }}
            </div>
            <div v-else-if="!filteredCapacity.length" class="p-8 text-center text-sm text-ink-gray-5">
              {{ __('No team profiles found for this role.') }}
            </div>
            <div v-else class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-surface-gray-2 text-ink-gray-6 border-b border-outline-gray-1 font-semibold uppercase tracking-wider text-[11px]">
                  <tr>
                    <th class="py-3 px-4">{{ __('Team Member') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Active Campaigns') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Deliverables (Done / Total)') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Pending') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Urgent (48h)') }}</th>
                    <th class="py-3 px-3">{{ __('Next Deadline') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Daily Cap') }}</th>
                    <th class="py-3 px-4 text-center">{{ __('Workload Status') }}</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-outline-gray-1">
                  <tr
                    v-for="row in filteredCapacity"
                    :key="row.user"
                    class="hover:bg-surface-gray-1 transition-colors"
                  >
                    <!-- Name & Role -->
                    <td class="py-3 px-4">
                      <div class="font-semibold text-ink-gray-9 text-sm">{{ row.full_name }}</div>
                      <div class="text-[11px] text-ink-gray-5">{{ row.role_type || __('Team Member') }}</div>
                    </td>

                    <!-- Active Campaigns -->
                    <td class="py-3 px-3 text-center font-medium text-ink-gray-8">
                      {{ row.active_campaigns }}
                    </td>

                    <!-- Deliverables (Done / Total) -->
                    <td class="py-3 px-3 text-center text-ink-gray-8">
                      <span class="font-semibold text-green-600">{{ row.completed }}</span>
                      <span class="text-ink-gray-4"> / {{ row.assigned }}</span>
                    </td>

                    <!-- Pending -->
                    <td class="py-3 px-3 text-center font-semibold text-ink-gray-9">
                      {{ row.pending }}
                    </td>

                    <!-- Urgent 48h -->
                    <td class="py-3 px-3 text-center">
                      <span
                        v-if="row.urgent > 0"
                        class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-bold bg-red-50 text-red-600 dark:bg-red-950/40"
                      >
                        <LucideFlame class="size-3 text-red-500 shrink-0" />
                        <span>{{ row.urgent }}</span>
                      </span>
                      <span v-else class="text-ink-gray-4">-</span>
                    </td>

                    <!-- Next Deadline -->
                    <td class="py-3 px-3 text-ink-gray-7 whitespace-nowrap">
                      {{ row.next_deadline || __('None') }}
                    </td>

                    <!-- Daily Capacity -->
                    <td class="py-3 px-3 text-center text-ink-gray-6">
                      {{ row.daily_capacity }}/day
                    </td>

                    <!-- Workload Status Band -->
                    <td class="py-3 px-4 text-center">
                      <div class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-semibold" :class="getBandBadgeClass(row.band)">
                        <span class="size-1.5 rounded-full" :class="getBandDotClass(row.band)"></span>
                        <span>{{ __(row.band) }}</span>
                        <span class="text-[10px] opacity-75 font-normal">({{ row.workload_score }})</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- VIEW 2: Stuck Campaigns List Table -->
          <div v-else class="border border-outline-gray-1 rounded-xl overflow-hidden bg-surface-base">
            <div v-if="stuckCampaigns.loading" class="p-8 text-center text-sm text-ink-gray-5">
              {{ __('Loading stuck campaigns...') }}
            </div>
            <div v-else-if="!stuckCampaigns.data?.length" class="p-8 text-center text-sm text-ink-gray-5">
              {{ __('No stuck campaigns! Everything is moving smoothly.') }}
            </div>
            <div v-else class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-surface-gray-2 text-ink-gray-6 border-b border-outline-gray-1 font-semibold uppercase tracking-wider text-[11px]">
                  <tr>
                    <th class="py-3 px-4">{{ __('Campaign / Song') }}</th>
                    <th class="py-3 px-3">{{ __('Current Stage') }}</th>
                    <th class="py-3 px-3">{{ __('Responsible Person') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Time in Stage') }}</th>
                    <th class="py-3 px-3">{{ __('Campaign Deadline') }}</th>
                    <th class="py-3 px-4 text-right">{{ __('Action') }}</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-outline-gray-1">
                  <tr
                    v-for="cmp in stuckCampaigns.data"
                    :key="cmp.name"
                    class="hover:bg-surface-gray-1 transition-colors cursor-pointer"
                    @click="openCampaign(cmp.name)"
                  >
                    <!-- Campaign Song -->
                    <td class="py-3 px-4 font-semibold text-ink-gray-9 text-sm">
                      <div class="hover:text-primary-600 transition-colors flex items-center gap-1.5">
                        <span>{{ cmp.song }}</span>
                        <span class="text-[11px] text-ink-gray-4 font-normal">({{ cmp.name }})</span>
                      </div>
                    </td>

                    <!-- Stage -->
                    <td class="py-3 px-3">
                      <span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-surface-gray-3 text-ink-gray-8">
                        {{ cmp.stage }}
                      </span>
                    </td>

                    <!-- Responsible Person -->
                    <td class="py-3 px-3 font-medium text-ink-gray-8">
                      {{ cmp.responsible }}
                    </td>

                    <!-- Time in Stage -->
                    <td class="py-3 px-3 text-center font-bold whitespace-nowrap">
                      <span
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] whitespace-nowrap"
                        :class="cmp.hours_in_stage >= 24 ? 'bg-amber-100 text-amber-900 font-bold' : 'bg-surface-gray-2 text-ink-gray-7'"
                        :title="`${cmp.hours_in_stage} total hours in ${cmp.stage}`"
                      >
                        {{ formatTimeInStage(cmp.hours_in_stage, true) }}
                      </span>
                    </td>

                    <!-- Deadline -->
                    <td class="py-3 px-3 text-ink-gray-7 whitespace-nowrap">
                      {{ cmp.deadline || __('No Deadline') }}
                    </td>

                    <!-- Action -->
                    <td class="py-3 px-4 text-right">
                      <Button
                        size="xs"
                        variant="subtle"
                        :label="__('Open')"
                        :iconRight="LucideArrowRight"
                        @click.stop="openCampaign(cmp.name)"
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { Dialog, Button, createResource, call } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { ref, computed } from 'vue'

import LucideBriefcase from '~icons/lucide/briefcase'
import LucideUserCheck from '~icons/lucide/user-check'
import LucideClock from '~icons/lucide/clock'
import LucideAlertTriangle from '~icons/lucide/alert-triangle'
import LucideFlame from '~icons/lucide/flame'
import LucideArrowRight from '~icons/lucide/arrow-right'

const router = useRouter()
const show = defineModel('open', { default: false })
const selectedRole = ref('All')
const activeView = ref('capacity') // 'capacity' | 'stuck'

// 1. Fetch Team Capacity Breakdown
const teamCapacity = createResource({
  url: 'music_crm.capacity.get_team_capacity',
  auto: true,
})

// 2. Fetch Who Can Take Next Campaign
const whoCanTake = createResource({
  url: 'music_crm.capacity.who_can_take_next',
  params: { role_type: '' },
  auto: true,
})

// 3. Fetch Stage Bottlenecks
const timeInStage = createResource({
  url: 'music_crm.capacity.time_in_stage',
  auto: true,
})

// 4. Fetch Exact Stuck Campaigns
const stuckCampaigns = createResource({
  url: 'music_crm.capacity.get_stuck_campaigns',
  auto: true,
})

// 5. Fetch Rework Leaderboard
const reworkLeaderboard = createResource({
  url: 'music_crm.capacity.rework_leaderboard',
  auto: true,
})

const filteredCapacity = computed(() => {
  const data = teamCapacity.data || []
  if (selectedRole.value === 'All') return data
  return data.filter((row) => row.role_type === selectedRole.value)
})

async function openCampaign(campaignId) {
  if (!campaignId) return
  show.value = false
  if (campaignId.startsWith('CMP-') || campaignId.startsWith('CRM-')) {
    router.push({ name: 'Lead', params: { leadId: campaignId } })
    return
  }

  try {
    const res = await call('frappe.client.get_value', {
      doctype: 'CRM Lead',
      filters: { custom_song: campaignId },
      fieldname: 'name',
    })
    const leadId = res?.name || campaignId
    router.push({ name: 'Lead', params: { leadId } })
  } catch {
    router.push({ name: 'Lead', params: { leadId: campaignId } })
  }
}

function getBandBadgeClass(band) {
  switch (band) {
    case 'Available':
      return 'bg-green-50 text-green-700 dark:bg-green-950/40 dark:text-green-400'
    case 'Healthy':
      return 'bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-400'
    case 'Loaded':
      return 'bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-400'
    case 'Overloaded':
      return 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-400'
    default:
      return 'bg-surface-gray-2 text-ink-gray-6'
  }
}

function getBandDotClass(band) {
  switch (band) {
    case 'Available':
      return 'bg-green-500'
    case 'Healthy':
      return 'bg-blue-500'
    case 'Loaded':
      return 'bg-amber-500'
    case 'Overloaded':
      return 'bg-red-500'
    default:
      return 'bg-gray-400'
  }
}

function formatTimeInStage(totalHours, full = false) {
  if (!totalHours || totalHours <= 0) return '0 hrs'
  const hours = parseFloat(totalHours) || 0
  const d = Math.floor(hours / 24)
  const h = Math.round(hours % 24)

  if (d >= 1) {
    if (h > 0) {
      return full ? `${d} days ${h} hrs` : `${d}d ${h}h`
    }
    return full ? `${d} days` : `${d}d`
  }
  return full ? `${Math.max(1, Math.round(hours))} hrs` : `${Math.max(1, Math.round(hours))}h`
}
</script>
