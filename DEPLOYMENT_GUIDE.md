# Deployment Guide - School Management System

## Overview
This guide provides step-by-step instructions for deploying the School Management System to various environments including development, staging, and production.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Development Deployment](#development-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Web Server Configuration](#web-server-configuration)
7. [Security Considerations](#security-considerations)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- Web server (Apache/Nginx for production)
- Database server (PostgreSQL recommended for production)

### Software Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Additional production dependencies
pip install gunicorn psycopg2-binary
```

## Development Deployment

### Local Development Setup
```bash
# Clone repository
git clone <repository-url>
cd School_management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate with sample data
python manage.py populate_db

# Run development server
python manage.py runserver
```

### Development Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_USE_TLS=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

## Production Deployment

### 1. Server Preparation

#### Ubuntu/Debian Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib git -y

# Create project user
sudo adduser schoolmgmt
sudo usermod -aG sudo schoolmgmt
```

#### Create Project Directory
```bash
# Switch to project user
sudo su - schoolmgmt

# Create project directory
mkdir -p /home/schoolmgmt/School_management
cd /home/schoolmgmt/School_management

# Clone repository
git clone <repository-url> .
```

### 2. Python Environment Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install production dependencies
pip install gunicorn psycopg2-binary
```

### 3. Database Configuration

#### PostgreSQL Setup
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE school_management;
CREATE USER schooluser WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE school_management TO schooluser;
ALTER USER schooluser CREATEDB;
\q
```

### 4. Environment Configuration

#### Production Settings
Create `/home/schoolmgmt/School_management/.env`:
```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=postgresql://schooluser:secure_password_here@localhost:5432/school_management
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,server-ip-address

# Email Configuration (Gmail example)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static/Media files
STATIC_ROOT=/home/schoolmgmt/School_management/staticfiles
MEDIA_ROOT=/home/schoolmgmt/School_management/media
```

#### Update settings.py for production
```python
# Add to settings.py
import os
from pathlib import Path
import dj_database_url

# Load environment variables
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.getenv('STATIC_ROOT', BASE_DIR / 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### 5. Database Migration and Setup
```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Populate with sample data (optional)
python manage.py populate_db
```

### 6. Gunicorn Configuration

#### Create Gunicorn service file
`/etc/systemd/system/school-management.service`:
```ini
[Unit]
Description=School Management Django App
After=network.target

[Service]
User=schoolmgmt
Group=www-data
WorkingDirectory=/home/schoolmgmt/School_management
Environment="PATH=/home/schoolmgmt/School_management/venv/bin"
EnvironmentFile=/home/schoolmgmt/School_management/.env
ExecStart=/home/schoolmgmt/School_management/venv/bin/gunicorn --workers 3 --bind unix:/home/schoolmgmt/School_management/school_management.sock myproject.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### Start and enable service
```bash
sudo systemctl daemon-reload
sudo systemctl start school-management
sudo systemctl enable school-management
sudo systemctl status school-management
```

### 7. Nginx Configuration

#### Create Nginx site configuration
`/etc/nginx/sites-available/school-management`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/schoolmgmt/School_management;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        root /home/schoolmgmt/School_management;
        expires 30d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/schoolmgmt/School_management/school_management.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

#### Enable site and restart Nginx
```bash
sudo ln -s /etc/nginx/sites-available/school-management /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 8. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/school_management
      - DEBUG=False
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=school_management
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - web
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## Environment Configuration

### Development
- DEBUG = True
- SQLite database
- Local email backend
- Simplified security settings

### Staging
- DEBUG = False
- PostgreSQL database
- Real email configuration
- Production-like security
- Same domain as production (staging.domain.com)

### Production
- DEBUG = False
- PostgreSQL database
- Full security headers
- SSL/TLS encryption
- Monitoring and logging

## Security Considerations

### 1. Secret Key Management
- Use environment variables
- Generate strong, unique keys
- Rotate keys regularly

### 2. Database Security
- Use strong passwords
- Limit database user permissions
- Regular security updates
- Backup encryption

### 3. Web Server Security
- Keep Nginx/Apache updated
- Configure security headers
- Use SSL/TLS certificates
- Regular security audits

### 4. Application Security
- Input validation
- SQL injection prevention
- XSS protection
- CSRF protection
- File upload restrictions

### 5. Server Security
- Regular system updates
- Firewall configuration
- SSH key authentication
- Fail2ban for intrusion prevention

## Backup Strategy

### Database Backups
```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/home/schoolmgmt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump school_management > $BACKUP_DIR/backup_$DATE.sql
gzip $BACKUP_DIR/backup_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

### Media Files Backup
```bash
# Rsync media files
rsync -av /home/schoolmgmt/School_management/media/ /backup/location/media/
```

### Automated Backups
Add to crontab:
```bash
# Daily database backup at 2 AM
0 2 * * * /home/schoolmgmt/scripts/backup_db.sh

# Weekly media backup on Sundays at 3 AM
0 3 * * 0 /home/schoolmgmt/scripts/backup_media.sh
```

## Monitoring and Maintenance

### Log Management
```bash
# Configure log rotation
sudo vim /etc/logrotate.d/school-management

/home/schoolmgmt/School_management/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 schoolmgmt schoolmgmt
}
```

### Health Checks
```bash
# Simple health check script
#!/bin/bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://your-domain.com/admin/)
if [ $STATUS -ne 200 ]; then
    echo "Website is down! Status: $STATUS"
    # Send alert
fi
```

### Performance Monitoring
- Monitor response times
- Database query performance
- Memory and CPU usage
- Disk space monitoring

## Troubleshooting

### Common Issues
1. **Static files not loading**: Check STATIC_ROOT and run collectstatic
2. **Database connection errors**: Verify credentials and connectivity
3. **Permission errors**: Check file/directory permissions
4. **Service won't start**: Check systemd logs with `journalctl -u school-management`

### Log Locations
- Django logs: `/home/schoolmgmt/School_management/logs/`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog`
- Gunicorn logs: `journalctl -u school-management`

## Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Multiple application servers
- Database read replicas
- CDN for static files

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching
- Use Redis for sessions

## Maintenance Schedule

### Weekly
- Check system logs
- Verify backup integrity
- Monitor performance metrics
- Security updates

### Monthly
- Database maintenance
- Clean up old files
- Review security logs
- Performance optimization

### Quarterly
- Full security audit
- Dependency updates
- Disaster recovery testing
- Capacity planning
