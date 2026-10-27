import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The app uses relative URLs only (/api, /ws). In dev they are proxied to the api-gateway;
// in Docker, nginx does the same (see nginx.conf).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:8080', changeOrigin: true },
      '/ws': { target: 'http://localhost:8080', ws: true, changeOrigin: true },
    },
  },
})
