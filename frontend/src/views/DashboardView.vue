<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../router/auth'
import { createTransaction, deleteTransaction, getDashboardSummary, getRecentTransactions, updateTransaction } from '../services/api'
import DashboardSummaryCards from '../components/DashboardSummaryCards.vue'
import TransactionEntryForm from '../components/TransactionEntryForm.vue'
import TransactionListPanel from '../components/TransactionListPanel.vue'

const router = useRouter()

const loading = ref(true)
const errorMessage = ref('')
const createErrorMessage = ref('')
const isCreating = ref(false)
const rowActionErrorMessage = ref('')
const actionMenuOpenId = ref(null)

const editingTransaction = ref(null)
const isSavingEdit = ref(false)
const editForm = ref({
	title: '',
	amount: '',
	type: 'expense',
	category: '',
	date: ''
})
const editErrorMessage = ref('')

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

const monthWindow = computed(() => {
	const now = new Date()
	const start = new Date(now.getFullYear(), now.getMonth(), 1, 0, 0, 0, 0)
	const end = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59, 999)

	return {
		startDate: start.toISOString(),
		endDate: end.toISOString()
	}
})

const resetTransactionForm = () => {
	newTransaction.value = {
		title: '',
		amount: '',
		type: 'expense',
		category: '',
		date: new Date().toISOString().slice(0, 10)
	}
}

const toDateInput = (dateValue) => {
	if (!dateValue) return ''
	const date = new Date(dateValue)
	if (Number.isNaN(date.getTime())) return ''
	return date.toISOString().slice(0, 10)
}

const toggleActionMenu = (transactionId) => {
	actionMenuOpenId.value = actionMenuOpenId.value === transactionId ? null : transactionId
}

const updateNewTransactionForm = (nextFormState) => {
	newTransaction.value = nextFormState
}

const updateEditFormState = (nextEditFormState) => {
	editForm.value = nextEditFormState
}

const closeEditModal = () => {
	editingTransaction.value = null
	editErrorMessage.value = ''
}

const openEditModal = (transaction) => {
	actionMenuOpenId.value = null
	rowActionErrorMessage.value = ''
	editingTransaction.value = transaction
	editForm.value = {
		title: transaction.title || '',
		amount: String(transaction.amount ?? ''),
		type: transaction.type || 'expense',
		category: transaction.category || '',
		date: toDateInput(transaction.date)
	}
}

const handleDeleteTransaction = async (transaction) => {
	actionMenuOpenId.value = null
	rowActionErrorMessage.value = ''
	const confirmed = window.confirm(`Delete transaction \"${transaction.title}\"?`)
	if (!confirmed) return

	try {
		await deleteTransaction(transaction.id)
		await loadDashboardData()
	} catch (error) {
		rowActionErrorMessage.value = error?.message || 'Unable to delete transaction right now.'
	}
}

const handleUpdateTransaction = async () => {
	editErrorMessage.value = ''
	if (!editingTransaction.value) return

	const amountValue = Number(editForm.value.amount)
	if (!editForm.value.title.trim()) {
		editErrorMessage.value = 'Title is required.'
		return
	}
	if (!Number.isFinite(amountValue) || amountValue <= 0) {
		editErrorMessage.value = 'Amount must be greater than 0.'
		return
	}

	isSavingEdit.value = true
	try {
		await updateTransaction(editingTransaction.value.id, {
			title: editForm.value.title.trim(),
			amount: amountValue,
			type: editForm.value.type,
			category: editForm.value.category.trim() || null,
			date: editForm.value.date ? new Date(`${editForm.value.date}T12:00:00`).toISOString() : null
		})

		closeEditModal()
		await loadDashboardData()
	} catch (error) {
		editErrorMessage.value = error?.message || 'Unable to update transaction right now.'
	} finally {
		isSavingEdit.value = false
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
			<DashboardSummaryCards :summary="summary" />

			<section class="mt-6 grid gap-6 lg:grid-cols-[360px_1fr]">
				<TransactionEntryForm
					:form="newTransaction"
					:error-message="createErrorMessage"
					:is-creating="isCreating"
					@update:form="updateNewTransactionForm"
					@submit="handleCreateTransaction"
				/>

				<TransactionListPanel
					:loading="loading"
					:error-message="errorMessage"
					:row-action-error-message="rowActionErrorMessage"
					:transactions="recentTransactions"
					:action-menu-open-id="actionMenuOpenId"
					:editing-transaction="editingTransaction"
					:edit-form="editForm"
					:is-saving-edit="isSavingEdit"
					:edit-error-message="editErrorMessage"
					@refresh="loadDashboardData"
					@toggle-action-menu="toggleActionMenu"
					@open-edit-modal="openEditModal"
					@delete-transaction="handleDeleteTransaction"
					@close-edit-modal="closeEditModal"
					@update:edit-form="updateEditFormState"
					@submit-edit="handleUpdateTransaction"
				/>
			</section>
		</main>
	</div>
</template>