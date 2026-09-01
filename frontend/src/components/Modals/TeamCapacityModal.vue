<template>
  <Dialog v-model:open="show" :size="'5xl'">
    <template #body>
      <div class="bg-surface-elevation-1 p-5 sm:p-6 overflow-x-hidden rounded-2xl">
        <!-- Modal Header -->
        <div class="flex items-start justify-between pb-4 border-b border-outline-gray-1">
          <div class="flex items-center gap-3">
            <div class="flex items-center justify-center size-10 rounded-xl bg-purple-50 text-purple-600 dark:bg-purple-950/50 dark:text-purple-400 border border-purple-200 dark:border-purple-800 shrink-0">
              <LucideBriefcase class="size-5" />
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-base sm:text-xl font-bold text-ink-gray-9">
                  {{ __('Team Capacity & Bandwidth') }}
                </h3>
              </div>
              <p class="text-xs text-ink-gray-5 mt-0.5">
                {{ __('Workload scores, available bandwidth, and workflow bottlenecks') }}
              </p>
            </div>
          </div>
          <Button variant="ghost" icon="lucide-x" class="w-8 h-8 rounded-lg hover:bg-surface-gray-2 text-ink-gray-6" @click="show = false" />
        </div>

        <div class="max-h-[74vh] overflow-y-auto overflow-x-hidden py-4 space-y-4">
          <!-- Top 3 Insight Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <!-- 1. Who can take next campaign -->
            <div class="p-3.5 rounded-xl border border-outline-gray-1 bg-surface-base flex flex-col gap-2 shadow-2xs">
              <div class="flex items-center gap-2 text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">
                <LucideUserCheck class="size-4 text-emerald-600" />
                <span>{{ __('Who Takes Next Campaign') }}</span>
              </div>
              <div
                v-if="whoCanTake.data?.length"
                class="space-y-1.5 max-h-[82px] overflow-y-auto pr-1"
              >
                <div
                  v-for="person in whoCanTake.data"
                  :key="person.user"
                  class="flex items-center justify-between text-xs py-0.5"
                >
                  <div class="flex items-center gap-1.5 min-w-0">
                    <span class="font-medium text-ink-gray-9 truncate text-xs">
                      <span class="text-ink-gray-5">{{ person.role_type }}:</span> {{ person.full_name }}
                    </span>
                  </div>
                  <span class="px-2 py-0.5 rounded text-[10px] bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 font-semibold shrink-0">
                    {{ person.band }}
                  </span>
                </div>
              </div>
              <div v-else class="text-xs text-ink-gray-5 py-1">
                {{ __('No available team members found') }}
              </div>
            </div>

            <!-- 2. Where work is stuck (Top Stuck Campaigns) -->
            <div class="p-3.5 rounded-xl border border-outline-gray-1 bg-surface-base flex flex-col gap-2 shadow-2xs">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2 text-xs font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wider">
                  <LucideClock class="size-4 text-amber-600" />
                  <span>{{ __('Where Work Is Stuck') }}</span>
                </div>
                <button
                  class="text-[11px] text-amber-700 dark:text-amber-400 hover:text-amber-800 font-semibold hover:underline transition-colors cursor-pointer"
                  @click="activeView = activeView === 'stuck' ? 'capacity' : 'stuck'"
                >
                  {{ activeView === 'stuck' ? __('View Capacity') : __('View All') }}
                </button>
              </div>
              <div v-if="stuckCampaigns.data?.length" class="space-y-1.5">
                <div
                  v-for="cmp in stuckCampaigns.data.slice(0, 2)"
                  :key="cmp.name"
                  class="flex items-center justify-between text-xs cursor-pointer hover:bg-surface-gray-2 p-1 rounded-lg transition-colors group"
                  @click="openCampaign(cmp.name)"
                >
                  <div class="flex flex-col min-w-0 pr-1">
                    <span class="font-semibold text-ink-gray-9 truncate max-w-[130px] group-hover:text-primary-600 text-xs" :title="cmp.song">
                      {{ cmp.song }}
                    </span>
                    <span class="text-[10px] text-ink-gray-5">
                      {{ cmp.stage }} • {{ cmp.responsible }}
                    </span>
                  </div>
                  <span
                    class="px-2 py-0.5 rounded text-[10px] bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 font-bold shrink-0"
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
              <div v-else class="text-xs text-ink-gray-5 py-1">
                {{ __('No stage bottleneck data yet') }}
              </div>
            </div>

            <!-- 3. Rework Leaderboard (Edits bouncing) -->
            <div class="p-3.5 rounded-xl border border-outline-gray-1 bg-surface-base flex flex-col gap-2 shadow-2xs">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2 text-xs font-bold text-rose-700 dark:text-rose-400 uppercase tracking-wider">
                  <LucideAlertTriangle class="size-4 text-rose-600" />
                  <span>{{ __('Rework Leaderboard') }}</span>
                </div>
              </div>
              <div v-if="reworkLeaderboard.data?.by_campaign?.length" class="space-y-1.5">
                <div
                  v-for="cmp in reworkLeaderboard.data.by_campaign.slice(0, 2)"
                  :key="cmp.name || cmp.campaign"
                  class="flex items-center justify-between text-xs cursor-pointer hover:bg-surface-gray-2 p-1 rounded-lg transition-colors group"
                  @click="openCampaign(cmp.name || cmp.campaign)"
                >
                  <span class="font-semibold text-ink-gray-9 truncate max-w-[130px] group-hover:text-primary-600 text-xs" :title="cmp.song || cmp.campaign">{{ cmp.song || cmp.campaign }}</span>
                  <span class="px-2 py-0.5 rounded text-[10px] bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 font-bold shrink-0">
                    {{ cmp.rework_rounds }} {{ __('rounds') }}
                  </span>
                </div>
              </div>
              <div v-else class="text-xs text-ink-gray-5 py-1">
                {{ __('No rework rounds recorded') }}
              </div>
            </div>
          </div>

          <!-- Navigation / Mode Tabs & Role Filters -->
          <div class="flex items-center justify-between flex-wrap gap-2 pt-1">
            <!-- View Switcher -->
            <div class="flex items-center p-1 bg-surface-gray-2 border border-outline-gray-1 rounded-xl shadow-2xs">
              <button
                class="px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer"
                :class="activeView === 'capacity' ? 'bg-surface-base text-ink-gray-9 shadow-xs font-bold' : 'text-ink-gray-5 hover:text-ink-gray-8'"
                @click="activeView = 'capacity'"
              >
                <span>{{ __('Team Capacity Table') }}</span>
              </button>
              <button
                class="px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-2 cursor-pointer"
                :class="activeView === 'stuck' ? 'bg-surface-base text-ink-gray-9 shadow-xs font-bold' : 'text-ink-gray-5 hover:text-ink-gray-8'"
                @click="activeView = 'stuck'"
              >
                <span>{{ __('Stuck Campaigns') }}</span>
                <span
                  v-if="stuckCampaigns.data?.length"
                  class="min-w-[18px] h-[18px] px-1.5 rounded-full flex items-center justify-center text-[10px] font-bold bg-amber-100 text-amber-800 dark:bg-amber-950/70 dark:text-amber-300 border border-amber-200 dark:border-amber-800"
                >
                  {{ stuckCampaigns.data.length }}
                </span>
              </button>
            </div>

            <!-- Role filter pill (Only for Capacity View) -->
            <div v-if="activeView === 'capacity'" class="flex items-center p-1 bg-surface-gray-2 border border-outline-gray-1 rounded-xl shadow-2xs">
              <button
                v-for="role in ['All', 'Project Manager', 'Editor', 'Executor']"
                :key="role"
                class="px-2.5 py-1 text-xs font-medium rounded-lg transition-all cursor-pointer"
                :class="selectedRole === role ? 'bg-surface-base text-ink-gray-9 font-bold shadow-xs' : 'text-ink-gray-5 hover:text-ink-gray-8'"
                @click="selectedRole = role"
              >
                {{ __(role) }}
              </button>
            </div>
          </div>

          <!-- VIEW 1: Team Capacity Breakdown Table -->
          <div v-if="activeView === 'capacity'" class="border border-outline-gray-1 rounded-xl overflow-hidden bg-surface-base shadow-xs">
            <div v-if="teamCapacity.loading" class="p-8 text-center text-sm text-ink-gray-5">
              {{ __('Loading team workload data...') }}
            </div>
            <div v-else class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-surface-gray-2 text-ink-gray-6 border-b border-outline-gray-1 font-bold uppercase tracking-wider text-[11px]">
                  <tr>
                    <th class="py-3 px-4">{{ __('Team Member') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Active Campaigns') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Deliverables (Done / Total)') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Pending') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Urgent (48h)') }}</th>
                    <th class="py-3 px-3 text-center">{{ __('Next Deadline') }}</th>
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
                    <!-- Member Name & Role -->
                    <td class="py-3 px-4">
                      <div class="flex flex-col">
                        <span class="font-bold text-ink-gray-9 text-sm leading-tight">{{ row.full_name }}</span>
                        <span class="text-[11px] text-ink-gray-5">{{ row.role_type }}</span>
                      </div>
                    </td>

                    <!-- Active Campaigns -->
                    <td class="py-3 px-3 text-center font-bold text-ink-gray-8 text-sm">
                      {{ row.active_campaigns }}
                    </td>

                    <!-- Deliverables Done / Total -->
                    <td class="py-3 px-3 text-center font-semibold whitespace-nowrap">
                      <span v-if="row.pending === 0 && row.assigned > 0" class="text-emerald-600 font-bold text-xs">
                        {{ row.completed }} / {{ row.assigned }}
                      </span>
                      <span v-else class="text-ink-gray-8 text-xs font-semibold">
                        <span class="text-emerald-600 font-bold">{{ row.completed }}</span> / {{ row.assigned }}
                      </span>
                    </td>

                    <!-- Pending Deliverables -->
                    <td class="py-3 px-3 text-center font-bold text-sm text-ink-gray-9">
                      {{ row.pending }}
                    </td>

                    <!-- Urgent 48h Deliverables -->
                    <td class="py-3 px-3 text-center whitespace-nowrap">
                      <span
                        v-if="row.urgent > 0"
                        class="inline-flex items-center gap-1 font-bold text-red-600"
                      >
                        <LucideFlame class="size-3.5 text-red-500 fill-red-500" />
                        <span>{{ row.urgent }}</span>
                      </span>
                      <span v-else class="text-ink-gray-4">-</span>
                    </td>

                    <!-- Next Deadline -->
                    <td class="py-3 px-3 text-center font-medium text-ink-gray-7 text-xs whitespace-nowrap">
                      {{ row.next_deadline || __('None') }}
                    </td>

                    <!-- Daily Cap -->
                    <td class="py-3 px-3 text-center text-ink-gray-5 text-xs">
                      {{ row.daily_capacity }}/day
                    </td>

                    <!-- Workload Status Band -->
                    <td class="py-3 px-4 text-center whitespace-nowrap">
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
          <div v-else class="border border-outline-gray-1 rounded-xl overflow-hidden bg-surface-base shadow-xs">
            <div v-if="stuckCampaigns.loading" class="p-8 text-center text-sm text-ink-gray-5">
              {{ __('Loading stuck campaigns...') }}
            </div>
            <div v-else-if="!stuckCampaigns.data?.length" class="p-8 text-center text-sm text-ink-gray-5">
              {{ __('No stuck campaigns! Everything is moving smoothly.') }}
            </div>
            <div v-else class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-surface-gray-2 text-ink-gray-6 border-b border-outline-gray-1 font-bold uppercase tracking-wider text-[11px]">
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
                    <!-- Campaign Song & ID -->
                    <td class="py-3 px-4">
                      <div class="flex flex-col min-w-0 max-w-[200px]">
                        <span class="font-bold text-ink-gray-9 text-sm truncate hover:text-primary-600 transition-colors" :title="cmp.song">
                          {{ cmp.song }}
                        </span>
                        <span class="text-[11px] text-ink-gray-5 font-normal mt-0.5">
                          {{ cmp.name }}
                        </span>
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
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] whitespace-nowrap font-bold"
                        :class="cmp.hours_in_stage >= 24 ? 'bg-amber-100 text-amber-900' : 'bg-surface-gray-2 text-ink-gray-7'"
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
