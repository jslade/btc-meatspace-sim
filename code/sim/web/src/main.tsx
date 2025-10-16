import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { BlockchainApp } from './BlockchainApp.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BlockchainApp />
  </StrictMode>,
)
