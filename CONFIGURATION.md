# Configuration Guide

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DB_NAME=school_management
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Gmail SMTP)
EHU=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password

# Django Settings
SECRET_KEY=your_very_long_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: Media and Static Files
MEDIA_ROOT=/path/to/media/files
STATIC_ROOT=/path/to/static/files
```

## Gmail Setup for Email Features

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password in `EMAIL_PASSWORD`

3. **Configure Email Settings** in your `.env`:
   ```env
   EHU=your_gmail@gmail.com
   EMAIL_PASSWORD=your_16_character_app_password
   ```

## Database Setup

### SQLite (Development)
No additional setup required. Django will create `db.sqlite3` automatically.

### PostgreSQL (Production)
1. **Install PostgreSQL**
2. **Create Database**:
   ```sql
   CREATE DATABASE school_management;
   CREATE USER school_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE school_management TO school_user;
   ```
3. **Update `.env`** with your PostgreSQL credentials

### MySQL (Alternative)
1. **Install MySQL**
2. **Create Database**:
   ```sql
   CREATE DATABASE school_management;
   CREATE USER 'school_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON school_management.* TO 'school_user'@'localhost';
   ```

## Static Files Configuration

### Development
```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

### Production
```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use WhiteNoise for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]
```

## Media Files Setup

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Create media directories:
```bash
mkdir -p media/students
```

## Security Settings

### Production Security
```python
# settings.py for production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security headers
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

## Performance Optimization

### Database Optimization
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'conn_max_age': 600,
        }
        # ... other settings
    }
}
```

### Caching (Optional)
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Troubleshooting

### Common Issues

1. **Email not sending**:
   - Check Gmail app password
   - Verify SMTP settings
   - Check firewall/antivirus

2. **Static files not loading**:
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT

3. **Database connection errors**:
   - Verify database credentials
   - Check database server is running
   - Ensure database exists

4. **Permission errors**:
   - Check file permissions
   - Ensure media directory is writable

### Debug Mode

Enable debug mode for development:
```env
DEBUG=True
```

This will show detailed error pages with stack traces.
