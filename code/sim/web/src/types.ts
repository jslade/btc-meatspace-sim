// Legacy types for backward compatibility
export interface Entity {
  id: string;
  type: 'person' | 'merchant';
  x: number;
  y: number;
  btc: number;
  vx: number;
  vy: number;
}

export interface Transaction {
  id: number;
  from_id: string;
  to_id: string;
  amount: number;
  timestamp: string;
}

export interface Stats {
  people: number;
  merchants: number;
  transactions: number;
  total_btc: number;
}

// New types for network node functionality
export interface Node {
  id: string;
  name: string;
  ip_address?: string;
  is_active: boolean;
  last_seen?: string;
}

export interface Message {
  id: number;
  from_node_id: string;
  to_node_id?: string;
  message_type: string;
  content: string;
  qr_data?: string;
  status: 'pending' | 'processed' | 'archived';
  is_broadcast: boolean;
  timestamp: string;
  processed_at?: string;
}

export interface MessageContent {
  type: string;
  from: string;
  to?: string;
  amount?: number;
  data?: any;
}
