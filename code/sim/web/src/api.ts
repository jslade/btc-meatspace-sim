import type { Settings, Peer, Message, Wallet, Transaction, Block } from './types';

const API_BASE = '/api';

export const api = {
  // Settings
  async getSettings(): Promise<Settings> {
    const res = await fetch(`${API_BASE}/settings`);
    return res.json();
  },

  async updateSettings(settings: Partial<Settings>): Promise<Settings> {
    const res = await fetch(`${API_BASE}/settings`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings),
    });
    return res.json();
  },

  // Peers
  async getPeers(): Promise<Peer[]> {
    const res = await fetch(`${API_BASE}/peers`);
    return res.json();
  },

  async createPeer(name: string): Promise<Peer> {
    const res = await fetch(`${API_BASE}/peers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    return res.json();
  },

  // Messages
  async getMessages(): Promise<Message[]> {
    const res = await fetch(`${API_BASE}/messages`);
    return res.json();
  },

  async createMessage(peer_id: number, content: string): Promise<Message> {
    const res = await fetch(`${API_BASE}/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ peer_id, content }),
    });
    return res.json();
  },

  // Wallets
  async getWallets(): Promise<Wallet[]> {
    const res = await fetch(`${API_BASE}/wallets`);
    return res.json();
  },

  async createWallet(name: string, salt: string, secret: string, pubkey: string): Promise<Wallet> {
    const res = await fetch(`${API_BASE}/wallets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, salt, secret, pubkey }),
    });
    return res.json();
  },

  // Transactions
  async getTransactions(): Promise<Transaction[]> {
    const res = await fetch(`${API_BASE}/transactions`);
    return res.json();
  },

  async createTransaction(transaction: Partial<Transaction>): Promise<Transaction> {
    const res = await fetch(`${API_BASE}/transactions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(transaction),
    });
    return res.json();
  },

  // Blocks
  async getBlocks(): Promise<Block[]> {
    const res = await fetch(`${API_BASE}/blocks`);
    return res.json();
  },

  async createBlock(block: Partial<Block>): Promise<Block> {
    const res = await fetch(`${API_BASE}/blocks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(block),
    });
    return res.json();
  },
};
