// Bitcoin Meatspace Simulator
// Configuration constants
const CONFIG = {
    INITIAL_BTC_MAX: 0.5,
    TRANSACTION_PERCENTAGE: 0.3,
    TRANSACTION_MIN: 0.01,
    TRANSACTION_MAX: 0.05,
    MAX_LOG_ENTRIES: 20,
    ENTITY_RADIUS: 20
};

class Entity {
    constructor(x, y, type) {
        this.x = x;
        this.y = y;
        this.type = type; // 'person' or 'merchant'
        this.btc = Math.random() * CONFIG.INITIAL_BTC_MAX;
        this.id = Math.random().toString(36).substring(2, 11);
        this.selected = false;
        this.vx = 0;
        this.vy = 0;
    }

    draw(ctx) {
        ctx.save();
        
        // Draw shadow
        ctx.shadowColor = 'rgba(0, 0, 0, 0.2)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 2;
        ctx.shadowOffsetY = 2;

        // Draw entity circle
        ctx.beginPath();
        ctx.arc(this.x, this.y, CONFIG.ENTITY_RADIUS, 0, Math.PI * 2);
        ctx.fillStyle = this.type === 'person' ? '#3b82f6' : '#10b981';
        ctx.fill();

        if (this.selected) {
            ctx.strokeStyle = '#f7931a';
            ctx.lineWidth = 3;
            ctx.stroke();
        }

        ctx.shadowColor = 'transparent';

        // Draw icon
        ctx.fillStyle = 'white';
        ctx.font = 'bold 20px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.type === 'person' ? '👤' : '🏪', this.x, this.y);

        // Draw BTC amount
        ctx.fillStyle = '#333';
        ctx.font = '10px Arial';
        ctx.fillText(this.btc.toFixed(3), this.x, this.y + 30);

        ctx.restore();
    }

    update(width, height) {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off walls
        if (this.x < CONFIG.ENTITY_RADIUS || this.x > width - CONFIG.ENTITY_RADIUS) {
            this.vx *= -1;
            this.x = Math.max(CONFIG.ENTITY_RADIUS, Math.min(width - CONFIG.ENTITY_RADIUS, this.x));
        }
        if (this.y < CONFIG.ENTITY_RADIUS || this.y > height - CONFIG.ENTITY_RADIUS) {
            this.vy *= -1;
            this.y = Math.max(CONFIG.ENTITY_RADIUS, Math.min(height - CONFIG.ENTITY_RADIUS, this.y));
        }

        // Friction
        this.vx *= 0.98;
        this.vy *= 0.98;
    }

    isClicked(mx, my) {
        const dx = this.x - mx;
        const dy = this.y - my;
        return Math.sqrt(dx * dx + dy * dy) < CONFIG.ENTITY_RADIUS;
    }
}

class Simulator {
    constructor() {
        this.canvas = document.getElementById('simCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.entities = [];
        this.transactions = [];
        this.selectedEntity = null;
        this.animationId = null;
        this.isWalking = false;

        this.setupEventListeners();
        this.animate();
    }

    setupEventListeners() {
        document.getElementById('addPerson').addEventListener('click', () => {
            this.addEntity('person');
        });

        document.getElementById('addMerchant').addEventListener('click', () => {
            this.addEntity('merchant');
        });

        document.getElementById('reset').addEventListener('click', () => {
            this.reset();
        });

        document.getElementById('startTx').addEventListener('click', () => {
            this.startTransaction();
        });

        document.getElementById('randomWalk').addEventListener('click', () => {
            this.toggleRandomWalk();
        });

        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            this.handleCanvasClick(x, y);
        });
    }

    addEntity(type) {
        const x = Math.random() * (this.canvas.width - 100) + 50;
        const y = Math.random() * (this.canvas.height - 100) + 50;
        this.entities.push(new Entity(x, y, type));
        this.updateStats();
        this.logEvent(`Added new ${type} at (${Math.floor(x)}, ${Math.floor(y)})`);
    }

    handleCanvasClick(x, y) {
        // Deselect previous
        if (this.selectedEntity) {
            this.selectedEntity.selected = false;
        }

        // Find clicked entity
        this.selectedEntity = null;
        for (let i = this.entities.length - 1; i >= 0; i--) {
            if (this.entities[i].isClicked(x, y)) {
                this.selectedEntity = this.entities[i];
                this.selectedEntity.selected = true;
                this.logEvent(`Selected ${this.selectedEntity.type} with ${this.selectedEntity.btc.toFixed(3)} BTC`);
                break;
            }
        }
    }

    startTransaction() {
        if (this.entities.length < 2) {
            this.logEvent('Need at least 2 entities for a transaction');
            return;
        }

        // Pick two random entities
        const from = this.entities[Math.floor(Math.random() * this.entities.length)];
        let to;
        do {
            to = this.entities[Math.floor(Math.random() * this.entities.length)];
        } while (to === from);

        const amount = Math.min(from.btc * CONFIG.TRANSACTION_PERCENTAGE, CONFIG.TRANSACTION_MIN + Math.random() * CONFIG.TRANSACTION_MAX);
        
        if (from.btc >= amount) {
            from.btc -= amount;
            to.btc += amount;

            this.transactions.push({
                from: from.id,
                to: to.id,
                amount: amount,
                timestamp: Date.now()
            });

            this.drawTransaction(from, to);
            this.logEvent(`Transaction: ${amount.toFixed(4)} BTC from ${from.type} to ${to.type}`);
            this.updateStats();
        } else {
            this.logEvent('Insufficient BTC for transaction');
        }
    }

    drawTransaction(from, to) {
        const startTime = Date.now();
        const duration = 1000;

        const animateTx = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Draw lightning bolt effect
            this.ctx.save();
            this.ctx.strokeStyle = `rgba(247, 147, 26, ${1 - progress})`;
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            this.ctx.moveTo(from.x, from.y);

            // Add some zigzag for effect
            const midX = (from.x + to.x) / 2 + (Math.random() - 0.5) * 20;
            const midY = (from.y + to.y) / 2 + (Math.random() - 0.5) * 20;
            this.ctx.lineTo(midX, midY);
            this.ctx.lineTo(to.x, to.y);
            this.ctx.stroke();
            this.ctx.restore();

            if (progress < 1) {
                requestAnimationFrame(animateTx);
            }
        };

        animateTx();
    }

    toggleRandomWalk() {
        this.isWalking = !this.isWalking;
        const btn = document.getElementById('randomWalk');
        
        if (this.isWalking) {
            btn.textContent = 'Stop Walking';
            btn.classList.remove('btn-info');
            btn.classList.add('btn-danger');
            this.entities.forEach(entity => {
                entity.vx = (Math.random() - 0.5) * 2;
                entity.vy = (Math.random() - 0.5) * 2;
            });
        } else {
            btn.textContent = 'Random Walk';
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-info');
            this.entities.forEach(entity => {
                entity.vx = 0;
                entity.vy = 0;
            });
        }
    }

    reset() {
        this.entities = [];
        this.transactions = [];
        this.selectedEntity = null;
        this.isWalking = false;
        document.getElementById('logEntries').innerHTML = '';
        const btn = document.getElementById('randomWalk');
        btn.textContent = 'Random Walk';
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-info');
        this.updateStats();
        this.logEvent('Simulation reset');
    }

    updateStats() {
        const people = this.entities.filter(e => e.type === 'person').length;
        const merchants = this.entities.filter(e => e.type === 'merchant').length;
        const totalBtc = this.entities.reduce((sum, e) => sum + e.btc, 0);

        document.getElementById('peopleCount').textContent = people;
        document.getElementById('merchantCount').textContent = merchants;
        document.getElementById('txCount').textContent = this.transactions.length;
        document.getElementById('totalBtc').textContent = totalBtc.toFixed(3);
    }

    logEvent(message) {
        const logEntries = document.getElementById('logEntries');
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        
        const time = new Date().toLocaleTimeString();
        entry.innerHTML = `<span class="time">[${time}]</span> ${message}`;
        
        logEntries.insertBefore(entry, logEntries.firstChild);

        // Keep only last N entries
        while (logEntries.children.length > CONFIG.MAX_LOG_ENTRIES) {
            logEntries.removeChild(logEntries.lastChild);
        }
    }

    animate() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw grid
        this.ctx.strokeStyle = '#e9ecef';
        this.ctx.lineWidth = 1;
        for (let x = 0; x < this.canvas.width; x += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        for (let y = 0; y < this.canvas.height; y += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }

        // Update and draw entities
        this.entities.forEach(entity => {
            if (this.isWalking) {
                entity.update(this.canvas.width, this.canvas.height);
            }
            entity.draw(this.ctx);
        });

        this.animationId = requestAnimationFrame(() => this.animate());
    }
}

// Initialize the simulator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const sim = new Simulator();
    sim.logEvent('Bitcoin Meatspace Simulator initialized');
    sim.logEvent('Add people and merchants to begin simulation');
});
