<template>
    <div class="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_15%_20%,rgba(47,112,255,0.33),transparent_38%),radial-gradient(circle_at_88%_10%,rgba(25,71,200,0.32),transparent_36%),linear-gradient(135deg,#05080f,#0a1226)] px-3 py-8 text-blue-50 sm:px-5">
        <div class="pointer-events-none absolute -bottom-24 -left-24 h-80 w-80 rounded-full bg-[radial-gradient(circle,rgba(74,164,255,0.14),transparent_68%)]" aria-hidden="true"></div>
        <div class="pointer-events-none absolute -right-20 -top-28 h-80 w-80 rounded-full bg-[radial-gradient(circle,rgba(74,164,255,0.14),transparent_68%)]" aria-hidden="true"></div>

        <section class="relative z-10 mx-auto grid w-full max-w-6xl overflow-hidden rounded-3xl border border-blue-300/20 bg-[#070d1cd6] shadow-[0_24px_70px_rgba(0,0,0,0.55)] backdrop-blur-md lg:min-h-[560px] lg:grid-cols-[1.05fr_1fr]">
            <div class="animate-[fadeup_.6s_ease-out_both] border-b border-blue-300/20 bg-[linear-gradient(165deg,rgba(33,74,194,0.18),transparent_72%),linear-gradient(10deg,rgba(74,164,255,0.08),transparent_50%)] px-7 py-10 sm:px-10 lg:border-b-0 lg:border-r lg:py-14">
                <p class="inline-block rounded-full border border-blue-300/35 px-3 py-1 text-xs uppercase tracking-[0.1em] text-blue-200/85">FinTrack</p>
                <h1 class="mt-4 text-4xl font-semibold leading-tight tracking-wide text-blue-50 sm:text-5xl">Welcome Back</h1>
                <p class="mt-4 max-w-xl text-base leading-8 text-blue-200/75 lg:max-w-md">
                    Sign in to monitor your balances, analyze spending, and stay in control of every transaction.
                </p>
            </div>

            <div class="animate-[fadeup_.68s_ease-out_both] px-6 py-8 sm:px-10 sm:py-10 lg:grid lg:items-center lg:px-10">
                <form class="mx-auto w-full max-w-md" @submit.prevent="handleLogin">
                    <h2 class="mb-6 text-3xl font-semibold tracking-wide text-blue-50">Login</h2>

                    <label for="username" class="mb-2 mt-3 block text-sm tracking-wide text-blue-200/90">Username</label>
                    <input
                        id="username"
                        v-model.trim="username"
                        type="text"
                        autocomplete="username"
                        placeholder="Enter your username"
                        class="w-full rounded-xl border border-blue-400/30 bg-blue-950/45 px-4 py-3 text-blue-50 outline-none transition duration-200 placeholder:text-blue-300/45 focus:border-blue-300/90 focus:bg-blue-950/65 focus:ring-4 focus:ring-blue-400/20"
                        required
                    />

                    <label for="password" class="mb-2 mt-4 block text-sm tracking-wide text-blue-200/90">Password</label>
                    <input
                        id="password"
                        v-model="password"
                        type="password"
                        autocomplete="current-password"
                        placeholder="Enter your password"
                        class="w-full rounded-xl border border-blue-400/30 bg-blue-950/45 px-4 py-3 text-blue-50 outline-none transition duration-200 placeholder:text-blue-300/45 focus:border-blue-300/90 focus:bg-blue-950/65 focus:ring-4 focus:ring-blue-400/20"
                        required
                    />

                    <p v-if="errorMessage" class="mt-3 text-sm text-blue-300" role="alert">{{ errorMessage }}</p>

                    <button
                        type="submit"
                        :disabled="isSubmitting"
                        class="mt-5 w-full rounded-xl bg-gradient-to-r from-blue-600 to-sky-400 px-4 py-3 text-sm font-semibold uppercase tracking-[0.12em] text-white transition duration-200 hover:-translate-y-0.5 hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-70"
                    >
                        {{ isSubmitting ? 'Signing in...' : 'Sign in' }}
                    </button>

                    <p class="mt-5 text-center text-sm text-blue-200/70">
                        New here?
                        <RouterLink to="/register" class="ml-1 border-b border-blue-300/50 text-blue-300 transition hover:text-blue-100">Create an account</RouterLink>
                    </p>
                </form>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../router/auth'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

const handleLogin = async () => {
    errorMessage.value = ''
    isSubmitting.value = true

    try {
        await authStore.login(username.value, password.value)
        await router.push('/dashboard')
    } catch (error) {
        const apiMessage = error?.response?.data?.detail
        errorMessage.value = apiMessage || 'Unable to login. Please check your credentials and try again.'
    } finally {
        isSubmitting.value = false
    }
}
</script>
