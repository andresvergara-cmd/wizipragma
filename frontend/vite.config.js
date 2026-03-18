import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import path from 'path'

// Check if HTTPS certificates exist
const certPath = path.resolve(__dirname, 'localhost.pem')
const keyPath = path.resolve(__dirname, 'localhost-key.pem')
const httpsEnabled = fs.existsSync(certPath) && fs.existsSync(keyPath)

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
    https: httpsEnabled ? {
      key: fs.readFileSync(keyPath),
      cert: fs.readFileSync(certPath),
    } : undefined
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})
