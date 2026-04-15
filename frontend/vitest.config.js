import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  test: {
    environment: 'happy-dom',
    setupFiles: ['./tests/setup.js'],
    include: ['src/**/*.{unit,int}.spec.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['src/**/*.{js,vue}'],
      exclude: ['src/main.js', 'src/style.css', 'src/assets/**'],
      thresholds: {
        lines: 80,
        statements: 80,
        functions: 80,
        branches: 70
      }
    }
  }
})
