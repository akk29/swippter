# Swippter

> An ecommerce platform for fast fashion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Maintainability](https://qlty.sh/gh/akk29/projects/swippter/maintainability.svg)](https://qlty.sh/gh/akk29/projects/swippter)
[![codecov](https://codecov.io/gh/akk29/swippter/graph/badge.svg?token=8AVEMH80AT)](https://codecov.io/gh/akk29/swippter)

<img src="docs/project-icon.svg" alt="Alt text" width="200" height="200" />

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#%EF%B8%8F-architecture) 
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Infrastructure Deployment](#%EF%B8%8F-infrastructure-deployment)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

Swippter is a modern ecommerce platform designed for fast fashion retail. Application provides a complete solution for managing products, orders, customers, and inventory with a scalable microservices architecture.

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

![Swippter Application Architecture](docs/backend/swippter-design.svg)

### Technology Stack

**Backend:**
- Language - Python
- Framework - Django
- Database - MySQL
- Caching - Redis
- Queue - Celery
- Broker - RabbitMQ
- Package Manager - UV

**Frontend:**
- Langauge - TypeScript
- Framework - ReactJS & Tailwind CSS
- Runtime - Bun

**Infrastructure:**
- Docker & Docker Compose
- Kubernetes

**Documentation:**
- API Documentation - Swagger / Swagger UI + Open API

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** : v29.1.2+
- **Docker Compose** : v2.40.3-desktop.1
- **Python** : v3.13.3+
- **Node.js** : v22.15.1+ and bun
- **Git** : v2.46.0
- **kubectl** - for Kubernetes deployment
  - Client Version : v1.34.1
  - Kustomize Version : v5.7.1

### System Requirements

- **CPU:** 2+ cores
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** 10GB free space


## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/akk29/swippter.git
cd swippter
```

### 2. Environment Configuration

Create environment files for settings and cofiguration.

#### Backend Environment (.env)

```bash
# Create backend environment file
cd backend/swippter
cp .env.example .env
```
<details>
<summary>Edit `.env` with your configuration:</summary>

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
# Frontend Settings
FRONT_URL="http://localhost:8000"
```
</details>

#### MySQL Environment (.env)

```bash
# Create MySQL environment file
cd infra/env
cp .mysql.env.example .mysql.env
```
<details>
<summary>Edit `.mysql.env` with your configuration:</summary>

```env
MYSQL_DATABASE=swippterdb
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_USER=dbuser
MYSQL_PASSWORD=rootpassword
MYSQL_ALLOW_EMPTY_PASSWORD=YES
```
</details>

#### Otel Environment Setup (.env)

```bash
# Create Otel environment file
cd infra/env
cp .otel.env.example .otel.env
```

<details>
<summary>Edit `.otel.env` with your configuration:</summary>

```env
OTEL_SERVICE_NAME=swippter-backend
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_INSECURE=true
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
```
</details>

#### Frontend Environment (.env)

```bash
# Create frontend environment file
cd frontend
cp .env.example .env
```

<details>
<summary>Edit `.env` with your configuration:</summary>

```env
REACT_APP_backend_url=http://localhost:8000/api
NODE_ENV=development
```

</details>

### 3. Install Dependencies

#### Backend

```bash
cd backend

# Install dependencies
uv sync

# Go to project directory
cd swippter
```

#### Frontend

```bash
cd frontend

# Install dependencies
bun install
```

## 🏃 Running the Application

### Option 1: Development Setup

<details>

<summary>Start Backend</summary>

```bash
cd backend

# Activate virtual environment
# Linux/Mac
source .venv/bin/activate  
# or
# Windows
.venv\Scripts\activate     

# Run Dependencies server (before running make sure redis, rabbitmq and mysql are running)
cd infra/docker
docker compose up redis mysql rabbitmq --force-recreate

cd backend/swippter
.venv\scripts\activate # windows

# Run database migrations
python manage.py makemigrations app
python manage.py makemigrations
python manage.py migrate

482:app.core.logging:INFO - logging:logging.py:setup:47 --- Setting up logger - objID - 1701358784016
494:app.core.logging:INFO - config:config.py:setup_logger:17 --- logger setup complete
501:app.core.logging:INFO - config:config.py:setup_redis:24 --- Successfully connected to Redis!
502:app.core.logging:INFO - config:config.py:setup_redis:30 --- Retrieved value: hello redis
Operations to perform:
  Apply all migrations: admin, app, auth, contenttypes, sessions, token_blacklist
Running migrations:

# Create superuser (admin) visit http://localhost:8000/admin in browser
python manage.py create_admin

# running development server
python manage.py runserver

Performing system checks...
System check identified no issues (0 silenced).
Django version 5.2.8, using settings 'swippter.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/
```

</details>

<details>
<summary>Start Background Workers (Celery)</summary>

```bash
cd backend

# Start Celery worker
celery -A swippter.celery worker --pool=solo --detach --loglevel=info

celery -A swippter.celery worker --pool=solo --loglevel=info # windows

# Start Flower (Celery monitoring)
celery -A swippter.celery flower --port=5555
```

</details>

<details>
<summary>Start Frontend</summary>

```bash
cd swippter/frontend

# Development server
bun run dev

# Build for production
bun run build
```

</details>

**Services will be available at:**
- Backend API: http://localhost:8000/api/v1/
- API Docs: http://localhost:8000/api/schema/swagger-ui/
- Admin Panel: http://localhost:8000/admin
- Frontend : http://localhost:3000

### Option 2: Docker Compose (Recommended for Live Demo)

This is the easiest way to run the entire application & observability stack.
Before running make sure to make update these file in your local directory to make container networking connection properly.
- Backend - [.env](#backend-environment-env) ```/backend/swippter/.env ```
- Database - [.mysql.env](#mysql-environment-setup-env) ```/infra/env/.mysql.env```
- Observability - [.otel.env](#otel-environment-setup-env) ```/infra/env/.otel.env ```
- Frontend - [.env](#frontend-environment-env) ```/frontend/.env```

```bash
# now update /backend/swippter/.env to point application code to container services
DBHOST="mysql"
REDIS="redis://redis:6379"
CELERY_BROKER_URL="amqp://guest:guest@rabbitmq:5672/" 

# From the project root directory
cd infra/docker

# Build and start all services
docker compose up --force-recreate

# Check running services
docker-compose ps

# Stop all services
docker-compose down
```

**Services will be available at:**
- Backend API: http://localhost/api/v1/
- API Docs: http://localhost/api/schema/swagger-ui/
- Admin Panel: http://localhost/admin
- Frontend : http://localhost
- Grafana : http://localhost:3200 - admin:admin

## ☸️ Infrastructure Deployment

⚠️ Please follow security guidelines for deployment based on your Cloud Provider. Project is currently is in development mode. Security related checklist will be available soon.

### Docker Compose Deployment

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
# Frontend Settings
FRONT_URL="http://localhost:8000"

# run via docker compose
cd infra/docker
docker compose up --force-recreate 
```

**Services will be available at:**
- Backend API: http://localhost/api/v1/
- API Docs: http://localhost/api/schema/swagger-ui/
- Admin Panel: http://localhost/admin
- Frontend : http://localhost

### Kubernetes Deployment

#### Prerequisites

```bash
# Ensure kubectl is configured
kubectl version

Client Version: v1.34.1
Kustomize Version: v5.7.1
Server Version: v1.34.1
```

#### Deploy to Kubernetes

```bash
cd infra/kubernetes

############### Automated Script for bore commands - Single Command Setup  ######################

# Windows
start-w.bat # for running services 
clean-w.bat # for cleaning services

############### Individual commadns for running services  ######################

# Create namespace
kubectl create namespace swippter

# Deploy mysql
kubectl create secret generic mysql-secret --from-env-file=../env/.mysql.env -n swippter
kubectl apply -f mysql/pvc.yaml -n swippter
kubectl apply -f mysql/deployment.yaml -n swippter
kubectl apply -f mysql/service.yaml -n swippter

# Deploy redis
kubectl apply -f redis/deployment.yaml -n swippter
kubectl apply -f redis/service.yaml -n swippter

# Deploy frontend
kubectl create configmap nginx-config --from-file=default.conf=../config/default.conf -n swippter
kubectl apply -f static-pvc.yaml -n swippter
kubectl apply -f frontend/deployment.yaml -n swippter
kubectl apply -f frontend/service.yaml -n swippter

# Deploy server
kubectl create secret generic otel-env-secret --from-env-file=../env/.otel.env -n swippter
kubectl apply -f server/deployment.yaml -n swippter
kubectl apply -f server/service.yaml -n swippter

# Deploy rabbitmq
kubectl apply -f rabbitmq/deployment.yaml -n swippter
kubectl apply -f rabbitmq/service.yaml -n swippter

# Deploy otel-collector
kubectl apply -f observability/otel-collector/config.yaml -n swippter
kubectl apply -f observability/otel-collector/deployment.yaml -n swippter
kubectl apply -f observability/otel-collector/service.yaml -n swippter

# Deploy loki
kubectl apply -f observability/loki/pvc.yaml -n swippter
kubectl apply -f observability/loki/deployment.yaml -n swippter
kubectl apply -f observability/loki/service.yaml -n swippter

# Deploy tempo
kubectl apply -f observability/tempo/config.yaml -n swippter
kubectl apply -f observability/tempo/pvc.yaml -n swippter
kubectl apply -f observability/tempo/deployment.yaml -n swippter
kubectl apply -f observability/tempo/service.yaml -n swippter

# Deploy promtail
kubectl apply -f observability/promtail/config.yaml -n swippter
kubectl apply -f observability/promtail/rbac.yaml -n swippter
kubectl apply -f observability/promtail/deployment.yaml -n swippter
kubectl apply -f observability/promtail/service.yaml -n swippter

# Deploy prometheus
kubectl apply -f observability/prometheus/config.yaml -n swippter
kubectl apply -f observability/prometheus/deployment.yaml -n swippter
kubectl apply -f observability/prometheus/service.yaml -n swippter

# Deploy grafana
kubectl apply -f observability/grafana/config.yaml -n swippter
kubectl apply -f observability/grafana/deployment.yaml -n swippter
kubectl apply -f observability/grafana/service.yaml -n swippter
```

**Services will be available at:**
- Backend API: http://localhost/api/v1/
- API Docs: http://localhost/api/schema/swagger-ui/
- Admin Panel: http://localhost/admin
- Frontend : http://localhost

## 📚 API Documentation

Once the backend is running for development setup, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc
- **OpenAPI JSON**: http://localhost:8000/api/schema
- **Admin Portal**: http://localhost:8000/admin

### Sample API Endpoints

```bash
# Health check / Check API
curl --request GET \
  --url http://localhost:8000/api/v1/health \
  --header 'Content-Type: application/json'
{
	"status": 200,
	"message": "success",
	"data": {
		"version": "v1",
		"method": "GET",
		"status": "healthy",
		"database": "connected",
		"redis": "connected"
	}
}

# User signup
curl -X POST http://localhost:8000/api/v1/signup \
  -H "Content-Type: application/json" \
  -d '{ "role" : 3, "first_name" : "test", "last_name" : "user", "email" : "a2@a.com", "password" : "test@123" } '

# User signin
curl -X POST http://localhost:8000/api/v1/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secure123"}'

# User signout
curl --request POST \
  --url http://localhost:8000/api/v1/signout \
  --header 'Content-Type: application/json' \
  --data '{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3NzAyODE5LCJpYXQiOjE3Njc3MDI1MTksImp0aSI6IjYwYTcwMzlkYThlYzQ4ZTQ5MDcxZDFlNGJmMjBhOGUzIiwidXVpZCI6ImU4ZmM4OGM4LWJkYjUtNDBhZS1iNjMxLWM4NDI3NjZkMGRkNyJ9.sRMzFNiUJtC9kSOvGICbY2bH2_KNIFRwn2xMiXYd4zM"
}'

# User forget 
curl --request POST \
  --url http://localhost:8000/api/v1/forgot \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3NzAyODE5LCJpYXQiOjE3Njc3MDI1MTksImp0aSI6IjYwYTcwMzlkYThlYzQ4ZTQ5MDcxZDFlNGJmMjBhOGUzIiwidXVpZCI6ImU4ZmM4OGM4LWJkYjUtNDBhZS1iNjMxLWM4NDI3NjZkMGRkNyJ9.sRMzFNiUJtC9kSOvGICbY2bH2_KNIFRwn2xMiXYd4zM'

# User verify
curl --request POST \
  --url http://localhost:8000/api/v1/verify \
  --header 'Content-Type: application/json' \
  --data '{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3NzAyODE5LCJpYXQiOjE3Njc3MDI1MTksImp0aSI6IjYwYTcwMzlkYThlYzQ4ZTQ5MDcxZDFlNGJmMjBhOGUzIiwidXVpZCI6ImU4ZmM4OGM4LWJkYjUtNDBhZS1iNjMxLWM4NDI3NjZkMGRkNyJ9.sRMzFNiUJtC9kSOvGICbY2bH2_KNIFRwn2xMiXYd4zM"
}'

# User refresh
curl --request POST \
  --url http://localhost:8000/api/v1/refresh \
  --header 'Content-Type: application/json' \
  --data '{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3NzAyODE5LCJpYXQiOjE3Njc3MDI1MTksImp0aSI6IjYwYTcwMzlkYThlYzQ4ZTQ5MDcxZDFlNGJmMjBhOGUzIiwidXVpZCI6ImU4ZmM4OGM4LWJkYjUtNDBhZS1iNjMxLWM4NDI3NjZkMGRkNyJ9.sRMzFNiUJtC9kSOvGICbY2bH2_KNIFRwn2xMiXYd4zM"
}'

# User change-password
curl --request POST \
  --url http://localhost:8000/api/v1/change-password \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3NzAyODE5LCJpYXQiOjE3Njc3MDI1MTksImp0aSI6IjYwYTcwMzlkYThlYzQ4ZTQ5MDcxZDFlNGJmMjBhOGUzIiwidXVpZCI6ImU4ZmM4OGM4LWJkYjUtNDBhZS1iNjMxLWM4NDI3NjZkMGRkNyJ9.sRMzFNiUJtC9kSOvGICbY2bH2_KNIFRwn2xMiXYd4zM'
```

## 🧪 Testing

### Backend Tests

```bash
cd backend/swippter

# Run all tests with coverage
coverage run manage.py test
coverage html -d coverage_html
```

### Frontend Tests

```bash
cd frontend

# Run tests

# Run with coverage

# Run E2E tests

# Run specific test file

```

## 🐛 Troubleshooting

### Common Issues

- #### Redis not running

```bash
828:app.core.logging:INFO - logging:logging.py:setup:47 --- Setting up logger - objID - 2009449615024
839:app.core.logging:INFO - config:config.py:setup_logger:17 --- logger setup complete
894:app.core.logging:CRITICAL - config:config.py:setup_redis:34 --- Redis connection error: Error 10061 connecting to localhost:6379. No connection could be made because the target machine actively refused it.

# Run redis 
docker compose run redis
# check in env and configure according to your environment
REDIS="redis://localhost:6379" # local setip
REDIS="redis://redis:6379" # docker or kubernetes setup
```


- #### Database Connection Error

```bash
# Run database

docker compose run mysql
```

- #### Rabbitmq Connection Error

```bash
# Error logs

backend -> .env
DEBUG=False # only then will be able to see this error on devlopment terminal
# Celery settings
CELERY_BROKER_URL="amqp://guest:guest@localhost:5672/" # local development
CELERY_BROKER_URL="amqp://guest:guest@rabbitmq:5672/"  # docker or kubernetes setup
raise ConnectionError(str(exc)) from exc
kombu.exceptions.OperationalError: [WinError 10061] No connection could be made because the target machine actively refused it

# run rabbit
docker compose run rabbitmq
```

- #### Kubernetes Error

```bash
Client Version: v1.34.1
Kustomize Version: v5.7.1
error: Get "https://kubernetes.docker.internal:6443/version?timeout=32s": read tcp 127.0.0.1:60227->127.0.0.1:6443: wsarecv: An existing connection was forcibly closed by the remote host. - error from a previous attempt: EO

# Run kuberntes from Docker Destop and create a cluster
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