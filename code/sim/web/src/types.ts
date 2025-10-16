// Types for blockchain simulator
export interface Settings {
  block_reward: number;
  difficulty_target: number;
}

export interface Peer {
  id: number;
  name: string;
  heartbeat?: string;
}

export interface Message {
  id: number;
  peer_id: number;
  timestamp: string;
  content: string;
  read: boolean;
  processed: boolean;
}

export interface Wallet {
  id: number;
  name: string;
  salt: string;
  pubkey: string;
}

export interface Transaction {
  id: number;
  peer_id?: number;
  name?: string;
  amount?: number;
  input_txn_id_1?: string;
  input_txn_sig_1?: string;
  input_txn_id_2?: string;
  input_txn_sig_2?: string;
  output_amount_1?: number;
  output_pk_1?: string;
  output_amount_2?: number;
  output_pk_2?: string;
  output_amount_3?: number;
  output_pk_3?: string;
  output_amount_4?: number;
  output_pk_4?: string;
  output_amount_5?: number;
  output_pk_5?: string;
}

export interface Block {
  id: number;
  peer_id?: number;
  commitment?: string;
  timestamp: string;
  target?: number;
  nonce?: string;
  hash?: string;
}

export type AppMode = 'peers' | 'send' | 'rcvd' | 'txns' | 'blocks' | 'wallet';
