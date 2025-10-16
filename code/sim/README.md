# Bitcoin Meatspace Simulator

A full-stack web application that simulates Bitcoin transactions in physical space (meatspace).

## Architecture

This application uses a modern full-stack architecture:

- **Frontend**: TypeScript + React (Vite) - located in `web/`
- **Backend**: Python 3 + Falcon + SQLAlchemy + SQLite - located in `backend/`
- **Orchestration**: Docker Compose
- **Deployment**: Optimized for Raspberry Pi

## Features

- **Interactive Canvas**: Visual representation of people and merchants in a physical space
- **Entity Management**: Add people (blue) and merchants (green) to the simulation via REST API
- **Bitcoin Transactions**: Simulate Bitcoin transactions between entities with persistence
- **Random Walk**: Make entities move around the space randomly
- **Real-time Statistics**: Track the number of people, merchants, transactions, and total BTC
- **Transaction Log**: View a detailed log of all activities and transactions
- **Persistent Storage**: SQLite database stores all entities and transactions

## Quick Start

### Using Docker Compose (Recommended)

```bash
docker-compose up --build
```

Then open http://localhost in your browser.

### Development Mode

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -b 0.0.0.0:8000 app.main:app
```

**Frontend:**
```bash
cd web
npm install
npm run dev
```

## Deployment to Raspberry Pi

See [README-DEPLOYMENT.md](./README-DEPLOYMENT.md) for detailed deployment instructions.

Quick deployment:
```bash
./deploy-pi.sh
```

## Project Structure

```
code/sim/
├── backend/              # Python Falcon backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py      # Falcon app
│   │   ├── models.py    # SQLAlchemy models
│   │   ├── database.py  # Database setup
│   │   └── resources.py # API endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── web/                  # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx      # Main app component
│   │   ├── SimulationCanvas.tsx
│   │   ├── api.ts       # API client
│   │   └── types.ts     # TypeScript types
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml    # Container orchestration
├── deploy-pi.sh         # Raspberry Pi deployment script
└── README-DEPLOYMENT.md # Deployment guide
```

## API Endpoints

### Entities
- `GET /api/entities` - List all entities
- `POST /api/entities` - Create entity
- `GET /api/entities/{id}` - Get specific entity
- `PUT /api/entities/{id}` - Update entity
- `DELETE /api/entities` - Delete all entities

### Transactions
- `GET /api/transactions` - List all transactions
- `POST /api/transactions` - Create transaction

### Statistics
- `GET /api/stats` - Get simulation statistics

## Technologies

### Frontend
- TypeScript
- React 18
- Vite (build tool)
- HTML5 Canvas API

### Backend
- Python 3.11
- Falcon (WSGI framework)
- SQLAlchemy (ORM)
- SQLite (database)
- Gunicorn (WSGI server)

### DevOps
- Docker & Docker Compose
- Nginx (production frontend server)
- Systemd (auto-start service)

## Simulation Details

- Each entity starts with a random amount of BTC (0 to 0.5 BTC)
- Transactions transfer up to 30% of the sender's balance (capped at 0.01-0.06 BTC)
- The canvas shows a grid representing physical space
- Entities are visualized with icons (👤 for people, 🏪 for merchants)
- All data is persisted in SQLite database

## Legacy Files

The original static HTML/JS/CSS files are still present in this directory for reference:
- `index.html` - Original static version
- `app.js` - Original JavaScript implementation
- `style.css` - Original styling

These are superseded by the new `web/` and `backend/` directories.
