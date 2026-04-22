# Linux Server Deploy

This project can be deployed on a regular Linux server without Render.

Recommended stack:

1. Ubuntu 22.04 or 24.04
2. Python 3.11
3. PostgreSQL
4. Gunicorn
5. Nginx
6. systemd

## Production layout

Recommended directories:

```text
/var/www/plit99/
  app/
  data/
  venv/
```

Where:

- `app/` is the Django project
- `data/` stores uploaded media
- `venv/` stores Python packages

## 1. Install system packages

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx
```

## 2. Clone the project

```bash
sudo mkdir -p /var/www/plit99
sudo chown $USER:$USER /var/www/plit99
cd /var/www/plit99
git clone <YOUR_REPO_URL> app
cd app
```

## 3. Create virtual environment

```bash
python3.11 -m venv /var/www/plit99/venv
source /var/www/plit99/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Create PostgreSQL database

Open PostgreSQL:

```bash
sudo -u postgres psql
```

Run:

```sql
CREATE DATABASE plit99_db;
CREATE USER plit99_user WITH PASSWORD 'change-this-password';
ALTER ROLE plit99_user SET client_encoding TO 'UTF8';
ALTER ROLE plit99_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE plit99_user SET timezone TO 'Asia/Bishkek';
GRANT ALL PRIVILEGES ON DATABASE plit99_db TO plit99_user;
\q
```

## 5. Create persistent data directory

```bash
mkdir -p /var/www/plit99/data/media
```

## 6. Create environment file

```bash
cp .env.example .env
```

Set production values:

```text
DEBUG=False
SECRET_KEY=replace-with-a-long-random-secret
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,server-ip
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
APP_DATA_DIR=/var/www/plit99/data
DATABASE_URL=postgresql://plit99_user:change-this-password@127.0.0.1:5432/plit99_db
SERVE_MEDIA_FILES=True
WEB_CONCURRENCY=1
GUNICORN_TIMEOUT=120
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=change-this-too
```

## 7. Run migrations and collect static

```bash
source /var/www/plit99/venv/bin/activate
export $(grep -v '^#' .env | xargs)
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_admin_if_missing
```

## 8. Test Gunicorn manually

```bash
source /var/www/plit99/venv/bin/activate
export $(grep -v '^#' .env | xargs)
gunicorn plit99_project.wsgi:application --bind 0.0.0.0:8000 --workers 1 --timeout 120
```

If it opens locally on port `8000`, continue.

## 9. Create systemd service

Create `/etc/systemd/system/plit99.service`:

```ini
[Unit]
Description=plit99 django app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/plit99/app
EnvironmentFile=/var/www/plit99/app/.env
ExecStart=/var/www/plit99/venv/bin/gunicorn plit99_project.wsgi:application --bind 127.0.0.1:8000 --workers 1 --timeout 120
Restart=always

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo chown -R www-data:www-data /var/www/plit99/data
sudo chown -R www-data:www-data /var/www/plit99/app
sudo systemctl daemon-reload
sudo systemctl enable plit99
sudo systemctl start plit99
sudo systemctl status plit99
```

## 10. Configure Nginx

Create `/etc/nginx/sites-available/plit99`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/plit99/app/staticfiles/;
    }

    location /media/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/plit99 /etc/nginx/sites-enabled/plit99
sudo nginx -t
sudo systemctl restart nginx
```

## 11. Enable HTTPS

If the site is public, install SSL:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 12. Update after future changes

When you push new code to the server:

```bash
cd /var/www/plit99/app
git pull
source /var/www/plit99/venv/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' .env | xargs)
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart plit99
```

## 13. What should be stored where

1. PostgreSQL:
   - news
   - gallery entries
   - categories
   - users
   - admin data
   - sessions

2. Filesystem in `/var/www/plit99/data/media`:
   - uploaded images
   - media files

## 14. Recommended production choice

For this project, PostgreSQL is strongly recommended over SQLite.

Use SQLite only for:

1. local development
2. quick testing

For a real public school website, PostgreSQL is the correct production database.
