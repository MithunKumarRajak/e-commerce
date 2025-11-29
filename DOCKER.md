# 🐳 Docker Deployment Guide

This guide will help you run the SmartShop e-commerce application using Docker and Docker Compose.

---

## 📋 Prerequisites

- **Docker** installed ([Installation Guide](https://docs.docker.com/get-docker/))
- **Docker Compose** installed ([Installation Guide](https://docs.docker.com/compose/install/))

---

## 🚀 Quick Start with Docker Compose

### 1. Build and Run

```bash
# Build and start all services (Django + PostgreSQL)
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The application will be available at: **http://localhost:8000**

### 2. Create Superuser

```bash
# In a new terminal (while containers are running)
docker-compose exec web python manage.py createsuperuser
```

### 3. Stop Services

```bash
# Stop containers
docker-compose down

# Stop and remove volumes (WARNING: This deletes the database)
docker-compose down -v
```

---

## 🔧 Configuration

### Environment Variables

The `docker-compose.yml` file includes default environment variables. For production, you should:

1. **Copy the example file:**
   ```bash
   cp .env.docker .env
   ```

2. **Edit `.env` and update:**
   - `SECRET_KEY` - Generate a secure random key
   - `DEBUG` - Set to `False` for production
   - `ALLOWED_HOSTS` - Add your domain
   - Email settings (if needed)

3. **Update docker-compose.yml:**
   ```yaml
   web:
     # ... other settings ...
     env_file:
       - .env  # Load from .env file instead of inline environment
   ```

### Generate SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📦 What's Included

The Docker setup includes:

- **PostgreSQL 15** database
- **Django web application** with Gunicorn
- **Automatic migrations** on startup
- **Static file collection** on startup
- **Persistent volumes** for database, static files, and media

---

## 🛠️ Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Run Django Commands

```bash
# Run any Django management command
docker-compose exec web python manage.py <command>

# Examples:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py shell
```

### Access PostgreSQL

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U ecommerce_user -d ecommerce_db

# Common PostgreSQL commands:
# \dt          - List tables
# \d tablename - Describe table
# \q           - Quit
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart web
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up -d --build

# Force rebuild (no cache)
docker-compose build --no-cache
docker-compose up -d
```

---

## 🗄️ Database Management

### Backup Database

```bash
# Create backup
docker-compose exec db pg_dump -U ecommerce_user ecommerce_db > backup.sql

# Or with custom format (recommended)
docker-compose exec db pg_dump -U ecommerce_user -Fc ecommerce_db > backup.dump
```

### Restore Database

```bash
# From SQL file
docker-compose exec -T db psql -U ecommerce_user ecommerce_db < backup.sql

# From dump file
docker-compose exec -T db pg_restore -U ecommerce_user -d ecommerce_db < backup.dump
```

### Reset Database

```bash
# WARNING: This deletes all data!
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 📊 Volumes

Docker Compose creates three volumes:

1. **postgres_data** - PostgreSQL database files
2. **static_volume** - Collected static files
3. **media_volume** - User-uploaded media files

### List Volumes

```bash
docker volume ls | grep e-commerce
```

### Inspect Volume

```bash
docker volume inspect e-commerce_postgres_data
```

---

## 🔍 Troubleshooting

### Issue: Container exits immediately

**Solution:** Check logs for errors
```bash
docker-compose logs web
```

### Issue: Database connection refused

**Solution:** Ensure database is ready
```bash
# Check database status
docker-compose ps

# Wait for database to be ready, then restart web
docker-compose restart web
```

### Issue: Static files not loading

**Solution:** Collect static files
```bash
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart web
```

### Issue: Permission denied on entrypoint script

**Solution:** Make script executable
```bash
chmod +x docker-entrypoint.sh
docker-compose up -d --build
```

### Issue: Port 8000 already in use

**Solution:** Change port in docker-compose.yml
```yaml
ports:
  - "8080:8000"  # Use port 8080 on host
```

---

## 🚀 Production Deployment with Docker

### On Your Server

1. **Install Docker and Docker Compose**

2. **Clone repository:**
   ```bash
   git clone https://github.com/MithunKumarRajak/e-commerce.git
   cd e-commerce
   ```

3. **Create production .env file:**
   ```bash
   cp .env.docker .env
   nano .env  # Edit with production values
   ```

4. **Update docker-compose.yml for production:**
   ```yaml
   web:
     restart: always
     environment:
       - DEBUG=False
       - SECRET_KEY=${SECRET_KEY}
       - ALLOWED_HOSTS=${ALLOWED_HOSTS}
     env_file:
       - .env
   ```

5. **Start services:**
   ```bash
   docker-compose up -d --build
   ```

6. **Set up Nginx reverse proxy** (recommended)

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/e-commerce/staticfiles/;
    }

    location /media/ {
        alias /path/to/e-commerce/media/;
    }
}
```

---

## 📝 Dockerfile Explanation

The Dockerfile does the following:

1. **Base image:** Python 3.11 slim
2. **Install system dependencies:** PostgreSQL client, build tools
3. **Install Python packages:** From requirements.txt
4. **Copy application code**
5. **Create necessary directories**
6. **Set up entrypoint script:** Runs migrations and collectstatic
7. **Expose port 8000**
8. **Start Gunicorn:** Production WSGI server

---

## 🎯 Best Practices

### Development

- Use `docker-compose up` (without -d) to see logs in real-time
- Mount local code as volume for hot-reloading
- Use DEBUG=True for development
- Use console email backend

### Production

- Use `docker-compose up -d` to run in background
- Set DEBUG=False
- Use strong SECRET_KEY
- Set appropriate ALLOWED_HOSTS
- Configure real SMTP for emails
- Set up automated backups
- Use Nginx as reverse proxy
- Enable SSL/HTTPS
- Monitor logs and performance

---

## 🔄 Updating the Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Run new migrations (if any)
docker-compose exec web python manage.py migrate

# Collect new static files
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

## 🆘 Need Help?

- Check application logs: `docker-compose logs -f web`
- Check database logs: `docker-compose logs -f db`
- Verify environment variables are set correctly
- Ensure .env file exists with correct values
- Make sure ports are not already in use

---

**Happy Dockerizing! 🐳**
