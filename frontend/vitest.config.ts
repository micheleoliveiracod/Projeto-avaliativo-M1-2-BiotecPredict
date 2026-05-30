import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

/**
 * Configuração do Vitest para BiotecPredict
 * 
 * @see https://vitest.dev/config/
 */
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: [],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'dist/',
      ]
    }
  }
})
