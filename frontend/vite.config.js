import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      '/predict': 'http://localhost:8000',
      '/analyze-resume': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    },
  },
})
