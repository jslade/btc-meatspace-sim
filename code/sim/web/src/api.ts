import type { Entity, Transaction, Stats, Node, Message } from './types';

const API_BASE = '/api';

export const api = {
  // Legacy Entity APIs
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

  // Legacy Transaction APIs
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

  // Node APIs
  async getNodes(): Promise<Node[]> {
    const res = await fetch(`${API_BASE}/nodes`);
    return res.json();
  },

  async registerNode(id?: string, name?: string, ip_address?: string): Promise<Node> {
    const res = await fetch(`${API_BASE}/nodes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, name, ip_address }),
    });
    return res.json();
  },

  // Message APIs
  async getMessages(node_id?: string, status?: string): Promise<Message[]> {
    const params = new URLSearchParams();
    if (node_id) params.append('node_id', node_id);
    if (status) params.append('status', status);
    
    const res = await fetch(`${API_BASE}/messages?${params}`);
    return res.json();
  },

  async sendMessage(
    from_node_id: string,
    content: any,
    to_node_id?: string,
    is_broadcast?: boolean,
    qr_data?: string
  ): Promise<Message> {
    const res = await fetch(`${API_BASE}/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from_node_id,
        to_node_id,
        content,
        is_broadcast,
        qr_data,
        message_type: 'transaction'
      }),
    });
    return res.json();
  },

  async updateMessageStatus(message_id: number, status: string): Promise<Message> {
    const res = await fetch(`${API_BASE}/messages/${message_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    return res.json();
  },
};
