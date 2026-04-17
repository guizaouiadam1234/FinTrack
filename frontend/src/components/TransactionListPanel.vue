<script setup>
const props = defineProps({
	loading: {
		type: Boolean,
		default: false
	},
	errorMessage: {
		type: String,
		default: ''
	},
	rowActionErrorMessage: {
		type: String,
		default: ''
	},
	transactions: {
		type: Array,
		required: true
	},
	actionMenuOpenId: {
		type: Number,
		default: null
	},
	editingTransaction: {
		type: Object,
		default: null
	},
	editForm: {
		type: Object,
		required: true
	},
	isSavingEdit: {
		type: Boolean,
		default: false
	},
	editErrorMessage: {
		type: String,
		default: ''
	}
})

const emit = defineEmits([
	'refresh',
	'toggle-action-menu',
	'open-edit-modal',
	'delete-transaction',
	'close-edit-modal',
	'update:editForm',
	'submit-edit'
])

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

const updateEditField = (field, value) => {
	emit('update:editForm', {
		...props.editForm,
		[field]: value
	})
}
</script>

<template>
	<article class="rounded-2xl border border-blue-300/20 bg-[#0a142db8] p-5 shadow-[0_18px_48px_rgba(0,0,0,0.45)] backdrop-blur-sm sm:p-6">
		<div class="flex flex-wrap items-center justify-between gap-3">
			<h2 class="text-lg font-semibold tracking-wide text-blue-50">Recent Transactions</h2>
			<button
				type="button"
				@click="emit('refresh')"
				class="rounded-lg border border-blue-300/35 bg-blue-500/15 px-3 py-1.5 text-xs font-medium uppercase tracking-[0.12em] text-blue-100 transition hover:bg-blue-500/30"
			>
				Refresh
			</button>
		</div>

		<p v-if="errorMessage" class="mt-4 rounded-lg border border-blue-300/30 bg-blue-900/35 px-3 py-2 text-sm text-blue-200">
			{{ errorMessage }}
		</p>

		<p v-if="rowActionErrorMessage" class="mt-3 rounded-lg border border-blue-300/30 bg-blue-900/35 px-3 py-2 text-sm text-blue-200">
			{{ rowActionErrorMessage }}
		</p>

		<div v-if="loading" class="mt-4 space-y-2">
			<div v-for="index in 6" :key="index" class="h-14 animate-pulse rounded-xl bg-blue-400/10"></div>
		</div>

		<ul v-else-if="transactions.length > 0" class="mt-4 divide-y divide-blue-300/12">
			<li v-for="transaction in transactions" :key="transaction.id" class="flex items-center justify-between gap-3 py-3">
				<div>
					<p class="text-sm font-medium text-blue-50">{{ transaction.title }}</p>
					<p class="text-xs text-blue-200/65">
						{{ transaction.category || 'Uncategorized' }} • {{ formatDate(transaction.date) }}
					</p>
				</div>
				<div class="flex items-center gap-3">
					<p class="text-sm font-semibold" :class="amountClass(transaction.type)">
						{{ amountPrefix(transaction.type) }}{{ formatCurrency(transaction.amount) }}
					</p>

					<div class="relative">
						<button
							type="button"
							@click="emit('toggle-action-menu', transaction.id)"
							class="rounded-md border border-blue-300/25 px-2 py-1 text-base leading-none text-blue-100 transition hover:bg-blue-500/20"
							aria-label="Transaction actions"
						>
							...
						</button>

						<div
							v-if="actionMenuOpenId === transaction.id"
							class="absolute right-0 z-20 mt-2 w-32 overflow-hidden rounded-lg border border-blue-300/25 bg-[#0c1734] shadow-[0_12px_28px_rgba(0,0,0,0.4)]"
						>
							<button
								type="button"
								@click="emit('open-edit-modal', transaction)"
								class="block w-full px-3 py-2 text-left text-xs font-medium uppercase tracking-[0.12em] text-blue-100 transition hover:bg-blue-500/20"
							>
								Edit
							</button>
							<button
								type="button"
								@click="emit('delete-transaction', transaction)"
								class="block w-full px-3 py-2 text-left text-xs font-medium uppercase tracking-[0.12em] text-blue-200 transition hover:bg-blue-500/20"
							>
								Delete
							</button>
						</div>
					</div>
				</div>
			</li>
		</ul>

		<p v-else class="mt-4 rounded-lg border border-blue-300/20 bg-blue-900/20 px-3 py-2 text-sm text-blue-200/80">
			No transactions yet. Add your first income or expense to populate this dashboard.
		</p>
	</article>

	<div v-if="editingTransaction" class="fixed inset-0 z-30 grid place-items-center bg-[#02050ec7] px-4 py-8">
		<div class="w-full max-w-md rounded-2xl border border-blue-300/25 bg-[#0a142d] p-5 shadow-[0_20px_60px_rgba(0,0,0,0.55)] sm:p-6">
			<div class="mb-4 flex items-center justify-between">
				<h3 class="text-lg font-semibold tracking-wide text-blue-50">Edit Transaction</h3>
				<button
					type="button"
					@click="emit('close-edit-modal')"
					class="rounded-md border border-blue-300/25 px-2 py-1 text-xs text-blue-100 transition hover:bg-blue-500/20"
				>
					Close
				</button>
			</div>

			<form class="space-y-3" @submit.prevent="emit('submit-edit')">
				<div>
					<label for="edit-title" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Title</label>
					<input
						id="edit-title"
						:value="editForm.title"
						@input="updateEditField('title', $event.target.value)"
						type="text"
						class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
						required
					/>
				</div>

				<div class="grid grid-cols-2 gap-3">
					<div>
						<label for="edit-amount" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Amount</label>
						<input
							id="edit-amount"
							:value="editForm.amount"
							@input="updateEditField('amount', $event.target.value)"
							type="number"
							step="0.01"
							min="0.01"
							class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
							required
						/>
					</div>

					<div>
						<label for="edit-type" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Type</label>
						<select
							id="edit-type"
							:value="editForm.type"
							@change="updateEditField('type', $event.target.value)"
							class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
						>
							<option value="expense">Expense</option>
							<option value="income">Income</option>
						</select>
					</div>
				</div>

				<div class="grid grid-cols-2 gap-3">
					<div>
						<label for="edit-category" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Category</label>
						<input
							id="edit-category"
							:value="editForm.category"
							@input="updateEditField('category', $event.target.value)"
							type="text"
							class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
						/>
					</div>

					<div>
						<label for="edit-date" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Date</label>
						<input
							id="edit-date"
							:value="editForm.date"
							@input="updateEditField('date', $event.target.value)"
							type="date"
							class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
						/>
					</div>
				</div>

				<p v-if="editErrorMessage" class="rounded-lg border border-blue-300/30 bg-blue-900/35 px-3 py-2 text-sm text-blue-200">
					{{ editErrorMessage }}
				</p>

				<button
					type="submit"
					:disabled="isSavingEdit"
					class="w-full rounded-xl bg-gradient-to-r from-blue-600 to-sky-400 px-4 py-2.5 text-xs font-semibold uppercase tracking-[0.12em] text-white transition hover:-translate-y-0.5 hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-70"
				>
					{{ isSavingEdit ? 'Saving...' : 'Save Changes' }}
				</button>
			</form>
		</div>
	</div>
</template>
