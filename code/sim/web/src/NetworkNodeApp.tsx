import { useState, useEffect } from 'react';
import type { Node, Message } from './types';
import { api } from './api';
import { QRScanner } from './QRScanner';
import { QRDisplay } from './QRDisplay';
import { MessageQueue } from './MessageQueue';
import './App.css';

export function NetworkNodeApp() {
  const [currentNode, setCurrentNode] = useState<Node | null>(null);
  const [nodes, setNodes] = useState<Node[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [scannedData, setScannedData] = useState<string>('');
  const [showScanner, setShowScanner] = useState(false);
  const [messageContent, setMessageContent] = useState('');
  const [selectedTarget, setSelectedTarget] = useState<string>('broadcast');
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (message: string) => {
    const time = new Date().toLocaleTimeString();
    setLogs((prev) => [`[${time}] ${message}`, ...prev].slice(0, 20));
  };

  const initializeNode = async () => {
    try {
      // Register this node
      const node = await api.registerNode(
        undefined,
        `Node-${Math.random().toString(36).substr(2, 6)}`
      );
      setCurrentNode(node);
      addLog(`Registered as node: ${node.name}`);
    } catch (error) {
      console.error('Error initializing node:', error);
      addLog('Error initializing node');
    }
  };

  const fetchNodes = async () => {
    try {
      const nodeList = await api.getNodes();
      setNodes(nodeList.filter(n => n.id !== currentNode?.id));
    } catch (error) {
      console.error('Error fetching nodes:', error);
    }
  };

  const fetchMessages = async () => {
    if (!currentNode) return;
    
    try {
      const msgs = await api.getMessages(currentNode.id, 'all');
      setMessages(msgs);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  useEffect(() => {
    initializeNode();
  }, []);

  useEffect(() => {
    if (currentNode) {
      fetchNodes();
      fetchMessages();
      
      // Poll for new messages every 5 seconds
      const interval = setInterval(() => {
        fetchMessages();
        fetchNodes();
      }, 5000);
      
      return () => clearInterval(interval);
    }
  }, [currentNode]);

  const handleScan = (data: string) => {
    setScannedData(data);
    setShowScanner(false);
    addLog(`Scanned QR code: ${data.substring(0, 50)}...`);
    
    // Try to parse as JSON
    try {
      const parsed = JSON.parse(data);
      setMessageContent(JSON.stringify(parsed, null, 2));
    } catch {
      setMessageContent(data);
    }
  };

  const handleSendMessage = async () => {
    if (!currentNode || !messageContent) return;

    try {
      const isBroadcast = selectedTarget === 'broadcast';
      const toNodeId = isBroadcast ? undefined : selectedTarget;

      await api.sendMessage(
        currentNode.id,
        messageContent,
        toNodeId,
        isBroadcast,
        scannedData
      );

      addLog(
        isBroadcast
          ? 'Broadcast message sent'
          : `Message sent to ${toNodeId}`
      );

      // Clear form
      setMessageContent('');
      setScannedData('');
      
      // Refresh messages
      fetchMessages();
    } catch (error) {
      console.error('Error sending message:', error);
      addLog('Error sending message');
    }
  };

  const handleProcessMessage = async (messageId: number) => {
    try {
      await api.updateMessageStatus(messageId, 'processed');
      addLog(`Message ${messageId} marked as processed`);
      fetchMessages();
    } catch (error) {
      console.error('Error processing message:', error);
    }
  };

  const handleArchiveMessage = async (messageId: number) => {
    try {
      await api.updateMessageStatus(messageId, 'archived');
      addLog(`Message ${messageId} archived`);
      fetchMessages();
    } catch (error) {
      console.error('Error archiving message:', error);
    }
  };

  const pendingMessages = messages.filter(m => m.status === 'pending');
  const processedMessages = messages.filter(m => m.status === 'processed');

  return (
    <div className="container">
      <header>
        <h1>🌐 Bitcoin Network Node</h1>
        <p className="subtitle">
          {currentNode ? `Node: ${currentNode.name}` : 'Initializing...'}
        </p>
      </header>

      <div className="simulation-area">
        {/* QR Scanning Section */}
        <div className="section">
          <h2>Scan QR Code</h2>
          <button
            onClick={() => setShowScanner(!showScanner)}
            className="btn btn-primary"
          >
            {showScanner ? 'Hide Scanner' : 'Show Scanner'}
          </button>
          
          {showScanner && (
            <div style={{ marginTop: '15px' }}>
              <QRScanner onScan={handleScan} />
            </div>
          )}

          {scannedData && (
            <div className="scanned-data">
              <h3>Scanned Data:</h3>
              <div className="qr-preview">
                <QRDisplay data={scannedData} size={150} />
              </div>
              <pre>{scannedData}</pre>
            </div>
          )}
        </div>

        {/* Message Composition Section */}
        <div className="section">
          <h2>Send Message</h2>
          <div className="message-form">
            <div className="form-group">
              <label>Target:</label>
              <select
                value={selectedTarget}
                onChange={(e) => setSelectedTarget(e.target.value)}
                className="form-control"
              >
                <option value="broadcast">Broadcast to All</option>
                {nodes.map((node) => (
                  <option key={node.id} value={node.id}>
                    {node.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Message Content:</label>
              <textarea
                value={messageContent}
                onChange={(e) => setMessageContent(e.target.value)}
                className="form-control"
                rows={5}
                placeholder='{"type": "transaction", "amount": 0.5, "from": "Alice", "to": "Bob"}'
              />
            </div>

            {messageContent && (
              <div className="message-preview">
                <h4>Preview:</h4>
                <QRDisplay data={messageContent} size={200} />
              </div>
            )}

            <button
              onClick={handleSendMessage}
              disabled={!messageContent || !currentNode}
              className="btn btn-success"
            >
              Send Message
            </button>
          </div>
        </div>

        {/* Received Messages Section */}
        <div className="section">
          <h2>Received Messages</h2>
          <div className="tabs">
            <button className="tab active">
              Pending ({pendingMessages.length})
            </button>
            <button className="tab">
              Processed ({processedMessages.length})
            </button>
          </div>

          <MessageQueue
            messages={pendingMessages}
            onProcess={handleProcessMessage}
            onArchive={handleArchiveMessage}
          />

          {processedMessages.length > 0 && (
            <details style={{ marginTop: '20px' }}>
              <summary>Show Processed Messages ({processedMessages.length})</summary>
              <MessageQueue
                messages={processedMessages}
                onProcess={handleProcessMessage}
                onArchive={handleArchiveMessage}
              />
            </details>
          )}
        </div>

        {/* Network Status */}
        <div className="section stats">
          <h3>Network Status</h3>
          <div className="stat-grid">
            <div className="stat-item">
              <span className="stat-label">Active Nodes:</span>
              <span className="stat-value">{nodes.length + 1}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Pending Messages:</span>
              <span className="stat-value">{pendingMessages.length}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Total Messages:</span>
              <span className="stat-value">{messages.length}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Activity Log */}
      <div className="transaction-log">
        <h3>Activity Log</h3>
        <div className="log-entries">
          {logs.map((log, i) => (
            <div key={i} className="log-entry">
              {log}
            </div>
          ))}
        </div>
      </div>

      <footer>
        <p>Scan QR codes to receive • Compose and send messages to network nodes</p>
      </footer>
    </div>
  );
}
