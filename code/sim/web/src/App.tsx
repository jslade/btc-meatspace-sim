import { useState, useEffect } from 'react';
import type { Entity, Stats } from './types';
import { api } from './api';
import { SimulationCanvas } from './SimulationCanvas';
import './App.css';

const CONFIG = {
  TRANSACTION_PERCENTAGE: 0.3,
  TRANSACTION_MIN: 0.01,
  TRANSACTION_MAX: 0.06,
};

function App() {
  const [entities, setEntities] = useState<Entity[]>([]);
  const [stats, setStats] = useState<Stats>({ people: 0, merchants: 0, transactions: 0, total_btc: 0 });
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);
  const [isWalking, setIsWalking] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (message: string) => {
    const time = new Date().toLocaleTimeString();
    setLogs((prev) => [`[${time}] ${message}`, ...prev].slice(0, 20));
  };

  const fetchData = async () => {
    try {
      const [entitiesData, statsData] = await Promise.all([
        api.getEntities(),
        api.getStats(),
      ]);
      setEntities(entitiesData);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();
    addLog('Bitcoin Meatspace Simulator initialized');
    addLog('Add people and merchants to begin simulation');
  }, []);

  const addPerson = async () => {
    const x = Math.random() * 750 + 25;
    const y = Math.random() * 550 + 25;
    try {
      await api.createEntity('person', x, y);
      await fetchData();
      addLog(`Added new person at (${Math.floor(x)}, ${Math.floor(y)})`);
    } catch (error) {
      console.error('Error adding person:', error);
    }
  };

  const addMerchant = async () => {
    const x = Math.random() * 750 + 25;
    const y = Math.random() * 550 + 25;
    try {
      await api.createEntity('merchant', x, y);
      await fetchData();
      addLog(`Added new merchant at (${Math.floor(x)}, ${Math.floor(y)})`);
    } catch (error) {
      console.error('Error adding merchant:', error);
    }
  };

  const startTransaction = async () => {
    if (entities.length < 2) {
      addLog('Need at least 2 entities for a transaction');
      return;
    }

    const from = entities[Math.floor(Math.random() * entities.length)];
    let to: Entity;
    do {
      to = entities[Math.floor(Math.random() * entities.length)];
    } while (to.id === from.id);

    const amount = Math.min(
      from.btc * CONFIG.TRANSACTION_PERCENTAGE,
      CONFIG.TRANSACTION_MIN + Math.random() * (CONFIG.TRANSACTION_MAX - CONFIG.TRANSACTION_MIN)
    );

    if (from.btc < amount) {
      addLog('Insufficient BTC for transaction');
      return;
    }

    try {
      await api.createTransaction(from.id, to.id, amount);
      await fetchData();
      addLog(`Transaction: ${amount.toFixed(4)} BTC from ${from.type} to ${to.type}`);
    } catch (error) {
      console.error('Error creating transaction:', error);
    }
  };

  const reset = async () => {
    try {
      await api.deleteAllEntities();
      await fetchData();
      setSelectedEntity(null);
      setIsWalking(false);
      addLog('Simulation reset');
    } catch (error) {
      console.error('Error resetting:', error);
    }
  };

  const toggleRandomWalk = () => {
    setIsWalking(!isWalking);
    // Note: Random walk would require periodic updates via API or WebSocket
    // For now, just toggle the state
  };

  const handleEntityClick = (entity: Entity | null) => {
    setSelectedEntity(entity);
    if (entity) {
      addLog(`Selected ${entity.type} with ${entity.btc.toFixed(3)} BTC`);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>🏢 Bitcoin Meatspace Simulator</h1>
        <p className="subtitle">Simulate Bitcoin transactions in physical space</p>
      </header>

      <div className="simulation-area">
        <div className="controls">
          <h2>Simulation Controls</h2>
          <div className="control-group">
            <button onClick={addPerson} className="btn btn-primary">
              Add Person
            </button>
            <button onClick={addMerchant} className="btn btn-success">
              Add Merchant
            </button>
            <button onClick={reset} className="btn btn-danger">
              Reset
            </button>
          </div>
          <div className="control-group">
            <button onClick={startTransaction} className="btn btn-warning">
              Start Transaction
            </button>
            <button
              onClick={toggleRandomWalk}
              className={`btn ${isWalking ? 'btn-danger' : 'btn-info'}`}
            >
              {isWalking ? 'Stop Walking' : 'Random Walk'}
            </button>
          </div>
        </div>

        <div className="canvas-container">
          <SimulationCanvas
            entities={entities}
            selectedEntity={selectedEntity}
            onEntityClick={handleEntityClick}
          />
        </div>

        <div className="stats">
          <h3>Statistics</h3>
          <div className="stat-grid">
            <div className="stat-item">
              <span className="stat-label">People:</span>
              <span className="stat-value">{stats.people}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Merchants:</span>
              <span className="stat-value">{stats.merchants}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Transactions:</span>
              <span className="stat-value">{stats.transactions}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Total BTC:</span>
              <span className="stat-value">{stats.total_btc.toFixed(3)}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="transaction-log">
        <h3>Transaction Log</h3>
        <div className="log-entries">
          {logs.map((log, i) => (
            <div key={i} className="log-entry">
              {log}
            </div>
          ))}
        </div>
      </div>

      <footer>
        <p>Click on the canvas to select entities • Use controls to simulate Bitcoin transactions</p>
      </footer>
    </div>
  );
}

export default App;
