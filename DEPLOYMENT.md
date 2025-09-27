# Deployment Guide - AI Student Dashboard

This guide provides comprehensive instructions for deploying the AI Student Dashboard to Oracle Cloud Infrastructure (OCI) and other platforms.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React SPA     │    │   Node.js API   │    │   MySQL DB      │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   OCI Object    │
         │              │   Storage       │
         │              └─────────────────┘
         │                       │
         └───────────────────────▼
                    ┌─────────────────┐
                    │   OCI Gen AI    │
                    │   Service       │
                    └─────────────────┘
```

## 🚀 OCI Deployment (Recommended)

### Prerequisites

1. **OCI Account Setup**
   - Active Oracle Cloud Infrastructure account
   - Appropriate permissions for resource creation
   - API keys generated and downloaded

2. **Required OCI Services**
   - Compute instances or Container Instances
   - MySQL Database Service (or self-managed MySQL)
   - Object Storage buckets
   - Generative AI service access
   - Load Balancer (optional)

### Step 1: OCI Resource Setup

#### 1.1 Create Compartment
```bash
# Using OCI CLI
oci iam compartment create \
  --compartment-id <tenancy-ocid> \
  --name "StudentDashboard" \
  --description "Compartment for AI Student Dashboard"
```

#### 1.2 Create VCN and Subnet
```bash
# Create VCN
oci network vcn create \
  --compartment-id <compartment-ocid> \
  --cidr-block "10.0.0.0/16" \
  --display-name "StudentDashboard-VCN"

# Create public subnet
oci network subnet create \
  --compartment-id <compartment-ocid> \
  --vcn-id <vcn-ocid> \
  --cidr-block "10.0.1.0/24" \
  --display-name "Public-Subnet"
```

#### 1.3 Create MySQL Database
```bash
# Using OCI Console or CLI
# Create MySQL Database System
# Choose appropriate shape and storage
# Note down the connection details
```

#### 1.4 Create Object Storage Bucket
```bash
# Create bucket for file uploads
oci os bucket create \
  --compartment-id <compartment-ocid> \
  --name "student-dashboard-uploads" \
  --namespace <your-namespace>
```

### Step 2: Backend Deployment

#### 2.1 Prepare Backend for Deployment

Create `server/Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Change ownership
RUN chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 5000

CMD ["npm", "start"]
```

#### 2.2 Deploy to OCI Container Instances

```bash
# Build and push Docker image
docker build -t student-dashboard-api .
docker tag student-dashboard-api <region>.ocir.io/<tenancy-namespace>/student-dashboard-api:latest
docker push <region>.ocir.io/<tenancy-namespace>/student-dashboard-api:latest

# Create container instance
oci container-instances container-instance create \
  --compartment-id <compartment-ocid> \
  --display-name "student-dashboard-api" \
  --containers '[{
    "imageUrl": "<region>.ocir.io/<tenancy-namespace>/student-dashboard-api:latest",
    "displayName": "api-container",
    "resourceConfig": {
      "vcpus": 1,
      "memoryInGBs": 2
    },
    "ports": [{"port": 5000, "protocol": "TCP"}]
  }]' \
  --vcn-id <vcn-ocid> \
  --subnet-id <subnet-ocid>
```

### Step 3: Frontend Deployment

#### 3.1 Build React Application

```bash
cd client
npm run build
```

#### 3.2 Deploy to OCI Web Apps

```bash
# Using OCI Web Apps
# Upload the build folder contents
# Configure custom domain if needed
```

#### 3.3 Alternative: Deploy to OCI Object Storage

```bash
# Create bucket for static hosting
oci os bucket create \
  --compartment-id <compartment-ocid> \
  --name "student-dashboard-frontend" \
  --namespace <your-namespace>

# Upload build files
aws s3 sync client/build/ s3://student-dashboard-frontend/ \
  --endpoint-url https://<namespace>.compat.objectstorage.<region>.oraclecloud.com
```

### Step 4: Environment Configuration

#### 4.1 Backend Environment Variables

Create `server/.env.production`:
```env
# Database Configuration
DB_HOST=<mysql-endpoint>
DB_USER=admin
DB_PASSWORD=<mysql-password>
DB_NAME=student_dashboard

# JWT Configuration
JWT_SECRET=<strong-random-secret>
JWT_EXPIRES_IN=7d

# Server Configuration
PORT=5000
NODE_ENV=production

# OCI Configuration
OCI_REGION=<your-region>
OCI_TENANCY_OCID=<tenancy-ocid>
OCI_USER_OCID=<user-ocid>
OCI_FINGERPRINT=<api-key-fingerprint>
OCI_PRIVATE_KEY_PATH=/app/oci-private-key.pem
OCI_COMPARTMENT_OCID=<compartment-ocid>
OCI_NAMESPACE=<your-namespace>
OCI_BUCKET_NAME=student-dashboard-uploads
OCI_GENERATIVE_AI_ENDPOINT=https://generativeai.oci.oraclecloud.com
OCI_GENERATIVE_AI_MODEL_ID=cohere.command-text-14b
```

#### 4.2 Frontend Environment Variables

Create `client/.env.production`:
```env
REACT_APP_API_URL=https://your-api-domain.com/api
```

## 🐳 Docker Deployment

### Docker Compose Setup

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: student_dashboard
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppassword
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  backend:
    build: ./server
    ports:
      - "5000:5000"
    environment:
      DB_HOST: mysql
      DB_USER: appuser
      DB_PASSWORD: apppassword
      DB_NAME: student_dashboard
      JWT_SECRET: your-jwt-secret
    depends_on:
      - mysql

  frontend:
    build: ./client
    ports:
      - "3000:80"
    environment:
      REACT_APP_API_URL: http://localhost:5000/api
    depends_on:
      - backend

volumes:
  mysql_data:
```

### Deploy with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Alternative Cloud Deployments

### AWS Deployment

#### Backend (AWS ECS/Fargate)
```yaml
# task-definition.json
{
  "family": "student-dashboard-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [{
    "name": "api",
    "image": "your-account.dkr.ecr.region.amazonaws.com/student-dashboard-api:latest",
    "portMappings": [{"containerPort": 5000}],
    "environment": [
      {"name": "NODE_ENV", "value": "production"}
    ]
  }]
}
```

#### Frontend (AWS S3 + CloudFront)
```bash
# Build and deploy
npm run build
aws s3 sync client/build/ s3://your-bucket-name --delete
aws cloudfront create-invalidation --distribution-id <distribution-id> --paths "/*"
```

### Google Cloud Platform

#### Backend (Cloud Run)
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/student-dashboard-api', './server']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/student-dashboard-api']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'student-dashboard-api', '--image', 'gcr.io/$PROJECT_ID/student-dashboard-api', '--platform', 'managed', '--region', 'us-central1']
```

#### Frontend (Firebase Hosting)
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Initialize Firebase
firebase init hosting

# Deploy
npm run build
firebase deploy
```

## 🔧 Production Optimizations

### Backend Optimizations

1. **Database Connection Pooling**
```javascript
// In database.js
const pool = mysql.createPool({
  connectionLimit: 10,
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  acquireTimeout: 60000,
  timeout: 60000,
  reconnect: true
});
```

2. **Caching Strategy**
```javascript
// Add Redis for caching
const redis = require('redis');
const client = redis.createClient(process.env.REDIS_URL);
```

3. **Logging and Monitoring**
```javascript
// Add Winston for logging
const winston = require('winston');
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### Frontend Optimizations

1. **Code Splitting**
```javascript
// Lazy load components
const AdminPanel = React.lazy(() => import('./pages/AdminPanel'));
```

2. **Service Worker for Caching**
```javascript
// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

3. **Environment-based Configuration**
```javascript
// Use environment variables for API URLs
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

## 🔒 Security Considerations

### Production Security Checklist

- [ ] Use HTTPS for all communications
- [ ] Implement proper CORS policies
- [ ] Set up rate limiting
- [ ] Use environment variables for secrets
- [ ] Implement proper error handling
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Database access controls
- [ ] File upload restrictions
- [ ] Input validation and sanitization

### SSL/TLS Configuration

```nginx
# Nginx configuration for SSL
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoring and Logging

### Application Monitoring

1. **Health Checks**
```javascript
// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage()
  });
});
```

2. **Error Tracking**
```javascript
// Add Sentry for error tracking
const Sentry = require('@sentry/node');
Sentry.init({ dsn: process.env.SENTRY_DSN });
```

3. **Performance Monitoring**
```javascript
// Add New Relic or similar
require('newrelic');
```

## 🚀 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm run install-all
    
    - name: Run tests
      run: npm test
    
    - name: Build application
      run: npm run build
    
    - name: Deploy to OCI
      run: |
        # Add OCI deployment commands
        echo "Deploying to OCI..."
```

## 📞 Support and Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check connection string
   - Verify network access
   - Check firewall rules

2. **File Upload Issues**
   - Verify OCI credentials
   - Check bucket permissions
   - Validate file size limits

3. **AI Service Issues**
   - Verify OCI AI service access
   - Check API quotas
   - Validate model availability

### Debugging Commands

```bash
# Check container logs
docker logs <container-id>

# Check database connection
mysql -h <host> -u <user> -p <database>

# Test API endpoints
curl -X GET http://localhost:5000/api/health

# Check OCI connectivity
oci os bucket list --compartment-id <compartment-ocid>
```

---

*This deployment guide provides comprehensive instructions for deploying the AI Student Dashboard across various platforms. Choose the deployment method that best fits your infrastructure requirements and budget.*
