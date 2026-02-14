# Client Gallery Generator — Usage & Deployment Guide

This document explains safety considerations for making the repository public, how to run the project locally, and a simple, practical way to deploy using Fly.io (Docker). Fly.io is a commonly used option with a free tier that supports containerized apps and managed Postgres.

## Is it safe to make the repository public?
- Code being public is fine — but NEVER commit secrets, credentials, private keys, or production databases.
- Sensitive files to remove before publishing:
  - `.env`, `.env.local`, any file containing API keys or passwords
  - `Gallery/db.sqlite3` (or any DB dump)
  - `/media/` contents if they contain private images
  - SSH keys, TLS certs, and other credentials
- If secrets were committed previously, rotate credentials immediately and scrub history (BFG or `git filter-repo`).
- Enable GitHub security features: secret scanning, Dependabot alerts, branch protection, and required reviews.

## Quick local setup
1. Copy the template and edit secrets:

```bash
cp .env.template .env
# edit .env and set DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS
```

2. Create a virtualenv and install dependencies (or use Docker):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run migrations and start the dev server:

```bash
python Gallery/manage.py migrate
python Gallery/manage.py createsuperuser   # optional
python Gallery/manage.py runserver
```

4. (Alternative) Use Docker Compose:

```bash
cp .env.template .env
docker compose up --build
```

## Deploying (recommended: Fly.io)
This is a straightforward container-based deployment flow. Fly.io offers a free tier suitable for small projects; confirm current pricing/tier constraints before relying on it.

1. Install `flyctl`: https://fly.io/docs/getting-started/installing-flyctl/

2. Authenticate and create an app:

```bash
flyctl auth login
flyctl launch --name client-gallery --copy-config --no-deploy
```

3. Add a Postgres instance (recommended for production):

```bash
flyctl postgres create --name client-gallery-db
# After creation, follow flyctl output to attach and set DATABASE_URL secret
```

4. Set environment variables (secrets) on Fly:

```bash
flyctl secrets set DJANGO_SECRET_KEY="<strong-secret>" DJANGO_DEBUG=False DJANGO_ALLOWED_HOSTS=client-gallery.fly.dev
# If using Backblaze/Cloudinary, set their keys here too
```

5. Deploy the Docker image:

```bash
flyctl deploy
```

6. Run migrations and collectstatic on the remote instance:

```bash
flyctl ssh console -C "python Gallery/manage.py migrate --noinput"
flyctl ssh console -C "python Gallery/manage.py collectstatic --noinput"
```

7. Verify the app and scale instances if necessary:

```bash
flyctl status
flyctl scale count 1    # change instance count
```

## Media & static files
- Static files: `collectstatic` writes to `staticfiles/` which WhiteNoise serves in production.
- Media (user-uploaded): for resilience and scaling, use object storage (Backblaze B2, AWS S3, or Cloudinary). Configure credentials as environment variables and update `settings.py` accordingly.

## Security checklist before making the repo public
- Remove `.env` and local DB from the repository and add them to `.gitignore` (already added).
- Audit commits for accidentally committed secrets; if found, rotate keys and scrub history.
- Use environment variables for all credentials.
- Add `CODEOWNERS`, enable branch protection, enforce signed commits or reviews for protected branches.
- Enable GitHub Advanced Security features where available.

## If you find leaked secrets
1. Immediately rotate or revoke the leaked credentials.
2. Remove the secret from the repo and scrub history with `git filter-repo` or BFG.
3. Force-push a cleaned branch and inform any collaborators of the incident.

## Next actions I can take for you
- Run `git rm --cached Gallery/db.sqlite3` and commit to stop tracking the DB.
- Audit the repository for committed secrets and propose a scrub plan using `git filter-repo`.
- Add an example `fly.toml` or GitHub Actions workflow to automate deploys.

---
If you want, I can: run the `git rm` step now, scan the repo for obvious secrets, or add a ready-to-use `fly.toml` and CI workflow. Which would you like next?
