# Swippter

> An ecommerce platform for fast fashion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Typescript](https://img.shields.io/badge/Typescript-3.13-green)](https://www.python.org/)
[![Redis](https://img.shields.io/badge/Redis-3.13-green)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-3.13-green)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.13-green)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-3.13-green)](https://www.python.org/)


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

### Design Document

[Swippter Design Document](https://www.notion.so/Swippter-Design-Document-2a901d4de5ee804f9bccd7441898614a)

![Swippter Application Architecture](docs/backend/swippter-design.svg)

### Technology Stack

**Backend:**
- Python - 3.13
- Django + DRF
- MySQL (database)
- Redis (caching)
- Celery/RabbitMQ (task queue)
- UV - Package Manager

**Frontend:**
- React.js
- TypeScript
- Tailwind CSS / Material-UI
- NodeJS - 22.
- Bun - 1.3.4

**Infrastructure:**
- Docker & Docker Compose
- Kubernetes

**Documentation:**
- Swagger / Swagger UI - API Documentation
- Open API - API Documentation

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (29.1.2+)
- **Docker Compose** (v2.40.3-desktop.1)
- **Python** (3.13.3+)
- **Node.js** (22.15.1+) and npm/yarn
- **Git**
- **kubectl** (for Kubernetes deployment)
  - Client Version: v1.34.1
  - Kustomize Version: v5.7.1

### System Requirements

- **CPU:** 2+ cores
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** 10GB free space

## 📁 Project Structure

```
swippter/
+---backend
|   +---.venv
|   |   +---Scripts
|   +---swippter
|       +---app
|       |   +---core                    # backend core code
|       |   +---management              # application run time commands
|       |   |   +---commands
|       |   +---migrations
|       |   +---models                  # database models
|       |   |   +---patterns            # patterns on database objects
|       |   +---routes                  # application routes
|       |   +---services                # backend services / business logic
|       |   +---tests                   # test suite
|       |   |   +---functional
|       |   +---utils                   # utilities functions
|       |   +---views                   # API views
|       +---swippter
+---frontend
+---infra
    +---config                          # config for services
    +---docker                                  
    |   +---dependencies                # backend dependencies docker file
    |   +---server                      # server docker file
    +---env                             # env file for services
    +---kubernetes
    |   +---mysql                       # mysql kubernetes file
    |   +---nginx                       # nginx kubernetes file
    |   +---rabbitmq                    # rabbitmq kubernetes file
    |   +---redis                       # redis kubernetes file
    |   +---server                      # server kubernetes file
    +---manual
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
cd backend/swippter
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Database settings
DB="mysql"
DATABASE="swippterdb"
DBUSER="dbuser"
DBPASSWORD="rootpassword"
DBHOST="localhost"
DBPORT="3306"
# Django framework settings
DEBUG=True
SECRET_KEY="!efo=n)#gcu8_-_15u81i-e3bre!2o-3inse+wca+bmp!+$w9-yp3djan3k4!tzw29"
# Django framework settings 
THROTTLE_RATE="2000/min"
# Admin user credentials
ADMIN_EMAIL="a@a.com"
ADMIN_PASSWORD="test@1234"
# Redis settings
REDIS="redis://localhost:6379"
# Celery settings
CELERY_BROKER_URL="amqp://guest:guest@localhost:5672/"
CELERY_TASK_SERIALIZER="json"
# Email Vendor settings
TRIGGER_MAIL_SWITCH=False
INFO_EMAIL="info@swippter.com"
RESET_EMAIL="reset@swippter.com"
EMAIL_HOST="sandbox.smtp.mailtrap.io"
EMAIL_HOST_USER="email_host_user"
EMAIL_HOST_PASSWORD="email_host_password"
EMAIL_PORT="25"

```

```bash
# Create backend environment file
cd infra/env
cp .mysql.env.example .mysql.env
```

Edit `.mysql.env` with your configuration:

```env
MYSQL_DATABASE=swippterdb
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_USER=dbuser
MYSQL_PASSWORD=rootpassword
MYSQL_ALLOW_EMPTY_PASSWORD=YES
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

```

### 3. Install Dependencies

#### Backend

```bash
cd backend

# Install dependencies
uv sync

# Go to project directory
cd swippter

# Run database migrations
python manage.py makemigrations app
python manage.py makemigrations
python manage.py migrate app
python manage.py migrate

2025-12-08 19:52:39,803:app.core.logging:INFO - logging:logging.py:setup:47 --- Setting up logger - objID - 1597121486128
2025-12-08 19:52:39,803:app.core.logging:INFO - config:config.py:setup_logger:17 --- logger setup complete
2025-12-08 19:52:39,810:app.core.logging:INFO - config:config.py:setup_redis:24 --- Successfully connected to Redis!
2025-12-08 19:52:39,814:app.core.logging:INFO - config:config.py:setup_redis:30 --- Retrieved value: hello redis
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK

# Create superuser (admin)
python manage.py create_admin
username: admin@admin.com
password: test@1234
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
# Before running make sure to make .env and .mysql.env file in your local directory

# From the project root directory
cd infra/docker

# Build and start all services
docker compose build dependencies

# create services
docker compose up nginx server redis mysql rabbitmq --force-recreate

# Check running services
docker-compose ps

# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: deletes data)
docker-compose down -v
```

**Services will be available at:**
- Backend API: http://localhost
- API Docs: http://localhost/api/schema/swagger-ui/
- Admin Panel: http://localhost/admin
- MySQL: localhost:3306
- Redis: localhost:6379

### Option 2: Local Development

#### Start Backend

```bash
cd backend

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Run Development server (before running make sure redis, rabbitmq and mysql are running)
cd infra/docker
docker compose up redis mysql rabbitmq --force-recreate
python manage.py runserver

2025-12-08 19:53:10,292:app.core.logging:INFO - logging:logging.py:setup:47 --- Setting up logger - objID - 1732918697264
2025-12-08 19:53:10,293:app.core.logging:INFO - config:config.py:setup_logger:17 --- logger setup complete
2025-12-08 19:53:10,310:app.core.logging:INFO - config:config.py:setup_redis:24 --- Successfully connected to Redis!
2025-12-08 19:53:10,317:app.core.logging:INFO - config:config.py:setup_redis:30 --- Retrieved value: hello redis
2025-12-08 19:53:10,785:app.core.logging:INFO - logging:logging.py:setup:47 --- Setting up logger - objID - 1677889953072
2025-12-08 19:53:10,785:app.core.logging:INFO - config:config.py:setup_logger:17 --- logger setup complete
2025-12-08 19:53:10,796:app.core.logging:INFO - config:config.py:setup_redis:24 --- Successfully connected to Redis!
2025-12-08 19:53:10,799:app.core.logging:INFO - config:config.py:setup_redis:30 --- Retrieved value: hello redis
Performing system checks...

System check identified no issues (0 silenced).
December 08, 2025 - 19:53:10
Django version 5.2.8, using settings 'swippter.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/

```

#### Start Frontend - IN_PROGRESS

```bash
cd frontend

# Development server
bun run dev

# Build for production
bun run build

# Serve production build
serve -s build -l 3000
```

#### Start Background Workers (Celery)

```bash
cd backend

# Start Celery worker
celery -A swippter.celery worker --pool=solo --detach --loglevel=info

# Start Flower (Celery monitoring)
celery -A swippter.celery flower --port=5555
```

### Option 3: Individual Docker Containers

```bash
# Build dependencies
cd infra/docker
docker compose build dependencies
docker compose up frontend server redis mysql rabbitmq --force-recreate
```

## ☸️ Infrastructure Deployment

### Docker Compose Commands

```bash

# Setting up env for backend before deployment
EDIT /backend/swippter/.env
# Database settings
DB="mysql"
DATABASE="swippterdb"
DBUSER="dbuser"
DBPASSWORD="rootpassword"
DBHOST="mysql" # point to container
DBPORT="3306"
# Django framework settings
DEBUG=False
SECRET_KEY='django-insecure-15+$3k4=e3b+bmp!wca8_-_n)#w9-yp3329!2+u81i!tzw!efo'
# Django rest framework settings 
THROTTLE_RATE='2000/min'
# Admin user credentials
ADMIN_EMAIL="a@a.com"
ADMIN_PASSWORD="test@1234"
# Redis settings
REDIS="redis://redis:6379" # point to container
# Celery settings
CELERY_BROKER_URL='amqp://guest:guest@rabbimq:5672/' # point to container
CELERY_TASK_SERIALIZER='json'
# Mailtrap settings
TRIGGER_MAIL_SWITCH=False
INFO_EMAIL="info@swippter.com"
RESET_EMAIL="reset@swippter.com"
EMAIL_HOST="sandbox.smtp.mailtrap.io"
EMAIL_HOST_USER="email_host_user"
EMAIL_HOST_PASSWORD="email_host_password"
EMAIL_PORT="25"
```


```bash
cd infra/docker

# build Dependencies
docker compose build dependencies

# Start Services
docker compose up nginx server redis mysql rabbitmq --force-recreate

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

# Config for nginx deployment
kubectl create configmap nginx-config --from-file=default.conf=../config/default.conf

# Create static storage
kubectl apply -f static-pvc.yaml

# ENV config for mysql service
kubectl create secret generic mysql-secret --from-env-file=../env/.mysql.env

# Deploy mysql
kubectl apply -f mysql/pvc.yaml
kubectl apply -f mysql/deployment.yaml
kubectl apply -f mysql/service.yaml

# Deploy redis
kubectl apply -f redis/deployment.yaml
kubectl apply -f redis/service.yaml

# Deploy nginx
kubectl apply -f nginx/deployment.yaml
kubectl apply -f nginx/service.yaml

# Deploy server
kubectl apply -f server/deployment.yaml
kubectl apply -f server/service.yaml

# Deploy rabbitmq
kubectl apply -f rabbitmq/deployment.yaml
kubectl apply -f rabbitmq/service.yaml

############### Automated Script for above commands ######################

# Windows

start-w.bat # for setup
clean-w.bat # for clean up

```

### Monitoring & Logging

```bash
# View application logs
docker-compose logs -f backend frontend

# Kubernetes logs
kubectl logs -f deployment/backend -n swippter

# Redis monitoring
docker-compose exec redis redis-cli INFO
```

## 📚 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost/docs
- **ReDoc**: http://localhost/redoc
- **OpenAPI JSON**: http://localhost/openapi.json

### Sample API Endpoints

```bash
# Health check / Check API
curl http://localhost:8000/api/v1/

# Browse products
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

# Run all tests with coverage
coverage run manage.py test

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

#### Redis not running

```bash
2025-12-08 19:34:07,229:app.core.logging:INFO - logging:logging.py:setup:47 --- Setting up logger - objID - 2890361975248
2025-12-08 19:34:07,229:app.core.logging:INFO - config:config.py:setup_logger:17 --- logger setup complete
2025-12-08 19:34:14,489:app.core.logging:CRITICAL - config:config.py:setup_redis:34 --- Redis connection error: Error 11001 connecting to redis:6379. getaddrinfo failed.
```

```bash
# Run redis 
docker compose run redis
```


#### Database Connection Error

```bash
# Run database

docker compose run mysql
```

#### Rabbitmq Connection Error

```bash
# Run Rabbitmq

docker compose run mysql
```


## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ by the Swippter team
- Thanks to all [contributors](https://github.com/akk29/swippter/graphs/contributors)

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/akk29/swippter/issues)

## 🔗 Links

- [Website](https://www.github.com/akk29/swippter)
- [Documentation](https://www.github.com/akk29/swippter)
- [API Reference](https://www.github.com/akk29/swippter)

---

**Note:** This is an educational/demonstration project. For production use, ensure proper security measures, monitoring, and scalability configurations are in place.
