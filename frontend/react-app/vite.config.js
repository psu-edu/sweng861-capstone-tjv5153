import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // This sets the host to 0.0.0.0
    port: 5173, // Set a consistent port (default is 5173)
  },
  test: {
    globals: true,           // Allows using 'describe', 'it', 'expect' without imports
    environment: 'jsdom',    // Simulates a browser environment
    setupFiles: './src/test/setup.js',
  },
})
