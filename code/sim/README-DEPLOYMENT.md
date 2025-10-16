# Bitcoin Meatspace Simulator - Deployment Guide

This guide covers deployment of the full-stack Bitcoin Meatspace Simulator, optimized for Raspberry Pi.

## Architecture

- **Frontend**: TypeScript + React (Vite) - `web/`
- **Backend**: Python 3 + Falcon + SQLAlchemy + SQLite - `backend/`
- **Orchestration**: Docker Compose
- **Target**: Raspberry Pi (ARM architecture)

## Prerequisites

### For Development
- Node.js 20+
- Python 3.11+
- Docker and Docker Compose

### For Raspberry Pi Deployment
- Raspberry Pi 3B+ or newer
- Raspberry Pi OS (64-bit recommended)
- Docker and Docker Compose installed on Pi

## Quick Start (Development)

### Backend Only
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
gunicorn -b 0.0.0.0:8000 app.main:app
```

### Frontend Only
```bash
cd web
npm install
npm run dev
```

### Full Stack with Docker Compose
```bash
docker-compose up --build
```

Access the application at http://localhost

## Raspberry Pi Deployment

### 1. Install Docker on Raspberry Pi

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose -y

# Reboot to apply changes
sudo reboot
```

### 2. Clone Repository on Pi

```bash
git clone https://github.com/jslade/btc-meatspace-sim.git
cd btc-meatspace-sim/code/sim
```

### 3. Build and Run

```bash
# Build for ARM architecture
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access the Application

The application will be available at:
- Frontend: http://<raspberry-pi-ip>
- Backend API: http://<raspberry-pi-ip>:8000/api

### 5. Automatic Startup (Optional)

Create a systemd service to start on boot:

```bash
sudo nano /etc/systemd/system/btc-sim.service
```

Add:
```ini
[Unit]
Description=Bitcoin Meatspace Simulator
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/btc-meatspace-sim/code/sim
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=pi

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable btc-sim
sudo systemctl start btc-sim
```

## Performance Optimization for Raspberry Pi

### 1. Memory Limits

Edit `docker-compose.yml` to add memory limits:

```yaml
services:
  backend:
    # ... existing config
    deploy:
      resources:
        limits:
          memory: 256M
  
  web:
    # ... existing config
    deploy:
      resources:
        limits:
          memory: 128M
```

### 2. Build Optimization

Use multi-stage builds (already configured in Dockerfiles) to reduce image size.

### 3. Database Optimization

For SQLite on Raspberry Pi, consider:
- Regular VACUUM operations
- Write-Ahead Logging (WAL) mode
- Adjust cache size

## API Endpoints

### Entities
- `GET /api/entities` - List all entities
- `POST /api/entities` - Create entity (body: `{type, x, y}`)
- `GET /api/entities/{id}` - Get specific entity
- `PUT /api/entities/{id}` - Update entity
- `DELETE /api/entities` - Delete all entities

### Transactions
- `GET /api/transactions` - List all transactions
- `POST /api/transactions` - Create transaction (body: `{from_id, to_id, amount}`)

### Statistics
- `GET /api/stats` - Get simulation statistics

### Health Check
- `GET /health` - Backend health check

## Monitoring

### Check Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f web
```

### Resource Usage
```bash
# Docker stats
docker stats

# Pi temperature
vcgencmd measure_temp
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 80
sudo lsof -i :80

# Or change port in docker-compose.yml
```

### Database Locked
```bash
# Restart backend
docker-compose restart backend
```

### Build Failures on Pi
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

### Performance Issues
- Monitor with `docker stats`
- Check temperature: `vcgencmd measure_temp`
- Consider adding heatsink/fan for sustained load
- Reduce number of entities in simulation

## Backup and Restore

### Backup Database
```bash
docker-compose exec backend cp /app/btc_sim.db /app/backup.db
docker cp btc-sim-backend:/app/backup.db ./btc_sim_backup.db
```

### Restore Database
```bash
docker cp ./btc_sim_backup.db btc-sim-backend:/app/btc_sim.db
docker-compose restart backend
```

## Security Considerations

1. **Change default ports** in production
2. **Add authentication** if exposing to internet
3. **Use HTTPS** with reverse proxy (nginx/traefik)
4. **Firewall rules** to limit access
5. **Regular updates** of base images

## Development Workflow

1. Make changes locally
2. Test with `docker-compose up --build`
3. Push to repository
4. Pull on Raspberry Pi
5. Rebuild: `docker-compose up --build -d`

## Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build -d

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Remove all data and start fresh
docker-compose down -v
docker-compose up --build -d
```

## Support

For issues or questions, please open an issue on GitHub.
