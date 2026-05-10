/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    alias: {
      'react-leaflet': '/src/test/__mocks__/react-leaflet.tsx',
      'leaflet/dist/leaflet.css': '/src/test/__mocks__/empty.css',
    },
  },
})
