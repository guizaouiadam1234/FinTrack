<script setup>
import { computed } from 'vue'

const props = defineProps({
	summary: {
		type: Object,
		required: true
	}
})

const formatCurrency = (amount) => {
	const value = Number.isFinite(Number(amount)) ? Number(amount) : 0
	return new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: 'USD',
		minimumFractionDigits: 2,
		maximumFractionDigits: 2
	}).format(value)
}

const formattedBalance = computed(() => formatCurrency(props.summary.total_balance))
const formattedMonthlyIncome = computed(() => formatCurrency(props.summary.monthly_income))
const formattedMonthlyExpenses = computed(() => formatCurrency(props.summary.monthly_expenses))
</script>

<template>
	<section class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
		<article class="rounded-2xl border border-blue-300/20 bg-[#0a142db8] p-5 shadow-[0_18px_48px_rgba(0,0,0,0.45)] backdrop-blur-sm">
			<p class="text-xs uppercase tracking-[0.14em] text-blue-200/70">Total Balance</p>
			<p class="mt-2 text-3xl font-semibold tracking-tight" :class="summary.total_balance >= 0 ? 'text-cyan-300' : 'text-blue-100'">
				{{ formattedBalance }}
			</p>
			<p class="mt-2 text-xs text-blue-200/60">All-time across your transactions</p>
		</article>

		<article class="rounded-2xl border border-blue-300/20 bg-[#0a142db8] p-5 shadow-[0_18px_48px_rgba(0,0,0,0.45)] backdrop-blur-sm">
			<p class="text-xs uppercase tracking-[0.14em] text-blue-200/70">Monthly Income</p>
			<p class="mt-2 text-3xl font-semibold tracking-tight text-cyan-300">{{ formattedMonthlyIncome }}</p>
			<p class="mt-2 text-xs text-blue-200/60">Current month (local time)</p>
		</article>

		<article class="rounded-2xl border border-blue-300/20 bg-[#0a142db8] p-5 shadow-[0_18px_48px_rgba(0,0,0,0.45)] backdrop-blur-sm sm:col-span-2 lg:col-span-1">
			<p class="text-xs uppercase tracking-[0.14em] text-blue-200/70">Monthly Expenses</p>
			<p class="mt-2 text-3xl font-semibold tracking-tight text-blue-100">{{ formattedMonthlyExpenses }}</p>
			<p class="mt-2 text-xs text-blue-200/60">{{ summary.transaction_count }} total transactions</p>
		</article>
	</section>
</template>
