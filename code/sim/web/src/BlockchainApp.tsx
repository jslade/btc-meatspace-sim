import { useState } from 'react';
import type { AppMode } from './types';
import './BlockchainApp.css';

export function BlockchainApp() {
  const [mode, setMode] = useState<AppMode>('peers');

  return (
    <div className="blockchain-app">
      <div className="sidebar">
        <button
          className={`sidebar-btn ${mode === 'peers' ? 'active' : ''}`}
          onClick={() => setMode('peers')}
        >
          Peers
        </button>
        <button
          className={`sidebar-btn ${mode === 'send' ? 'active' : ''}`}
          onClick={() => setMode('send')}
        >
          Send
        </button>
        <button
          className={`sidebar-btn ${mode === 'rcvd' ? 'active' : ''}`}
          onClick={() => setMode('rcvd')}
        >
          Rcvd
        </button>
        <button
          className={`sidebar-btn ${mode === 'txns' ? 'active' : ''}`}
          onClick={() => setMode('txns')}
        >
          Txns
        </button>
        <button
          className={`sidebar-btn ${mode === 'blocks' ? 'active' : ''}`}
          onClick={() => setMode('blocks')}
        >
          Blocks
        </button>
        <button
          className={`sidebar-btn ${mode === 'wallet' ? 'active' : ''}`}
          onClick={() => setMode('wallet')}
        >
          Wallet
        </button>
      </div>

      <div className="main-content">
        <div className="content-header">
          <h1>{getModeTitle(mode)}</h1>
        </div>
        <div className="content-body">
          {/* Content will be added here */}
        </div>
      </div>
    </div>
  );
}

function getModeTitle(mode: AppMode): string {
  switch (mode) {
    case 'peers':
      return 'Peers';
    case 'send':
      return 'Send Message';
    case 'rcvd':
      return 'Received Messages';
    case 'txns':
      return 'Transactions';
    case 'blocks':
      return 'Blocks';
    case 'wallet':
      return 'Wallet';
  }
}
