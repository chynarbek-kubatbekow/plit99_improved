# Deploy Guide: Render and Linux

This project is now prepared for a normal production deployment flow:

- Django app runs through Gunicorn
- database is the primary source of truth
- media files live in `MEDIA_ROOT`
- static files are served with WhiteNoise
- no JSON snapshot fallback
- no mirrored media copy inside the repository
- Django admin uses the standard built-in interface again

## Recommended Production Architecture

For a real school website, use this setup:

1. Render Web Service for the Django app
2. Render PostgreSQL for the database
3. Persistent Disk mounted at `/var/data` for uploaded media

This is already reflected in [render.yaml](./render.yaml).

## Important Production Notes

1. News, categories, gallery entries, users, and admin data are stored in PostgreSQL.
2. Uploaded images are not stored inside PostgreSQL in the current architecture.
3. Uploaded images are stored in `MEDIA_ROOT`, which should point to persistent storage.
4. On Render, that means a persistent disk.
5. On a Linux VPS, that means a normal persistent directory on the server.

## Before First Deploy

Prepare these things first:

1. Push the latest project code to GitHub.
2. Make sure `requirements.txt`, `build.sh`, `start.sh`, and `render.yaml` are committed.
3. Decide whether you will deploy:
   - through Render Blueprint using `render.yaml`
   - manually through the Render dashboard
   - on your own Linux server
4. Prepare admin credentials:
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_EMAIL`
   - `DJANGO_SUPERUSER_PASSWORD`

## Option 1: Render Blueprint Deploy

This is the easiest and cleanest path.

### What the blueprint creates

The current [render.yaml](./render.yaml) defines:

1. A PostgreSQL database named `plit99-db`
2. A Python web service named `plit99-web`
3. A persistent disk mounted to `/var/data`
4. `DATABASE_URL` from the Render database connection string
5. `APP_DATA_DIR=/var/data`

### Step-by-step

1. Commit and push your project to GitHub.
2. Open Render Dashboard.
3. Go to `Blueprints`.
4. Click `New Blueprint Instance`.
5. Select your GitHub repository.
6. Render will detect `render.yaml`.
7. Review the services:
   - PostgreSQL database
   - web service
8. Before clicking apply, add these environment variables for the web service if you want admin creation on first boot:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=strong-password-here
```

9. Click `Apply`.
10. Wait for the first deploy to finish.

### What happens during startup

On each start, [start.sh](./start.sh) runs:

1. `python manage.py migrate --noinput`
2. `python manage.py create_admin_if_missing`
3. Gunicorn start

That means:

- database tables are created automatically
- admin user can be created automatically
- the site starts in one consistent flow

## Option 2: Manual Deploy on Render

If you do not want to use Blueprint:

### Create the database

1. In Render, create a PostgreSQL database.
2. Copy its internal connection string.

### Create the web service

1. Create a new Web Service from your GitHub repository.
2. Set runtime to `Python 3`.
3. Use:

```text
Build Command: bash build.sh
Start Command: bash start.sh
```

### Add environment variables

Set these values:

```text
PYTHON_VERSION=3.11.11
DEBUG=false
SECRET_KEY=<generate-a-long-secret>
DATABASE_URL=<internal-postgres-url-from-render>
APP_DATA_DIR=/var/data
SERVE_MEDIA_FILES=true
WEB_CONCURRENCY=1
GUNICORN_TIMEOUT=120
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=strong-password-here
```

### Add persistent disk

1. Open your web service in Render.
2. Go to `Disks`.
3. Add a persistent disk.
4. Mount path: `/var/data`
5. Choose disk size according to expected uploads.

Without the disk:

- the site will still boot
- PostgreSQL data will persist
- uploaded media files will be lost after redeploy/restart

## Option 3: Deploy on Your Own Linux Server

This project also works on a normal Ubuntu server.

### Recommended server stack

1. Ubuntu 22.04 or 24.04
2. Python 3.11
3. PostgreSQL 15 or newer
4. Nginx
5. systemd
6. Virtual environment inside the project

### Example directory layout

```text
/var/www/plit99/
  app/         -> project code
  data/        -> media files
  venv/        -> Python virtualenv
```

### Linux setup steps

1. Install system packages:

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx
```

2. Clone the project:

```bash
sudo mkdir -p /var/www/plit99
sudo chown $USER:$USER /var/www/plit99
cd /var/www/plit99
git clone <YOUR_REPO_URL> app
cd app
```

3. Create virtualenv and install dependencies:

```bash
python3.11 -m venv /var/www/plit99/venv
source /var/www/plit99/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

4. Create PostgreSQL database:

```bash
sudo -u postgres psql
```

Then in PostgreSQL:

```sql
CREATE DATABASE plit99_db;
CREATE USER plit99_user WITH PASSWORD 'change-this-password';
ALTER ROLE plit99_user SET client_encoding TO 'UTF8';
ALTER ROLE plit99_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE plit99_user SET timezone TO 'Asia/Bishkek';
GRANT ALL PRIVILEGES ON DATABASE plit99_db TO plit99_user;
\q
```

5. Create media directory:

```bash
mkdir -p /var/www/plit99/data/media
```

6. Create environment file:

```bash
cp .env.example .env
```

Then update `.env` with production values:

```text
DEBUG=False
SECRET_KEY=<long-random-secret>
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
APP_DATA_DIR=/var/www/plit99/data
DATABASE_URL=postgresql://plit99_user:change-this-password@127.0.0.1:5432/plit99_db
SERVE_MEDIA_FILES=True
WEB_CONCURRENCY=1
GUNICORN_TIMEOUT=120
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=strong-password-here
```

7. Run migrations and collect static:

```bash
source /var/www/plit99/venv/bin/activate
export $(grep -v '^#' .env | xargs)
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_admin_if_missing
```

8. Test Gunicorn:

```bash
gunicorn plit99_project.wsgi:application --bind 0.0.0.0:8000
```

9. Create a systemd service:

`/etc/systemd/system/plit99.service`

```ini
[Unit]
Description=plit99 django site
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

10. Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable plit99
sudo systemctl start plit99
sudo systemctl status plit99
```

11. Configure Nginx:

`/etc/nginx/sites-available/plit99`

```nginx
server {
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

12. Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/plit99 /etc/nginx/sites-enabled/plit99
sudo nginx -t
sudo systemctl restart nginx
```

13. Add HTTPS with Certbot if this is a public site.

## First Production Checklist

After deploy, verify:

1. `/` loads
2. `/news/` loads
3. `/gallery/` loads
4. `/admin/` opens
5. Admin login works
6. You can create news through admin
7. Uploaded image is visible after page refresh
8. Uploaded image is still visible after service restart
9. Static files load without 404 errors
10. Database data stays after redeploy

## Common Mistakes

1. `ALLOWED_HOSTS` does not include your domain
2. `CSRF_TRUSTED_ORIGINS` is missing `https://`
3. `DATABASE_URL` points to SQLite in production
4. No persistent disk for uploaded media
5. Weak or missing `SECRET_KEY`
6. Running multiple app workers with SQLite

## Should You Move from SQLite to PostgreSQL?

Yes. For this project, production should use PostgreSQL.

### Why PostgreSQL is better here

1. Better reliability under real concurrent traffic
2. Better admin/session behavior in production
3. Safer writes than SQLite for a public site with admin activity
4. Easier future scaling
5. Better backup and recovery options

### When SQLite is still acceptable

SQLite is acceptable only for:

1. local development
2. quick demos
3. temporary internal preview environments

For the real public lyceum site, PostgreSQL is the right choice.
