# Deploy To Render

## Files Prepared

- `render.yaml`
- `build.sh`
- `start.sh`
- `.env.example`
- updated `requirements.txt`
- production-ready `plit99_project/settings.py`

## Before You Deploy

1. Push the project to GitHub.
2. In `render.yaml`, change `plit99-web` to your real Render service name if you want a different URL.
3. If you change the service name, also update:
   - `ALLOWED_HOSTS`
   - `CSRF_TRUSTED_ORIGINS`

## Recommended Setup On Render

1. Create a new **Web Service** from your GitHub repo.
2. Render should detect `render.yaml` automatically.
3. For this project, the recommended setup is **SQLite on the Render persistent disk**.
4. No separate Render database is required if you keep the default SQLite setup.
5. If you want the site content to be loaded automatically on the first deploy, add:

```text
LOAD_FIXTURE_ON_DEPLOY=true
```

After the first successful deploy, switch it back to `false` or remove it.

6. If you do not have Render Shell, you can create the Django admin user automatically during deploy with:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your@email.com
DJANGO_SUPERUSER_PASSWORD=your-strong-password
```

The deploy script will create the superuser only if it does not already exist.

## Important Notes

### Database

The project is now configured like this:

- local development: SQLite by default
- Render production: SQLite on the persistent disk by default
- uploaded media: persistent disk via `APP_DATA_DIR`

If `DATABASE_URL` is not set, the app uses SQLite automatically.

For Render, nothing special needs to be "activated" inside Django:

- the persistent disk is attached in `render.yaml`
- `APP_DATA_DIR` points Django to that disk
- `python manage.py migrate` creates the SQLite database there automatically on first deploy

This project also applies SQLite-safe settings for Render:

- `WEB_CONCURRENCY=1` to avoid multi-process write conflicts
- SQLite connection timeout
- WAL mode and related PRAGMA tuning on connect

### Media Files

Your project uses `media/` for uploaded files.

On Render, local filesystem storage is not permanent across deploys unless you attach persistent storage or move media to an external storage service.

This project now stores uploaded media inside `APP_DATA_DIR`. In `render.yaml`, that path is mounted to a persistent disk by default.

That means:

- static files are safe because `collectstatic` + WhiteNoise are configured
- uploaded media files need a persistent disk or external object storage

## Useful Commands After First Deploy

Create admin user:

```bash
python manage.py createsuperuser
```

If you want to load seed content:

```bash
python manage.py seed_data
```

If you want to load the exported database content manually:

```bash
python manage.py loaddata core/fixtures/content.json
```

Run these from the Render shell after the first successful deploy.
