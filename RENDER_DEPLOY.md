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
3. You do not need to hardcode `ALLOWED_HOSTS` or `CSRF_TRUSTED_ORIGINS` for the default `onrender.com` domain. The Django settings pick up the Render hostname automatically.

## Recommended Setup On Render

1. Create a new **Web Service** from your GitHub repo.
2. Render should detect `render.yaml` automatically.
3. For a free/open deployment, use the no-database mode configured in `render.yaml`.
4. The app will use the built-in JSON snapshot `core/fixtures/site_content.json` and in-repo media files instead of a Render database.
5. In Render env vars, set:

```text
ENABLE_DATABASE=false
BOOTSTRAP_DATABASE=false
LOAD_FIXTURE_ON_DEPLOY=false
SERVE_MEDIA_FILES=true
```

6. If you later decide to use paid persistent storage, switch to `ENABLE_DATABASE=true`, `BOOTSTRAP_DATABASE=true`, and add `APP_DATA_DIR=/data` to Render env vars.

If you do not have Render Shell, you can create the Django admin user automatically during deploy with:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your@email.com
DJANGO_SUPERUSER_PASSWORD=your-strong-password
```

The deploy script will create the superuser only if it does not already exist.

## Important Notes

### Database

This project supports two Render modes:

- Free/no-disk mode: `ENABLE_DATABASE=false`, `BOOTSTRAP_DATABASE=false`.
  In this mode the site renders from `core/fixtures/site_content.json` and from in-repo media files.
- Paid/disk mode: `ENABLE_DATABASE=true`, `BOOTSTRAP_DATABASE=true`, and `APP_DATA_DIR=/data`.
  In that case the app stores SQLite and media on a persistent disk.

If `DATABASE_URL` is not set and `ENABLE_DATABASE=false`, the app does not use persistent database storage.

For free Render deployment, no special disk mount is required.

This project also applies SQLite-safe settings for Render when database mode is enabled:

- `WEB_CONCURRENCY=1` to avoid multi-process write conflicts
- SQLite connection timeout
- PRAGMA tuning on connect
- `SQLITE_JOURNAL_MODE=DELETE` on Render to avoid WAL/shm issues on hosted disks
- signed-cookie sessions on Render by default, so `/admin/` does not depend on SQLite session writes

### Admin Panel

If you want to sign in to `/admin/` right after deploy, set:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your@email.com
DJANGO_SUPERUSER_PASSWORD=your-strong-password
```

The deploy script runs:

```bash
python manage.py create_admin_if_missing
```

and now also refreshes the JSON content snapshot automatically.

### Media Files

Your project uses `media/` for uploaded files.

On Render, local filesystem storage is not permanent across deploys unless you attach persistent storage or move media to an external storage service.

For the free/no-disk deployment mode, rely on media files that are committed into the repository under `media/`.
The app can serve those files from the repo using `SERVE_MEDIA_FILES=true`.

That means:

- static files are safe because `collectstatic` + WhiteNoise are configured
- news pages using repo-stored cover images will work without a Render disk
- uploaded media through admin will not persist after redeploy without persistent storage

### Content Snapshot Fallback

News and gallery content are now duplicated into JSON snapshot files automatically:

- runtime snapshot: `APP_DATA_DIR/content_snapshot/site_content.json`
- project mirror snapshot: `core/fixtures/site_content.json`

Uploaded images are also mirrored into the project `media/` directory when possible.

If the database becomes unavailable later, public pages (`/news/`, `/gallery/`, `/media/`, news detail pages) fall back to the snapshot JSON plus media files instead of crashing.

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

If you want to refresh the runtime/public snapshot manually:

```bash
python manage.py refresh_content_snapshot
```

Run these from the Render shell after the first successful deploy.
