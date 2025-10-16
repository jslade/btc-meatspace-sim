import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { NetworkNodeApp } from './NetworkNodeApp.tsx'

// Use NetworkNodeApp by default for network node functionality
// Import App from './App.tsx' for legacy simulation mode

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <NetworkNodeApp />
  </StrictMode>,
)
