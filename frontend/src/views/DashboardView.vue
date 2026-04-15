<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../router/auth'
import { createTransaction, getDashboardSummary, getRecentTransactions } from '../services/api'

const router = useRouter()

const loading = ref(true)
const errorMessage = ref('')
const createErrorMessage = ref('')
const isCreating = ref(false)

const summary = ref({
	total_balance: 0,
	monthly_income: 0,
	monthly_expenses: 0,
	transaction_count: 0
})
const recentTransactions = ref([])
const newTransaction = ref({
	title: '',
	amount: '',
	type: 'expense',
	category: '',
	date: new Date().toISOString().slice(0, 10)
})

const todayLabel = computed(() => {
	return new Intl.DateTimeFormat('en-US', {
		weekday: 'short',
		month: 'short',
		day: 'numeric'
	}).format(new Date())
})

const formattedBalance = computed(() => formatCurrency(summary.value.total_balance))
const formattedMonthlyIncome = computed(() => formatCurrency(summary.value.monthly_income))
const formattedMonthlyExpenses = computed(() => formatCurrency(summary.value.monthly_expenses))

const monthWindow = computed(() => {
	const now = new Date()
	const start = new Date(now.getFullYear(), now.getMonth(), 1, 0, 0, 0, 0)
	const end = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59, 999)

	return {
		startDate: start.toISOString(),
		endDate: end.toISOString()
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

const formatDate = (dateValue) => {
	if (!dateValue) return 'No date'
	const parsedDate = new Date(dateValue)
	if (Number.isNaN(parsedDate.getTime())) return 'Invalid date'

	return new Intl.DateTimeFormat('en-US', {
		month: 'short',
		day: 'numeric',
		year: 'numeric'
	}).format(parsedDate)
}

const amountClass = (type) => {
	return type === 'income' ? 'text-cyan-300' : 'text-blue-100'
}

const amountPrefix = (type) => {
	return type === 'income' ? '+' : '-'
}

const resetTransactionForm = () => {
	newTransaction.value = {
		title: '',
		amount: '',
		type: 'expense',
		category: '',
		date: new Date().toISOString().slice(0, 10)
	}
}

const loadDashboardData = async () => {
	errorMessage.value = ''
	loading.value = true

	try {
		const [summaryResponse, recentResponse] = await Promise.all([
			getDashboardSummary(monthWindow.value),
			getRecentTransactions(20)
		])

		summary.value = summaryResponse
		recentTransactions.value = recentResponse
	} catch (error) {
		errorMessage.value = error?.message || 'Unable to load dashboard data right now.'
	} finally {
		loading.value = false
	}
}

const handleCreateTransaction = async () => {
	createErrorMessage.value = ''

	const amountValue = Number(newTransaction.value.amount)
	if (!newTransaction.value.title.trim()) {
		createErrorMessage.value = 'Title is required.'
		return
	}
	if (!Number.isFinite(amountValue) || amountValue <= 0) {
		createErrorMessage.value = 'Amount must be greater than 0.'
		return
	}

	isCreating.value = true
	try {
		await createTransaction({
			title: newTransaction.value.title.trim(),
			amount: amountValue,
			type: newTransaction.value.type,
			category: newTransaction.value.category.trim() || null,
			date: newTransaction.value.date ? new Date(`${newTransaction.value.date}T12:00:00`).toISOString() : null
		})

		resetTransactionForm()
		await loadDashboardData()
	} catch (error) {
		createErrorMessage.value = error?.message || 'Unable to add transaction right now.'
	} finally {
		isCreating.value = false
	}
}

const handleLogout = async () => {
	authStore.logout()
	await router.push('/login')
}

onMounted(() => {
	loadDashboardData()
})
</script>

<template>
	<div class="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_15%_10%,rgba(54,120,255,0.28),transparent_36%),radial-gradient(circle_at_90%_8%,rgba(21,64,176,0.32),transparent_34%),linear-gradient(140deg,#04070d,#0b1324)] text-blue-50">
		<div class="pointer-events-none absolute -left-24 top-28 h-72 w-72 rounded-full bg-[radial-gradient(circle,rgba(74,164,255,0.16),transparent_65%)]"></div>
		<div class="pointer-events-none absolute -right-20 -top-16 h-72 w-72 rounded-full bg-[radial-gradient(circle,rgba(47,112,255,0.16),transparent_65%)]"></div>

		<header class="relative z-10 border-b border-blue-300/20 bg-[#081127bf] backdrop-blur-md">
			<div class="mx-auto flex w-full max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
				<div class="flex items-center gap-3">
					<div class="grid h-10 w-10 place-items-center rounded-xl border border-blue-300/35 bg-blue-500/15 text-sm font-bold tracking-wider text-blue-200">
						FT
					</div>
					<div>
						<p class="text-xs uppercase tracking-[0.14em] text-blue-200/70">FinTrack</p>
						<h1 class="text-lg font-semibold tracking-wide text-blue-50 sm:text-xl">Dashboard</h1>
					</div>
				</div>

				<div class="flex items-center gap-3">
					<p class="hidden rounded-full border border-blue-300/25 bg-blue-400/10 px-3 py-1 text-xs tracking-wide text-blue-100/85 sm:block">
						{{ todayLabel }}
					</p>

					<button
						type="button"
						@click="handleLogout"
						class="rounded-xl border border-blue-300/35 bg-blue-500/15 px-4 py-2 text-sm font-medium tracking-wide text-blue-100 transition duration-200 hover:-translate-y-0.5 hover:border-blue-200/60 hover:bg-blue-500/30"
					>
						Log Out
					</button>
				</div>
			</div>
		</header>

		<main class="relative z-10 mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
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

			<section class="mt-6 grid gap-6 lg:grid-cols-[360px_1fr]">
				<article class="rounded-2xl border border-blue-300/20 bg-[#0a142db8] p-5 shadow-[0_18px_48px_rgba(0,0,0,0.45)] backdrop-blur-sm sm:p-6">
					<h2 class="text-lg font-semibold tracking-wide text-blue-50">Add Transaction</h2>
					<p class="mt-1 text-xs text-blue-200/70">Create income or expense and refresh the dashboard instantly.</p>

					<form class="mt-4 space-y-3" @submit.prevent="handleCreateTransaction">
						<div>
							<label for="title" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Title</label>
							<input
								id="title"
								v-model="newTransaction.title"
								type="text"
								placeholder="Salary, groceries, rent..."
								class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition placeholder:text-blue-300/40 focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
								required
							/>
						</div>

						<div class="grid grid-cols-2 gap-3">
							<div>
								<label for="amount" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Amount</label>
								<input
									id="amount"
									v-model="newTransaction.amount"
									type="number"
									step="0.01"
									min="0.01"
									placeholder="0.00"
									class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition placeholder:text-blue-300/40 focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
									required
								/>
							</div>

							<div>
								<label for="type" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Type</label>
								<select
									id="type"
									v-model="newTransaction.type"
									class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
								>
									<option value="expense">Expense</option>
									<option value="income">Income</option>
								</select>
							</div>
						</div>

						<div class="grid grid-cols-2 gap-3">
							<div>
								<label for="category" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Category</label>
								<input
									id="category"
									v-model="newTransaction.category"
									type="text"
									placeholder="Optional"
									class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition placeholder:text-blue-300/40 focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
								/>
							</div>

							<div>
								<label for="date" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Date</label>
								<input
									id="date"
									v-model="newTransaction.date"
									type="date"
									class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
								/>
							</div>
						</div>

						<p v-if="createErrorMessage" class="rounded-lg border border-blue-300/30 bg-blue-900/35 px-3 py-2 text-sm text-blue-200">
							{{ createErrorMessage }}
						</p>

						<button
							type="submit"
							:disabled="isCreating"
							class="w-full rounded-xl bg-gradient-to-r from-blue-600 to-sky-400 px-4 py-2.5 text-xs font-semibold uppercase tracking-[0.12em] text-white transition hover:-translate-y-0.5 hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-70"
						>
							{{ isCreating ? 'Saving...' : 'Add Transaction' }}
						</button>
					</form>
				</article>

				<article class="rounded-2xl border border-blue-300/20 bg-[#0a142db8] p-5 shadow-[0_18px_48px_rgba(0,0,0,0.45)] backdrop-blur-sm sm:p-6">
				<div class="flex flex-wrap items-center justify-between gap-3">
					<h2 class="text-lg font-semibold tracking-wide text-blue-50">Recent Transactions</h2>
					<button
						type="button"
						@click="loadDashboardData"
						class="rounded-lg border border-blue-300/35 bg-blue-500/15 px-3 py-1.5 text-xs font-medium uppercase tracking-[0.12em] text-blue-100 transition hover:bg-blue-500/30"
					>
						Refresh
					</button>
				</div>

				<p v-if="errorMessage" class="mt-4 rounded-lg border border-blue-300/30 bg-blue-900/35 px-3 py-2 text-sm text-blue-200">
					{{ errorMessage }}
				</p>

				<div v-if="loading" class="mt-4 space-y-2">
					<div v-for="index in 6" :key="index" class="h-14 animate-pulse rounded-xl bg-blue-400/10"></div>
				</div>

				<ul v-else-if="recentTransactions.length > 0" class="mt-4 divide-y divide-blue-300/12">
					<li v-for="transaction in recentTransactions" :key="transaction.id" class="flex items-center justify-between gap-3 py-3">
						<div>
							<p class="text-sm font-medium text-blue-50">{{ transaction.title }}</p>
							<p class="text-xs text-blue-200/65">
								{{ transaction.category || 'Uncategorized' }} • {{ formatDate(transaction.date) }}
							</p>
						</div>
						<p class="text-sm font-semibold" :class="amountClass(transaction.type)">
							{{ amountPrefix(transaction.type) }}{{ formatCurrency(transaction.amount) }}
						</p>
					</li>
				</ul>

				<p v-else class="mt-4 rounded-lg border border-blue-300/20 bg-blue-900/20 px-3 py-2 text-sm text-blue-200/80">
					No transactions yet. Add your first income or expense to populate this dashboard.
				</p>
				</article>
			</section>
		</main>
	</div>
</template>