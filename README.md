# Swippter

> An ecommerce platform for fast fashion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-93.3%25-blue)](https://www.python.org/)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Infrastructure Deployment](#infrastructure-deployment)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Swippter is a modern ecommerce platform designed for fast fashion retail. The application provides a complete solution for managing products, orders, customers, and inventory with a scalable microservices architecture.

### Key Features

- 🛍️ Product catalog management
- 🛒 Shopping cart functionality
- 💳 Secure payment processing
- 👤 User authentication and authorization
- 📦 Order management and tracking
- 📊 Admin dashboard
- 🔍 Product search and filtering
- 📱 Responsive design

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend   │─────▶│  Database   │
│   (React)   │      │  (Python)   │      │ (PostgreSQL)│
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   Redis     │
                     │   Cache     │
                     └─────────────┘
```

### Technology Stack

**Backend:**
- Python 3.x
- FastAPI / Django / Flask (framework)
- PostgreSQL (database)
- Redis (caching)
- Celery (task queue)

**Frontend:**
- React.js / Next.js
- TypeScript
- Tailwind CSS / Material-UI

**Infrastructure:**
- Docker & Docker Compose
- Kubernetes
- Nginx (reverse proxy)
- AWS / GCP / Azure

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (20.10+)
- **Docker Compose** (2.0+)
- **Python** (3.9+)
- **Node.js** (16+) and npm/yarn
- **Git**
- **kubectl** (for Kubernetes deployment)
- **Terraform** (optional, for infrastructure)

### System Requirements

- **CPU:** 2+ cores
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** 10GB free space

## 📁 Project Structure

```
swippter/
├── backend/                 # Backend application
│   ├── api/                # API routes
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── middleware/         # Middleware functions
│   ├── config/             # Configuration files
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend Docker image
│   └── manage.py           # Management script
│
├── frontend/               # Frontend application
│   ├── public/            # Static assets
│   ├── src/               # Source code
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── utils/         # Utility functions
│   │   └── App.js         # Main app component
│   ├── package.json       # Node dependencies
│   ├── Dockerfile         # Frontend Docker image
│   └── nginx.conf         # Nginx configuration
│
├── infra/                  # Infrastructure as Code
│   ├── docker/            # Docker configurations
│   │   └── docker-compose.yml
│   ├── kubernetes/        # K8s manifests
│   │   ├── deployments/
│   │   ├── services/
│   │   ├── configmaps/
│   │   └── secrets/
│   ├── terraform/         # Terraform configs
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── scripts/           # Deployment scripts
│   └── helm/              # Helm charts
│
├── .github/               # GitHub workflows
├── docs/                  # Documentation
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── SECURITY.md
```

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/akk29/swippter.git
cd swippter
```

### 2. Environment Configuration

Create environment files for backend and frontend:

#### Backend Environment (.env)

```bash
# Create backend environment file
cd backend
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/swippter_db
DB_HOST=postgres
DB_PORT=5432
DB_NAME=swippter_db
DB_USER=swippter_user
DB_PASSWORD=your_secure_password

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_HOST=redis
REDIS_PORT=6379

# Application
SECRET_KEY=your_super_secret_key_change_this
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# Payment Gateway (Stripe/PayPal)
STRIPE_PUBLIC_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key

# AWS S3 (for file storage)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=swippter-media
AWS_S3_REGION_NAME=us-east-1

# Application Settings
PORT=8000
WORKERS=4
LOG_LEVEL=info
```

#### Frontend Environment (.env)

```bash
# Create frontend environment file
cd frontend
cp .env.example .env
```

Edit `.env`:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000/ws

# Stripe
REACT_APP_STRIPE_PUBLIC_KEY=pk_test_your_key

# Analytics
REACT_APP_GA_TRACKING_ID=UA-XXXXXXXXX-X

# Environment
REACT_APP_ENV=development
```

### 3. Install Dependencies

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install
# or
yarn install
```

## 🏃 Running the Application

### Option 1: Docker Compose (Recommended)

This is the easiest way to run the entire application stack.

```bash
# From the project root directory
cd infra/docker

# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Check running services
docker-compose ps

# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: deletes data)
docker-compose down -v
```

**Services will be available at:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Admin Panel: http://localhost:8000/admin
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Option 2: Local Development

#### Start Backend

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Run development server
python manage.py runserver 0.0.0.0:8000

# Or with gunicorn (production-like)
gunicorn app.main:app --bind 0.0.0.0:8000 --workers 4

# Or with uvicorn (for FastAPI)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Start Frontend

```bash
cd frontend

# Development server
npm start
# or
yarn start

# Build for production
npm run build
# or
yarn build

# Serve production build
npm run serve
# or
serve -s build -l 3000
```

#### Start Background Workers (Celery)

```bash
cd backend

# Start Celery worker
celery -A app.celery worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A app.celery beat --loglevel=info

# Start Flower (Celery monitoring)
celery -A app.celery flower --port=5555
```

### Option 3: Individual Docker Containers

```bash
# Build backend image
cd backend
docker build -t swippter-backend:latest .
docker run -d -p 8000:8000 --name swippter-backend swippter-backend:latest

# Build frontend image
cd frontend
docker build -t swippter-frontend:latest .
docker run -d -p 3000:80 --name swippter-frontend swippter-frontend:latest
```

## ☸️ Infrastructure Deployment

### Docker Compose Commands

```bash
cd infra/docker

# Start services
docker-compose up -d

# Scale specific service
docker-compose up -d --scale backend=3

# View service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute commands in container
docker-compose exec backend python manage.py shell
docker-compose exec postgres psql -U swippter_user -d swippter_db

# Rebuild specific service
docker-compose up -d --build backend

# Health check
docker-compose ps
```

### Kubernetes Deployment

#### Prerequisites

```bash
# Ensure kubectl is configured
kubectl cluster-info
kubectl get nodes
```

#### Deploy to Kubernetes

```bash
cd infra/kubernetes

# Create namespace
kubectl create namespace swippter

# Apply ConfigMaps and Secrets
kubectl apply -f configmaps/ -n swippter
kubectl apply -f secrets/ -n swippter

# Deploy database (PostgreSQL)
kubectl apply -f deployments/postgres-deployment.yaml -n swippter
kubectl apply -f services/postgres-service.yaml -n swippter

# Deploy Redis
kubectl apply -f deployments/redis-deployment.yaml -n swippter
kubectl apply -f services/redis-service.yaml -n swippter

# Deploy backend
kubectl apply -f deployments/backend-deployment.yaml -n swippter
kubectl apply -f services/backend-service.yaml -n swippter

# Deploy frontend
kubectl apply -f deployments/frontend-deployment.yaml -n swippter
kubectl apply -f services/frontend-service.yaml -n swippter

# Apply Ingress
kubectl apply -f ingress/ingress.yaml -n swippter

# Check deployment status
kubectl get pods -n swippter
kubectl get services -n swippter
kubectl get ingress -n swippter

# View logs
kubectl logs -f deployment/backend -n swippter
kubectl logs -f deployment/frontend -n swippter

# Scale deployment
kubectl scale deployment backend --replicas=5 -n swippter

# Delete deployment
kubectl delete namespace swippter
```

#### Using Helm

```bash
cd infra/helm

# Install Helm chart
helm install swippter ./swippter-chart -n swippter --create-namespace

# Upgrade release
helm upgrade swippter ./swippter-chart -n swippter

# Rollback
helm rollback swippter 1 -n swippter

# Uninstall
helm uninstall swippter -n swippter

# List releases
helm list -n swippter
```

### Terraform (Infrastructure as Code)

```bash
cd infra/terraform

# Initialize Terraform
terraform init

# Plan infrastructure changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Or apply directly
terraform apply -auto-approve

# Show current state
terraform show

# Destroy infrastructure
terraform destroy -auto-approve

# Format Terraform files
terraform fmt

# Validate configuration
terraform validate
```

### Monitoring & Logging

```bash
# View application logs
docker-compose logs -f backend frontend

# Kubernetes logs
kubectl logs -f deployment/backend -n swippter

# Access Flower (Celery monitoring)
open http://localhost:5555

# PostgreSQL monitoring
docker-compose exec postgres psql -U swippter_user -d swippter_db

# Redis monitoring
docker-compose exec redis redis-cli INFO
```

## 📚 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Sample API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get products
curl http://localhost:8000/api/v1/products

# Get product by ID
curl http://localhost:8000/api/v1/products/1

# Create product (requires auth)
curl -X POST http://localhost:8000/api/v1/products \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"T-Shirt","price":29.99}'

# User registration
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123"}'

# User login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123"}'
```

## 🛠️ Development

### Database Migrations

```bash
cd backend

# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate app_name migration_name

# Show migrations
python manage.py showmigrations
```

### Seed Database

```bash
cd backend

# Load fixtures
python manage.py loaddata fixtures/initial_data.json

# Create sample data
python manage.py seed_database

# Clear database
python manage.py flush
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 .
black .
isort .
pylint app/

# Frontend linting
cd frontend
npm run lint
npm run lint:fix
npm run format
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run against all files
pre-commit run --all-files
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_products.py

# Run specific test
pytest tests/test_products.py::test_get_product

# Run with verbose output
pytest -v

# Run in parallel
pytest -n auto
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test
# or
yarn test

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run test:e2e

# Run specific test file
npm test -- ProductCard.test.js
```

### Integration Tests

```bash
# Run all integration tests
cd tests/integration
pytest -v

# Test API endpoints
pytest test_api_integration.py
```

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Connect to PostgreSQL
docker-compose exec postgres psql -U swippter_user -d swippter_db
```

#### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 PID  # macOS/Linux
taskkill /PID pid /F  # Windows
```

#### Container Won't Start

```bash
# Check container status
docker-compose ps

# View container logs
docker-compose logs backend

# Remove and rebuild
docker-compose down
docker-compose up -d --build --force-recreate
```

#### Permission Denied Errors

```bash
# Fix file permissions (Linux/Mac)
sudo chown -R $USER:$USER .

# Docker permission issues
sudo usermod -aG docker $USER
newgrp docker
```

### Clear Cache and Data

```bash
# Clear Docker cache
docker system prune -a --volumes

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Clear node modules
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ by the Swippter team
- Thanks to all [contributors](https://github.com/akk29/swippter/graphs/contributors)

## 📞 Support

- 📫 Email: support@swippter.com
- 🐛 Issues: [GitHub Issues](https://github.com/akk29/swippter/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/akk29/swippter/discussions)

## 🔗 Links

- [Website](https://swippter.com)
- [Documentation](https://docs.swippter.com)
- [API Reference](https://api.swippter.com/docs)
- [Blog](https://blog.swippter.com)

---

**Note:** This is an educational/demonstration project. For production use, ensure proper security measures, monitoring, and scalability configurations are in place.
