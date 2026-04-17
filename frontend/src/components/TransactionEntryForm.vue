<script setup>
const props = defineProps({
	form: {
		type: Object,
		required: true
	},
	errorMessage: {
		type: String,
		default: ''
	},
	isCreating: {
		type: Boolean,
		default: false
	}
})

const emit = defineEmits(['update:form', 'submit'])

const updateField = (field, value) => {
	emit('update:form', {
		...props.form,
		[field]: value
	})
}
</script>

<template>
	<article class="rounded-2xl border border-blue-300/20 bg-[#0a142db8] p-5 shadow-[0_18px_48px_rgba(0,0,0,0.45)] backdrop-blur-sm sm:p-6">
		<h2 class="text-lg font-semibold tracking-wide text-blue-50">Add Transaction</h2>
		<p class="mt-1 text-xs text-blue-200/70">Create income or expense and refresh the dashboard instantly.</p>

		<form class="mt-4 space-y-3" @submit.prevent="emit('submit')">
			<div>
				<label for="title" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Title</label>
				<input
					id="title"
					:value="form.title"
					@input="updateField('title', $event.target.value)"
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
						:value="form.amount"
						@input="updateField('amount', $event.target.value)"
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
						:value="form.type"
						@change="updateField('type', $event.target.value)"
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
						:value="form.category"
						@input="updateField('category', $event.target.value)"
						type="text"
						placeholder="Optional"
						class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition placeholder:text-blue-300/40 focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
					/>
				</div>

				<div>
					<label for="date" class="mb-1 block text-xs uppercase tracking-[0.12em] text-blue-200/80">Date</label>
					<input
						id="date"
						:value="form.date"
						@input="updateField('date', $event.target.value)"
						type="date"
						class="w-full rounded-xl border border-blue-300/25 bg-blue-950/40 px-3 py-2 text-sm text-blue-50 outline-none transition focus:border-blue-200/60 focus:ring-4 focus:ring-blue-400/20"
					/>
				</div>
			</div>

			<p v-if="errorMessage" class="rounded-lg border border-blue-300/30 bg-blue-900/35 px-3 py-2 text-sm text-blue-200">
				{{ errorMessage }}
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
</template>
