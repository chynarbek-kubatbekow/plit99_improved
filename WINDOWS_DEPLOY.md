# Windows Physical Server Deploy

This guide describes deployment on a physical Windows server.

Recommended stack:

1. Windows Server 2019/2022 or Windows 10/11 Pro on a physical machine
2. Python 3.11
3. PostgreSQL for Windows
4. Waitress as the WSGI application server
5. IIS with URL Rewrite and Application Request Routing as the public reverse proxy
6. NSSM or Windows Task Scheduler to keep the app running

## Production Layout

Recommended directories:

```text
C:\plit99\
  app\
  data\
  venv\
```

Where:

- `app\` is the Django project
- `data\` stores uploaded media and runtime files
- `venv\` stores Python packages

## 1. Install Software

Install:

1. Python 3.11 for Windows
2. Git for Windows
3. PostgreSQL for Windows
4. IIS
5. URL Rewrite for IIS
6. Application Request Routing for IIS
7. NSSM, if you want to run the site as a Windows service

During Python installation, enable `Add python.exe to PATH`.

## 2. Copy Or Clone The Project

Open PowerShell as Administrator:

```powershell
New-Item -ItemType Directory -Force C:\plit99
Set-Location C:\plit99
git clone <YOUR_REPO_URL> app
Set-Location C:\plit99\app
```

If the project is copied manually, place it in `C:\plit99\app`.

## 3. Create Virtual Environment

```powershell
py -3.11 -m venv C:\plit99\venv
C:\plit99\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 4. Create PostgreSQL Database

Open `psql` from the Start menu or run it from the PostgreSQL `bin` folder.

Run:

```sql
CREATE DATABASE plit99_db;
CREATE USER plit99_user WITH PASSWORD 'change-this-password';
ALTER ROLE plit99_user SET client_encoding TO 'UTF8';
ALTER ROLE plit99_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE plit99_user SET timezone TO 'Asia/Bishkek';
GRANT ALL PRIVILEGES ON DATABASE plit99_db TO plit99_user;
```

## 5. Create Data Directory

```powershell
New-Item -ItemType Directory -Force C:\plit99\data\media
```

## 6. Create Environment File

Create `C:\plit99\app\.env` from `.env.example`.

Production example:

```text
DEBUG=False
SECRET_KEY=replace-with-a-long-random-secret
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,server-ip,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
APP_DATA_DIR=C:\plit99\data
DATABASE_URL=postgresql://plit99_user:change-this-password@127.0.0.1:5432/plit99_db
SERVE_MEDIA_FILES=True
WAITRESS_PORT=8000
WAITRESS_THREADS=4
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=change-this-too
```

For a local-only test you may keep SQLite:

```text
DATABASE_URL=sqlite:///C:/plit99/data/db.sqlite3
```

For a real public website, PostgreSQL is recommended.

## 7. Build The Project

```powershell
Set-Location C:\plit99\app
C:\plit99\venv\Scripts\Activate.ps1
.\build.ps1
python manage.py create_admin_if_missing
```

## 8. Test Waitress Manually

```powershell
Set-Location C:\plit99\app
C:\plit99\venv\Scripts\Activate.ps1
.\start.ps1
```

Open:

```text
http://127.0.0.1:8000/
```

If the site opens, continue.

## 9. Run As A Windows Service With NSSM

Download NSSM and place `nssm.exe` somewhere permanent, for example:

```text
C:\nssm\nssm.exe
```

Create the service:

```powershell
C:\nssm\nssm.exe install plit99
```

Use these values in the NSSM window:

```text
Path: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Startup directory: C:\plit99\app
Arguments: -ExecutionPolicy Bypass -NoProfile -File C:\plit99\app\start.ps1
```

Then start it:

```powershell
C:\nssm\nssm.exe start plit99
```

Useful commands:

```powershell
C:\nssm\nssm.exe restart plit99
C:\nssm\nssm.exe stop plit99
C:\nssm\nssm.exe edit plit99
```

## 10. Configure IIS Reverse Proxy

Enable IIS, then install:

1. URL Rewrite
2. Application Request Routing

In IIS Manager:

1. Open the server node.
2. Open `Application Request Routing Cache`.
3. Open `Server Proxy Settings`.
4. Enable proxy.

Create a site for the domain and point it to any empty folder, for example:

```text
C:\plit99\iis-root
```

Add a reverse proxy rule:

```text
Pattern: (.*)
Rewrite URL: http://127.0.0.1:8000/{R:1}
```

The Django app serves static files through WhiteNoise and media files through the project when `SERVE_MEDIA_FILES=True`.

## 11. Firewall

Open only public web ports:

```powershell
New-NetFirewallRule -DisplayName "HTTP 80" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
New-NetFirewallRule -DisplayName "HTTPS 443" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow
```

Keep port `8000` private unless you intentionally want direct local-network access.

## 12. HTTPS

For a public domain, add an SSL certificate in IIS:

1. Use your hosting provider certificate, or
2. Use a Windows ACME client such as `win-acme`.

After the certificate is installed, bind it to the IIS site on port `443`.

## 13. Update After Future Changes

```powershell
Set-Location C:\plit99\app
git pull
C:\plit99\venv\Scripts\Activate.ps1
.\build.ps1
C:\nssm\nssm.exe restart plit99
```

## 14. What Should Be Stored Where

PostgreSQL:

- news
- gallery entries
- categories
- users
- admin data
- sessions

Filesystem in `C:\plit99\data\media`:

- uploaded images
- media files

## 15. Final Check

Check:

1. Main page opens through the domain.
2. `/admin/` opens.
3. Static CSS and JS load correctly.
4. Uploaded images are visible after refresh.
5. Service restarts after Windows reboot.
6. Database data remains after project updates.
