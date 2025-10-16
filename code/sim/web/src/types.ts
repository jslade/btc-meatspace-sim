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
