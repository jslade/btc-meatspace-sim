import type { Entity, Transaction, Stats } from './types';

const API_BASE = '/api';

export const api = {
  // Entities
  async getEntities(): Promise<Entity[]> {
    const res = await fetch(`${API_BASE}/entities`);
    return res.json();
  },

  async createEntity(type: 'person' | 'merchant', x: number, y: number): Promise<Entity> {
    const res = await fetch(`${API_BASE}/entities`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, x, y }),
    });
    return res.json();
  },

  async updateEntity(id: string, data: Partial<Entity>): Promise<Entity> {
    const res = await fetch(`${API_BASE}/entities/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  async deleteAllEntities(): Promise<void> {
    await fetch(`${API_BASE}/entities`, { method: 'DELETE' });
  },

  // Transactions
  async getTransactions(): Promise<Transaction[]> {
    const res = await fetch(`${API_BASE}/transactions`);
    return res.json();
  },

  async createTransaction(from_id: string, to_id: string, amount: number): Promise<Transaction> {
    const res = await fetch(`${API_BASE}/transactions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ from_id, to_id, amount }),
    });
    return res.json();
  },

  // Stats
  async getStats(): Promise<Stats> {
    const res = await fetch(`${API_BASE}/stats`);
    return res.json();
  },
};
