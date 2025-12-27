# Deployment Guide - Core Integrator

## Overview
Complete deployment guide for the Core Integrator system covering MongoDB setup, cloud deployment, and production configuration.

## MongoDB Setup

### Option 1: MongoDB Community Server (Local)

#### Installation
1. **Download MongoDB:**
   - Visit: https://www.mongodb.com/try/download/community
   - Select Windows, Version 7.0+
   - Download MSI installer

2. **Install MongoDB:**
   ```bash
   # Run the MSI installer
   # Choose "Complete" installation
   # Install as Windows Service
   ```

3. **Start MongoDB:**
   ```bash
   # MongoDB should start automatically as a service
   # Or manually start:
   net start MongoDB
   ```

4. **Verify Installation:**
   ```bash
   mongosh
   # Should connect to MongoDB shell
   ```

### Option 2: MongoDB Atlas (Cloud)

#### Setup
1. **Create Account:**
   - Visit: https://www.mongodb.com/atlas
   - Sign up for free tier

2. **Create Cluster:**
   - Choose free M0 cluster
   - Select region (closest to you)
   - Create cluster

3. **Get Connection String:**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy connection string

#### Configuration
```bash
# .env
USE_MONGODB=true
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE_NAME=core_integrator
```

### Enable MongoDB in Core Integrator

#### Step 1: Install Dependencies
```bash
pip install pymongo
```

#### Step 2: Configure Environment
```bash
# .env
USE_MONGODB=true
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE_NAME=core_integrator
```

#### Step 3: Test Connection
```bash
python -c "
from src.db.mongodb_adapter import MongoDBAdapter
try:
    adapter = MongoDBAdapter()
    print('✅ MongoDB connection successful')
except Exception as e:
    print(f'❌ MongoDB connection failed: {e}')
"
```

## Cloud Deployment

### AWS Deployment

#### EC2 Setup
```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# Security Group: Allow ports 22, 80, 443, 8001

# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+
sudo apt install python3.9 python3.9-pip python3.9-venv -y

# Clone repository
git clone your-repo-url
cd Core-Integrator-Sprint-1.1-

# Setup virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Environment Configuration
```bash
# Create production .env
cp config/.env.example .env

# Edit .env for production
nano .env
```

```bash
# Production .env
DB_PATH=data/context.db
SSPL_ENABLED=true
SSPL_ALLOW_DRIFT_SECONDS=300
USE_MONGODB=true
MONGODB_CONNECTION_STRING=your_atlas_connection_string
MONGODB_DATABASE_NAME=core_integrator_prod
INTEGRATOR_USE_NOOPUR=false
```

#### Process Management with systemd
```bash
# Create service file
sudo nano /etc/systemd/system/core-integrator.service
```

```ini
[Unit]
Description=Core Integrator API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Core-Integrator-Sprint-1.1-
Environment=PATH=/home/ubuntu/Core-Integrator-Sprint-1.1-/venv/bin
ExecStart=/home/ubuntu/Core-Integrator-Sprint-1.1-/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable core-integrator
sudo systemctl start core-integrator
sudo systemctl status core-integrator
```

#### Nginx Reverse Proxy
```bash
# Install Nginx
sudo apt install nginx -y

# Create site configuration
sudo nano /etc/nginx/sites-available/core-integrator
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/core-integrator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data logs/bridge

# Expose port
EXPOSE 8001

# Run application
CMD ["python", "main.py"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  core-integrator:
    build: .
    ports:
      - "8001:8001"
    environment:
      - DB_PATH=data/context.db
      - USE_MONGODB=true
      - MONGODB_CONNECTION_STRING=mongodb://mongo:27017
      - MONGODB_DATABASE_NAME=core_integrator
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - mongo

  mongo:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=core_integrator

volumes:
  mongo_data:
```

#### Build and Run
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f core-integrator

# Stop
docker-compose down
```

### Kubernetes Deployment

#### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: core-integrator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: core-integrator
  template:
    metadata:
      labels:
        app: core-integrator
    spec:
      containers:
      - name: core-integrator
        image: your-registry/core-integrator:latest
        ports:
        - containerPort: 8001
        env:
        - name: USE_MONGODB
          value: "true"
        - name: MONGODB_CONNECTION_STRING
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: connection-string
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: core-integrator-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: core-integrator-service
spec:
  selector:
    app: core-integrator
  ports:
  - port: 80
    targetPort: 8001
  type: LoadBalancer
```

## Production Configuration

### Security Hardening

#### Environment Variables
```bash
# Production .env
SSPL_ENABLED=true
SSPL_ALLOW_DRIFT_SECONDS=60  # Stricter in production
```

#### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

#### SSL/TLS with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Monitoring and Logging

#### Application Logs
```python
# Enhanced logging configuration
import logging
from logging.handlers import RotatingFileHandler

# Configure rotating file handler
handler = RotatingFileHandler(
    'logs/bridge/app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s'
))

logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)
```

#### System Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Monitor application
sudo systemctl status core-integrator
sudo journalctl -u core-integrator -f
```

#### Health Checks
```bash
# Add to crontab for health monitoring
*/5 * * * * curl -f http://localhost:8001/system/health || echo "Health check failed" | mail -s "Core Integrator Alert" admin@yourdomain.com
```

### Database Migration

#### SQLite to MongoDB Migration
```python
# scripts/migrate_to_mongodb.py
from src.db.memory import ContextMemory
from src.db.mongodb_adapter import MongoDBAdapter
import json

def migrate_sqlite_to_mongodb():
    """Migrate data from SQLite to MongoDB"""
    
    # Source: SQLite
    sqlite_memory = ContextMemory("data/context.db")
    
    # Destination: MongoDB
    mongo_adapter = MongoDBAdapter()
    
    # Get all unique user IDs (requires custom query)
    import sqlite3
    conn = sqlite3.connect("data/context.db")
    cursor = conn.execute("SELECT DISTINCT user_id FROM interactions")
    user_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    print(f"Migrating data for {len(user_ids)} users...")
    
    for user_id in user_ids:
        history = sqlite_memory.get_user_history(user_id)
        print(f"Migrating {len(history)} interactions for user {user_id}")
        
        for entry in history:
            mongo_adapter.store_interaction(
                user_id,
                entry["request"],
                entry["response"]
            )
    
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_sqlite_to_mongodb()
```

### Backup and Recovery

#### Database Backup
```bash
# SQLite backup
cp data/context.db backups/context_$(date +%Y%m%d_%H%M%S).db

# MongoDB backup
mongodump --uri="your_connection_string" --out=backups/mongodb_$(date +%Y%m%d_%H%M%S)
```

#### Automated Backup Script
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup SQLite database
if [ -f "data/context.db" ]; then
    cp data/context.db $BACKUP_DIR/context_$DATE.db
    echo "SQLite backup created: context_$DATE.db"
fi

# Backup application logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Add to crontab for daily backups
0 2 * * * /home/ubuntu/Core-Integrator-Sprint-1.1-/backup.sh
```

### Performance Optimization

#### Database Optimization
```python
# MongoDB indexes for performance
from pymongo import MongoClient

client = MongoClient("your_connection_string")
db = client.core_integrator
collection = db.interactions

# Create compound index
collection.create_index([
    ("user_id", 1),
    ("module", 1), 
    ("timestamp", -1)
])

# Create timestamp index
collection.create_index([("timestamp", -1)])
```

#### Application Optimization
```python
# Use connection pooling for MongoDB
from pymongo import MongoClient

client = MongoClient(
    "your_connection_string",
    maxPoolSize=50,
    minPoolSize=10,
    maxIdleTimeMS=30000
)
```

### Load Balancing

#### Multiple Instances
```bash
# Run multiple instances on different ports
python main.py --port 8001 &
python main.py --port 8002 &
python main.py --port 8003 &
```

#### Nginx Load Balancer
```nginx
upstream core_integrator {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://core_integrator;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 8001
sudo lsof -i :8001
sudo kill -9 <PID>
```

#### Database Connection Issues
```bash
# Check MongoDB status
sudo systemctl status mongod

# Check connection string
python -c "from pymongo import MongoClient; print(MongoClient('your_string').admin.command('ping'))"
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R ubuntu:ubuntu /home/ubuntu/Core-Integrator-Sprint-1.1-
chmod +x scripts/*.py
```

### Log Analysis
```bash
# Application logs
tail -f logs/bridge/app.log

# System logs
sudo journalctl -u core-integrator -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Maintenance

### Regular Tasks
- [ ] Monitor disk space (`df -h`)
- [ ] Check application logs for errors
- [ ] Verify database backups
- [ ] Update dependencies (`pip list --outdated`)
- [ ] Monitor system resources (`htop`)
- [ ] Check SSL certificate expiry
- [ ] Review security logs

### Updates
```bash
# Update application
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart core-integrator
```

### Scaling Considerations
- Monitor response times and error rates
- Scale horizontally with load balancers
- Consider database sharding for large datasets
- Implement caching for frequently accessed data
- Use CDN for static assets

This deployment guide ensures a robust, scalable, and maintainable production deployment of the Core Integrator system.