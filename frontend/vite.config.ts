import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Configuração do Vite para BiotecPredict
 * 
 * @see https://vitejs.dev/config/
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: false,
    host: '0.0.0.0',
    proxy: {
      '/api': 'http://localhost:8001',
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
  },
})
