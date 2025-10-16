# Bitcoin Blockchain Simulator

An educational Bitcoin blockchain simulator designed for hands-on learning. Each device acts as a network node where teams can interact with blockchain concepts through a touch-optimized interface.

## Overview

This application enables physical Bitcoin blockchain simulations where teams use devices (Raspberry Pi or desktop) to:
- Register as peers in the network
- Send and receive messages via plaintext
- Create and validate transactions
- Mine and view blocks
- Manage team wallets

## Architecture

### Frontend (`code/sim/web/`)
- **TypeScript + React 18** - Modern component-based UI
- **Vite** - Fast build tool and dev server
- **Touchscreen Optimized** - Full-screen interface designed for touch interaction
- **Mode-Based Navigation** - Six operational modes accessible via sidebar

### Backend (`code/sim/backend/`)
- **Python 3.11** - Modern Python runtime
- **Falcon** - Lightweight WSGI framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Persistent data storage
- **Service Layer Architecture** - Clean separation of concerns

## Quick Start

### Using Docker (Recommended)

```bash
cd code/sim
./runme.sh
```

Access at http://localhost

### Development Mode

**Backend:**
```bash
cd code/sim/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -b 0.0.0.0:8000 app.main:app --reload
```

**Frontend:**
```bash
cd code/sim/web
npm install
npm run dev
```

## Features

### Touchscreen Interface
- **Full-Screen Layout** - Maximizes display space
- **Sidebar Navigation** - Six mode buttons: Peers, Send, Rcvd, Txns, Blocks, Wallet

### Message System
- **Plaintext Messages** - Sent via touchscreen typing (no QR codes)
- **YAML-Style Parsing** - Messages with `key: value` format parsed into structured data
- **Best-Effort Extraction** - System attempts to populate object models from message content

### Blockchain Models
- Settings, Peers, Messages, Wallets, Transactions, Blocks
- Mining tracking with mined and pending transactions

## Message Format

Messages can be plain text or use YAML-style format:

```
type: transaction
from: Alice
to: Bob
amount: 50
```

## API Endpoints

- `GET/PUT /api/settings` - Blockchain configuration
- `GET/POST /api/peers` - Peer management
- `GET/POST /api/messages` - Message handling
- `GET/POST /api/wallets` - Wallet management
- `GET/POST /api/transactions` - Transaction operations
- `GET/POST /api/blocks` - Block management
- `GET /health` - Health check

## Code Structure

```
code/sim/
├── backend/app/
│   ├── models/       # Database models (one per file)
│   ├── services/     # Business logic layer
│   ├── resources/    # API controllers (thin)
│   └── main.py       # Application entry point
├── web/src/
│   ├── BlockchainApp.tsx
│   └── api.ts
├── docker-compose.yml
└── runme.sh
```

## License

See LICENSE file in repository root.
