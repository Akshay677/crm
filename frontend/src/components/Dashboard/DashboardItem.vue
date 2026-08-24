<template>
  <div class="h-full w-full">
    <div
      v-if="item.type == 'number_chart'"
      class="flex h-full w-full rounded shadow overflow-hidden transition-all duration-200"
      :class="['total_campaigns', 'active_campaigns', 'completed_campaigns', 'pending_campaigns', 'total_deliverables', 'completed_deliverables', 'pending_deliverables'].includes(item.name) && !editing ? 'cursor-pointer hover:ring-1 hover:ring-outline-gray-2 hover:shadow-md' : ''"
      @click="handleClick"
    >
      <Tooltip :text="__(item.data.tooltip)" class="w-full">
        <NumberChart
          v-if="item.data"
          :key="index"
          class="!items-start w-full"
          :config="item.data"
        >
          <template #title>
            <div class="flex items-center justify-between w-full">
              <span class="truncate text-sm-medium text-ink-gray-5 font-medium">
                {{ item.data.title }}
              </span>
              <div
                v-if="getCardMeta(item.name)"
                class="flex items-center justify-center size-7 rounded-lg ml-2 shrink-0 transition-transform group-hover:scale-105"
                :class="getCardMeta(item.name).bg"
              >
                <component
                  :is="getCardMeta(item.name).icon"
                  class="size-4"
                  :class="getCardMeta(item.name).color"
                />
              </div>
            </div>
          </template>
          <template #delta>
            <div
              v-if="item.data && item.data.delta !== undefined && item.data.delta !== null"
              class="flex items-center gap-1.5 mt-0.5"
            >
              <div
                class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[11px] font-semibold leading-none"
                :class="getTrendBadgeClass(item.data)"
              >
                <component
                  :is="getTrendIcon(item.data)"
                  class="size-3"
                />
                <span>{{ formatTrendValue(item.data) }}</span>
              </div>
              <span class="text-[11px] text-ink-gray-4">
                {{ __('vs last period') }}
              </span>
            </div>
          </template>
        </NumberChart>
      </Tooltip>
    </div>
    <div
      v-else-if="item.type == 'spacer'"
      class="rounded bg-surface-base h-full overflow-hidden text-ink-gray-5 flex items-center justify-center"
      :class="editing ? 'border border-dashed border-outline-gray-2' : ''"
    >
      {{ editing ? __('Spacer') : '' }}
    </div>
    <div
      v-else-if="item.type == 'axis_chart'"
      class="h-full w-full rounded-md bg-surface-base shadow flex flex-col p-4 sm:p-5"
    >
      <div v-if="item.data?.title" class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 mb-3">
        <div class="flex items-center gap-2.5">
          <div
            v-if="getSectionIcon(item.name)"
            class="flex items-center justify-center size-8 rounded-lg shrink-0"
            :class="getSectionIcon(item.name).bg"
          >
            <component
              :is="getSectionIcon(item.name).icon"
              class="size-4"
              :class="getSectionIcon(item.name).color"
            />
          </div>
          <div>
            <div class="text-sm font-semibold text-ink-gray-8">
              {{ __(item.data.title) }}
            </div>
            <div v-if="item.data.subtitle" class="text-xs text-ink-gray-5">
              {{ __(item.data.subtitle) }}
            </div>
          </div>
        </div>
        <Button
          v-if="item.name === 'team_workload' && !editing"
          variant="subtle"
          size="sm"
          class="self-start sm:self-auto text-xs"
          :label="__('View Bandwidth & Capacity')"
          :iconRight="LucideArrowRight"
          @click="showCapacityModal = true"
        />
      </div>
      <div class="flex-1 min-h-0 w-full">
        <AxisChart v-if="item.data" :config="getCleanChartConfig(item.data)" />
      </div>
    </div>
    <TeamCapacityModal
      v-if="showCapacityModal"
      v-model:open="showCapacityModal"
    />
    <div
      v-else-if="item.type == 'donut_chart'"
      class="h-full w-full rounded-md bg-surface-base shadow flex flex-col p-4 sm:p-5 overflow-hidden"
    >
      <div v-if="item.data?.title" class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2.5">
          <div
            v-if="getSectionIcon(item.name)"
            class="flex items-center justify-center size-8 rounded-lg shrink-0"
            :class="getSectionIcon(item.name).bg"
          >
            <component
              :is="getSectionIcon(item.name).icon"
              class="size-4"
              :class="getSectionIcon(item.name).color"
            />
          </div>
          <div>
            <div class="text-sm font-semibold text-ink-gray-8">
              {{ __(item.data.title) }}
            </div>
            <div v-if="item.data.subtitle" class="text-xs text-ink-gray-5">
              {{ __(item.data.subtitle) }}
            </div>
          </div>
        </div>
      </div>
      <div class="flex-1 min-h-0 w-full">
        <DonutChart v-if="item.data" :config="getCleanChartConfig(item.data)" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { AxisChart, DonutChart, NumberChart, Tooltip, Button } from 'frappe-ui'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

import TeamCapacityModal from '@/components/Modals/TeamCapacityModal.vue'

import LucideLayers from '~icons/lucide/layers'
import LucideActivity from '~icons/lucide/activity'
import LucideCheckCircle2 from '~icons/lucide/check-circle-2'
import LucideClock from '~icons/lucide/clock'
import LucidePackage from '~icons/lucide/package'
import LucideSend from '~icons/lucide/send'
import LucideHourglass from '~icons/lucide/hourglass'
import LucideZap from '~icons/lucide/zap'
import LucideUsers from '~icons/lucide/users'
import LucideHandshake from '~icons/lucide/handshake'
import LucideTrophy from '~icons/lucide/trophy'
import LucideCircleDollarSign from '~icons/lucide/circle-dollar-sign'
import LucideTimer from '~icons/lucide/timer'
import LucideTrendingUp from '~icons/lucide/trending-up'
import LucideTrendingDown from '~icons/lucide/trending-down'
import LucideMinus from '~icons/lucide/minus'

import LucidePieChart from '~icons/lucide/pie-chart'
import LucideLineChart from '~icons/lucide/line-chart'
import LucideBriefcase from '~icons/lucide/briefcase'
import LucideAlertTriangle from '~icons/lucide/alert-triangle'
import LucideBarChart3 from '~icons/lucide/bar-chart-3'
import LucideFilter from '~icons/lucide/filter'
import LucideXCircle from '~icons/lucide/x-circle'
import LucideShare2 from '~icons/lucide/share-2'
import LucideMapPin from '~icons/lucide/map-pin'
import LucideUserCheck from '~icons/lucide/user-check'
import LucideArrowRight from '~icons/lucide/arrow-right'

import { viewsStore } from '@/stores/views'

const router = useRouter()
const showCapacityModal = ref(false)
const { getPublicViews } = viewsStore()

const getCampaignView = (label) => {
  const view = getPublicViews().find((v) => v.label === label && v.dt === 'CRM Lead')
  return view ? view.name : label
}

const getDeliverableView = (label) => {
  const view = getPublicViews().find((v) => v.label === label && v.dt === 'CRM Task')
  return view ? view.name : label
}

const props = defineProps({
  index: { type: Number, required: true },
  item: { type: Object, required: true },
  editing: { type: Boolean, default: false },
})

const cardMetaMap = {
  total_campaigns: {
    icon: LucideLayers,
    bg: 'bg-blue-50 dark:bg-blue-950/40',
    color: 'text-blue-600 dark:text-blue-400',
  },
  active_campaigns: {
    icon: LucideActivity,
    bg: 'bg-green-50 dark:bg-green-950/40',
    color: 'text-green-600 dark:text-green-400',
  },
  completed_campaigns: {
    icon: LucideCheckCircle2,
    bg: 'bg-purple-50 dark:bg-purple-950/40',
    color: 'text-purple-600 dark:text-purple-400',
  },
  pending_campaigns: {
    icon: LucideClock,
    bg: 'bg-amber-50 dark:bg-amber-950/40',
    color: 'text-amber-600 dark:text-amber-400',
  },
  total_deliverables: {
    icon: LucidePackage,
    bg: 'bg-violet-50 dark:bg-violet-950/40',
    color: 'text-violet-600 dark:text-violet-400',
  },
  completed_deliverables: {
    icon: LucideSend,
    bg: 'bg-teal-50 dark:bg-teal-950/40',
    color: 'text-teal-600 dark:text-teal-400',
  },
  pending_deliverables: {
    icon: LucideHourglass,
    bg: 'bg-orange-50 dark:bg-orange-950/40',
    color: 'text-orange-600 dark:text-orange-400',
  },
  execution_rate: {
    icon: LucideZap,
    bg: 'bg-cyan-50 dark:bg-cyan-950/40',
    color: 'text-cyan-600 dark:text-cyan-400',
  },
  total_leads: {
    icon: LucideUsers,
    bg: 'bg-blue-50 dark:bg-blue-950/40',
    color: 'text-blue-600 dark:text-blue-400',
  },
  ongoing_deals: {
    icon: LucideHandshake,
    bg: 'bg-blue-50 dark:bg-blue-950/40',
    color: 'text-blue-600 dark:text-blue-400',
  },
  won_deals: {
    icon: LucideTrophy,
    bg: 'bg-amber-50 dark:bg-amber-950/40',
    color: 'text-amber-600 dark:text-amber-400',
  },
  average_won_deal_value: {
    icon: LucideCircleDollarSign,
    bg: 'bg-green-50 dark:bg-green-950/40',
    color: 'text-green-600 dark:text-green-400',
  },
  average_deal_value: {
    icon: LucideCircleDollarSign,
    bg: 'bg-violet-50 dark:bg-violet-950/40',
    color: 'text-violet-600 dark:text-violet-400',
  },
  average_time_to_close_a_lead: {
    icon: LucideTimer,
    bg: 'bg-red-50 dark:bg-red-950/40',
    color: 'text-red-600 dark:text-red-400',
  },
  average_time_to_close_a_deal: {
    icon: LucideTimer,
    bg: 'bg-pink-50 dark:bg-pink-950/40',
    color: 'text-pink-600 dark:text-pink-400',
  },
}

const sectionMetaMap = {
  campaigns_by_stage: {
    icon: LucidePieChart,
    bg: 'bg-blue-50 dark:bg-blue-950/40',
    color: 'text-blue-600 dark:text-blue-400',
  },
  campaigns_by_execution_stage: {
    icon: LucideBarChart3,
    bg: 'bg-violet-50 dark:bg-violet-950/40',
    color: 'text-violet-600 dark:text-violet-400',
  },
  execution_trend: {
    icon: LucideLineChart,
    bg: 'bg-green-50 dark:bg-green-950/40',
    color: 'text-green-600 dark:text-green-400',
  },
  team_workload: {
    icon: LucideBriefcase,
    bg: 'bg-purple-50 dark:bg-purple-950/40',
    color: 'text-purple-600 dark:text-purple-400',
  },
  campaigns_at_risk: {
    icon: LucideAlertTriangle,
    bg: 'bg-red-50 dark:bg-red-950/40',
    color: 'text-red-600 dark:text-red-400',
  },
  sales_trend: {
    icon: LucideLineChart,
    bg: 'bg-blue-50 dark:bg-blue-950/40',
    color: 'text-blue-600 dark:text-blue-400',
  },
  forecasted_revenue: {
    icon: LucideBarChart3,
    bg: 'bg-violet-50 dark:bg-violet-950/40',
    color: 'text-violet-600 dark:text-violet-400',
  },
  funnel_conversion: {
    icon: LucideFilter,
    bg: 'bg-cyan-50 dark:bg-cyan-950/40',
    color: 'text-cyan-600 dark:text-cyan-400',
  },
  deals_by_stage_donut: {
    icon: LucidePieChart,
    bg: 'bg-blue-50 dark:bg-blue-950/40',
    color: 'text-blue-600 dark:text-blue-400',
  },
  lost_deal_reasons: {
    icon: LucideXCircle,
    bg: 'bg-red-50 dark:bg-red-950/40',
    color: 'text-red-600 dark:text-red-400',
  },
  leads_by_source: {
    icon: LucideShare2,
    bg: 'bg-teal-50 dark:bg-teal-950/40',
    color: 'text-teal-600 dark:text-teal-400',
  },
  deals_by_source: {
    icon: LucideShare2,
    bg: 'bg-teal-50 dark:bg-teal-950/40',
    color: 'text-teal-600 dark:text-teal-400',
  },
  deals_by_territory: {
    icon: LucideMapPin,
    bg: 'bg-amber-50 dark:bg-amber-950/40',
    color: 'text-amber-600 dark:text-amber-400',
  },
  deals_by_salesperson: {
    icon: LucideUserCheck,
    bg: 'bg-violet-50 dark:bg-violet-950/40',
    color: 'text-violet-600 dark:text-violet-400',
  },
}

function getCardMeta(name) {
  return cardMetaMap[name] || null
}

function getSectionIcon(name) {
  return sectionMetaMap[name] || {
    icon: LucideBarChart3,
    bg: 'bg-surface-gray-2',
    color: 'text-ink-gray-6',
  }
}

function getCleanChartConfig(data) {
  if (!data) return {}
  return {
    ...data,
    title: '',
    subtitle: '',
  }
}

function getTrendBadgeClass(data) {
  const delta = data.delta || 0
  const negativeIsBetter = data.negativeIsBetter || false

  if (delta > 0) {
    return negativeIsBetter
      ? 'bg-red-50 text-red-700 dark:bg-red-950/50 dark:text-red-400'
      : 'bg-green-50 text-green-700 dark:bg-green-950/50 dark:text-green-400'
  } else if (delta < 0) {
    return negativeIsBetter
      ? 'bg-green-50 text-green-700 dark:bg-green-950/50 dark:text-green-400'
      : 'bg-red-50 text-red-700 dark:bg-red-950/50 dark:text-red-400'
  } else {
    return 'bg-surface-gray-2 text-ink-gray-5'
  }
}

function getTrendIcon(data) {
  const delta = data.delta || 0
  if (delta > 0) return LucideTrendingUp
  if (delta < 0) return LucideTrendingDown
  return LucideMinus
}

function formatTrendValue(data) {
  const delta = data.delta || 0
  const prefix = data.deltaPrefix || (delta > 0 ? '+' : '')
  const suffix = data.deltaSuffix !== undefined ? data.deltaSuffix : '%'
  return `${prefix}${Math.round(delta * 10) / 10}${suffix}`
}

function handleClick() {
  if (props.editing) return

  const campaignViews = {
    total_campaigns: 'Total Campaigns',
    active_campaigns: 'Active Campaigns',
    completed_campaigns: 'Completed Campaigns',
    pending_campaigns: 'Pending Campaigns',
  }

  const deliverableViews = {
    total_deliverables: 'Total Deliverables',
    completed_deliverables: 'Posted Deliverables',
    pending_deliverables: 'Pending Deliverables',
  }

  if (campaignViews[props.item.name]) {
    const viewLabel = campaignViews[props.item.name]
    const viewName = getCampaignView(viewLabel)
    if (props.item.name === 'total_campaigns') {
      router.push({ name: 'Leads' })
    } else {
      router.push({ name: 'Leads', query: { view: viewName } })
    }
  } else if (deliverableViews[props.item.name]) {
    const viewLabel = deliverableViews[props.item.name]
    const viewName = getDeliverableView(viewLabel)
    if (props.item.name === 'total_deliverables') {
      router.push({ name: 'Tasks', query: { view: viewName } })
    } else {
      router.push({ name: 'Tasks', query: { view: viewName } })
    }
  }
}
</script>
