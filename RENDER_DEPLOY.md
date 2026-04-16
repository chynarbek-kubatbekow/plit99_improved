# Deploy To Render

## Files Prepared

- `render.yaml`
- `build.sh`
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
3. For production, use a **PostgreSQL** database and set its connection string as `DATABASE_URL`.
4. If you want the site content to be loaded automatically on the first deploy, add:

```text
LOAD_FIXTURE_ON_DEPLOY=true
```

After the first successful deploy, switch it back to `false` or remove it.

5. If you do not have Render Shell, you can create the Django admin user automatically during deploy with:

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
- Render production: PostgreSQL via `DATABASE_URL`

If `DATABASE_URL` is not set, the app falls back to SQLite.

### Media Files

Your project uses `media/` for uploaded files.

On Render, local filesystem storage is not permanent across deploys unless you attach persistent storage or move media to an external storage service.

That means:

- static files are safe because `collectstatic` + WhiteNoise are configured
- uploaded media files need special handling

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
