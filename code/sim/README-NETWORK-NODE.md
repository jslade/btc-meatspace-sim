# Bitcoin Network Node Application - User Guide

## Overview

This application turns each Raspberry Pi device into a network node for a physical Bitcoin simulation game. Teams/groups use QR codes to send transactions and messages to each other over a local network.

## How It Works

### Physical Setup
- Each team has a Raspberry Pi with:
  - Camera for scanning QR codes
  - Display showing the web interface
  - Network connection (local wired LAN)

### Game Flow

1. **Node Registration**
   - Each device automatically registers as a node on startup
   - Nodes can discover other active nodes on the network

2. **Scanning QR Codes**
   - Users hand-generate QR codes with transaction instructions
   - Click "Show Scanner" to activate the camera
   - Point camera at QR code to scan
   - Scanned data appears for confirmation

3. **Sending Messages**
   - Review scanned content or manually enter message
   - Choose to broadcast to all nodes or send to specific node
   - Message is displayed as QR code for verification
   - Click "Send Message" to transmit

4. **Receiving Messages**
   - Incoming messages appear in "Received Messages" section
   - Each message shows:
     - QR code representation
     - Decoded content
     - Sender information
     - Timestamp
   - Messages start as "pending"

5. **Processing Messages**
   - Click on a message to expand and view details
   - Click "Mark as Processed" when team has acted on it
   - Processed messages move to history
   - Messages remain in order received

## Features

### QR Code Scanning
- Uses device camera to scan QR codes
- Real-time scanning with visual feedback
- Automatic decode and display

### Message Queue
- **Pending Messages**: Require action from the team
- **Processed Messages**: Already handled, kept in history
- **Archived Messages**: Removed from active queue
- Order-preserving - messages stay in sequence

### Network Communication
- **Broadcast**: Send to all nodes simultaneously
- **Targeted Send**: Send to specific node
- **Real-time Updates**: Polls for new messages every 5 seconds
- **Node Discovery**: Automatically finds other devices

### Display Features
- Shows scanned QR codes visually
- Displays message content as both QR and text
- Activity log tracks all actions
- Network status shows connected nodes

## Message Format

Messages can be any text, but JSON format is recommended:

```json
{
  "type": "transaction",
  "from": "Alice",
  "to": "Bob",
  "amount": 0.5,
  "memo": "Payment for coffee"
}
```

## Controls

### Main Interface
- **Show Scanner**: Open camera for QR scanning
- **Target Dropdown**: Choose broadcast or specific node
- **Message Content**: Enter or view scanned message
- **Send Message**: Transmit to network
- **Message Queue**: View and process received messages

### Message Actions
- **Mark as Processed**: Move message to processed state
- **Archive**: Remove from active queue
- **Expand/Collapse**: Click message to view details

## Network Status

The interface shows:
- **Active Nodes**: Number of devices on network
- **Pending Messages**: Messages requiring action
- **Total Messages**: All messages (pending + processed)

## Activity Log

Tracks all actions:
- Node registration
- QR code scans
- Messages sent/received
- Status changes

## Tips for Use

1. **Generating QR Codes**
   - Use any QR code generator
   - Keep messages under 400 characters for reliability
   - Use JSON format for structured data

2. **Message Processing**
   - Process messages in order received
   - Review message details before processing
   - Use activity log to track what you've done

3. **Network Communication**
   - Use broadcast for announcements
   - Use targeted sends for private transactions
   - Check network status to see connected nodes

4. **Camera Usage**
   - Ensure good lighting for scanning
   - Hold QR code steady
   - Position QR code within the frame outline

## API Endpoints

For programmatic access:

- `GET /api/nodes` - List all nodes
- `POST /api/nodes` - Register a node
- `GET /api/messages?node_id={id}` - Get messages for node
- `POST /api/messages` - Send a message
- `PUT /api/messages/{id}` - Update message status

## Troubleshooting

### Camera Not Working
- Check browser permissions for camera access
- Ensure device has camera connected
- Try refreshing the page

### Messages Not Appearing
- Check network connection
- Verify other nodes are online
- Check network status panel

### QR Scan Issues
- Improve lighting
- Clean camera lens
- Generate larger QR codes
- Reduce message size

## Development

To run locally:

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -b 0.0.0.0:8000 app.main:app

# Frontend  
cd web
npm install
npm run dev
```

Visit http://localhost:5173

## Deployment

See [README-DEPLOYMENT.md](./README-DEPLOYMENT.md) for Raspberry Pi deployment instructions.

Quick deploy:
```bash
./deploy-pi.sh
```
