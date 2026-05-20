import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

const rawBasePath = process.env.WEBSITE_BASE_PATH?.trim().replace(/\/+$/, '')
const basePath = rawBasePath
  ? `/${rawBasePath.replace(/^\/+/, '')}/`
  : '/'

export default defineConfig({
  base: basePath,
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/healthz': 'http://localhost:8000',
    },
  },
  test: {
    environment: 'happy-dom',
    setupFiles: ['./src/test-setup.ts'],
    globals: true,
  },
})
