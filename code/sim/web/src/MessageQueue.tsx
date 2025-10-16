import { useState } from 'react';
import type { Message } from './types';
import { QRDisplay } from './QRDisplay';

interface MessageQueueProps {
  messages: Message[];
  onProcess: (messageId: number) => void;
  onArchive: (messageId: number) => void;
}

export function MessageQueue({ messages, onProcess, onArchive }: MessageQueueProps) {
  const [expandedMessage, setExpandedMessage] = useState<number | null>(null);

  const toggleExpand = (messageId: number) => {
    setExpandedMessage(expandedMessage === messageId ? null : messageId);
  };

  const parseContent = (content: string) => {
    try {
      return JSON.parse(content);
    } catch {
      return content;
    }
  };

  return (
    <div className="message-queue">
      <h2>Message Queue</h2>
      
      {messages.length === 0 ? (
        <div className="empty-state">
          <p>No messages in queue</p>
        </div>
      ) : (
        <div className="message-list">
          {messages.map((message) => {
            const isExpanded = expandedMessage === message.id;
            const parsedContent = parseContent(message.content);

            return (
              <div
                key={message.id}
                className={`message-item ${message.status}`}
                onClick={() => toggleExpand(message.id)}
              >
                <div className="message-header">
                  <div className="message-info">
                    <span className="message-type">{message.message_type}</span>
                    {message.is_broadcast && (
                      <span className="broadcast-badge">BROADCAST</span>
                    )}
                    <span className="message-from">From: {message.from_node_id}</span>
                    <span className="message-time">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <div className="message-status">
                    <span className={`status-badge status-${message.status}`}>
                      {message.status}
                    </span>
                  </div>
                </div>

                {isExpanded && (
                  <div className="message-body">
                    <div className="message-content">
                      <h4>Content:</h4>
                      <pre>{JSON.stringify(parsedContent, null, 2)}</pre>
                    </div>

                    {message.qr_data && (
                      <div className="message-qr">
                        <h4>QR Code:</h4>
                        <QRDisplay data={message.qr_data} size={200} />
                      </div>
                    )}

                    <div className="message-actions">
                      {message.status === 'pending' && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onProcess(message.id);
                          }}
                          className="btn btn-success"
                        >
                          Mark as Processed
                        </button>
                      )}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onArchive(message.id);
                        }}
                        className="btn btn-secondary"
                      >
                        Archive
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
