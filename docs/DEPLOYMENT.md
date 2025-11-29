# PesoScan Deployment Guide

## Overview

This guide covers deployment options for the PesoScan counterfeit detection system, from local development to production-ready deployments.

## Development Deployment

### Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- Git

### Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd pesoscan
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python main.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Docker Deployment

### Docker Compose (Recommended)

1. **Create `docker-compose.yml`**
   ```yaml
   version: '3.8'
   
   services:
     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         - ENVIRONMENT=production
         - DATABASE_URL=postgresql://user:pass@db:5432/pesoscan
       volumes:
         - ./trained_models:/app/trained_models
       depends_on:
         - db
         - redis
   
     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
       environment:
         - REACT_APP_API_URL=http://localhost:8000
       depends_on:
         - backend
   
     db:
       image: postgres:13
       environment:
         - POSTGRES_DB=pesoscan
         - POSTGRES_USER=pesoscan_user
         - POSTGRES_PASSWORD=secure_password
       volumes:
         - postgres_data:/var/lib/postgresql/data
         - ./init.sql:/docker-entrypoint-initdb.d/init.sql
       ports:
         - "5432:5432"
   
     redis:
       image: redis:7-alpine
       ports:
         - "6379:6379"
       volumes:
         - redis_data:/data
   
     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./ssl:/etc/ssl/certs
       depends_on:
         - frontend
         - backend
   
   volumes:
     postgres_data:
     redis_data:
   ```

2. **Create Backend Dockerfile**
   ```dockerfile
   # backend/Dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       libgl1-mesa-glx \
       libglib2.0-0 \
       libsm6 \
       libxext6 \
       libxrender-dev \
       libgomp1 \
       && rm -rf /var/lib/apt/lists/*
   
   # Install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application code
   COPY . .
   
   # Create directories for models and uploads
   RUN mkdir -p trained_models uploads
   
   # Expose port
   EXPOSE 8000
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
     CMD curl -f http://localhost:8000/api/health || exit 1
   
   # Run application
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
   ```

3. **Create Frontend Dockerfile**
   ```dockerfile
   # frontend/Dockerfile
   FROM node:16-alpine as build
   
   WORKDIR /app
   
   # Install dependencies
   COPY package*.json ./
   RUN npm ci --only=production
   
   # Copy source and build
   COPY . .
   RUN npm run build
   
   # Production stage
   FROM nginx:alpine
   
   # Copy built files
   COPY --from=build /app/build /usr/share/nginx/html
   
   # Copy nginx config
   COPY nginx.conf /etc/nginx/nginx.conf
   
   # Expose port
   EXPOSE 80
   
   # Health check
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
     CMD curl -f http://localhost || exit 1
   
   CMD ["nginx", "-g", "daemon off;"]
   ```

4. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   ```

## Cloud Deployment

### AWS Deployment

#### Option 1: Elastic Container Service (ECS)

1. **Create ECR Repositories**
   ```bash
   aws ecr create-repository --repository-name pesoscan-backend
   aws ecr create-repository --repository-name pesoscan-frontend
   ```

2. **Build and Push Images**
   ```bash
   # Get login token
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   
   # Build and push backend
   docker build -t pesoscan-backend ./backend
   docker tag pesoscan-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/pesoscan-backend:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/pesoscan-backend:latest
   
   # Build and push frontend
   docker build -t pesoscan-frontend ./frontend
   docker tag pesoscan-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/pesoscan-frontend:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/pesoscan-frontend:latest
   ```

3. **Create ECS Task Definition**
   ```json
   {
     "family": "pesoscan",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "1024",
     "memory": "2048",
     "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "backend",
         "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/pesoscan-backend:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "ENVIRONMENT",
             "value": "production"
           }
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/pesoscan",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "backend"
           }
         }
       }
     ]
   }
   ```

#### Option 2: Elastic Beanstalk

1. **Create Application**
   ```bash
   eb init pesoscan --platform "Docker running on 64bit Amazon Linux 2"
   eb create production --elb-type application
   ```

2. **Configure Environment**
   ```bash
   eb setenv ENVIRONMENT=production DATABASE_URL=<rds-connection-string>
   eb deploy
   ```

### Google Cloud Platform (GCP)

#### Cloud Run Deployment

1. **Build Images**
   ```bash
   gcloud builds submit --tag gcr.io/<project-id>/pesoscan-backend ./backend
   gcloud builds submit --tag gcr.io/<project-id>/pesoscan-frontend ./frontend
   ```

2. **Deploy Services**
   ```bash
   # Deploy backend
   gcloud run deploy pesoscan-backend \
     --image gcr.io/<project-id>/pesoscan-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars ENVIRONMENT=production
   
   # Deploy frontend
   gcloud run deploy pesoscan-frontend \
     --image gcr.io/<project-id>/pesoscan-frontend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars REACT_APP_API_URL=<backend-url>
   ```

### Microsoft Azure

#### Container Apps Deployment

1. **Create Resource Group**
   ```bash
   az group create --name pesoscan-rg --location eastus
   ```

2. **Create Container Registry**
   ```bash
   az acr create --resource-group pesoscan-rg --name pesoscanregistry --sku Basic
   ```

3. **Build and Push Images**
   ```bash
   az acr build --registry pesoscanregistry --image pesoscan-backend ./backend
   az acr build --registry pesoscanregistry --image pesoscan-frontend ./frontend
   ```

4. **Deploy Container Apps**
   ```bash
   az containerapp env create --name pesoscan-env --resource-group pesoscan-rg --location eastus
   
   az containerapp create \
     --name pesoscan-backend \
     --resource-group pesoscan-rg \
     --environment pesoscan-env \
     --image pesoscanregistry.azurecr.io/pesoscan-backend:latest \
     --target-port 8000 \
     --ingress external
   ```

## Production Configuration

### Environment Variables

**Backend (.env)**
```env
# Environment
ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/pesoscan
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["https://yourdomain.com"]

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=/app/uploads

# AI Models
YOLO_MODEL_PATH=/app/trained_models/peso_detection.pt
CNN_MODEL_PATH=/app/trained_models/peso_classifier.pt

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO
```

**Frontend (.env.production)**
```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
REACT_APP_SENTRY_DSN=https://your-sentry-dsn
GENERATE_SOURCEMAP=false
```

### SSL/TLS Configuration

**Nginx Configuration**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Handle large file uploads
        client_max_body_size 10M;
    }
}
```

### Database Setup

**PostgreSQL Production Setup**
```sql
-- Create database and user
CREATE DATABASE pesoscan;
CREATE USER pesoscan_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE pesoscan TO pesoscan_user;

-- Connect to pesoscan database
\c pesoscan;

-- Create tables
CREATE TABLE scan_history (
    id SERIAL PRIMARY KEY,
    scan_id VARCHAR(50) UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_path VARCHAR(255),
    detection_result JSONB,
    classification_result JSONB,
    processing_time FLOAT,
    user_ip VARCHAR(45)
);

CREATE INDEX idx_scan_timestamp ON scan_history(timestamp);
CREATE INDEX idx_scan_id ON scan_history(scan_id);

-- Create stats table
CREATE TABLE system_stats (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    total_scans INTEGER DEFAULT 0,
    authentic_count INTEGER DEFAULT 0,
    counterfeit_count INTEGER DEFAULT 0,
    average_confidence FLOAT DEFAULT 0.0,
    UNIQUE(date)
);
```

### Monitoring and Logging

**Docker Compose with Monitoring**
```yaml
services:
  # ... existing services ...

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

  elasticsearch:
    image: elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  kibana:
    image: kibana:7.14.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  prometheus_data:
  grafana_data:
  elasticsearch_data:
```

### Security Considerations

1. **API Security**
   - Implement rate limiting
   - Use API keys for production
   - Validate all inputs
   - Sanitize file uploads

2. **Infrastructure Security**
   - Use HTTPS/TLS everywhere
   - Implement proper firewall rules
   - Keep dependencies updated
   - Use secrets management

3. **Data Protection**
   - Encrypt sensitive data
   - Implement data retention policies
   - Regular security audits
   - GDPR compliance if applicable

### Performance Optimization

1. **Backend Optimization**
   - Use async/await for I/O operations
   - Implement connection pooling
   - Add response caching
   - Optimize AI model inference

2. **Frontend Optimization**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement lazy loading
   - Optimize bundle size

3. **Database Optimization**
   - Add proper indexes
   - Implement query optimization
   - Use connection pooling
   - Regular maintenance

### Backup and Recovery

1. **Database Backups**
   ```bash
   # Automated backup script
   #!/bin/bash
   BACKUP_DIR="/backups"
   DATE=$(date +%Y%m%d_%H%M%S)
   
   pg_dump -h localhost -U pesoscan_user pesoscan > $BACKUP_DIR/pesoscan_$DATE.sql
   
   # Keep only last 7 days
   find $BACKUP_DIR -name "pesoscan_*.sql" -mtime +7 -delete
   ```

2. **Model and Asset Backups**
   ```bash
   # Backup trained models
   aws s3 sync ./trained_models s3://pesoscan-models/backup/
   
   # Backup uploaded images
   aws s3 sync ./uploads s3://pesoscan-uploads/backup/
   ```

### Troubleshooting

**Common Deployment Issues:**

1. **Memory Issues**
   - Increase container memory limits
   - Optimize AI model loading
   - Implement model caching

2. **Network Issues**
   - Check firewall rules
   - Verify DNS configuration
   - Test connectivity between services

3. **Performance Issues**
   - Monitor resource usage
   - Optimize database queries
   - Scale horizontally if needed

**Health Checks:**
```bash
# Check service health
curl http://localhost:8000/api/health

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Monitor resources
docker stats
```

This deployment guide provides comprehensive instructions for deploying PesoScan in various environments, from development to production-ready cloud deployments.