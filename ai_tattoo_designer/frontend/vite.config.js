import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: 'dist',  // Required by Render to know what to publish
  },
  server: {
    host: true,       // Allows Render to bind to external network
    port: 4173        // Optional but helpful if you want consistent local + cloud
  }
})
