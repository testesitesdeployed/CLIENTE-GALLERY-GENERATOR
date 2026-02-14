# Complete Deployment Guide for Photon Client Gallery

This guide walks you through deploying the Photon Client Gallery application from start to finish, using **Fly.io** as the hosting platform (recommended) with a managed PostgreSQL database.

---

## Table of Contents

1. [Before You Start](#before-you-start)
2. [Step 1: Prepare Your Repository](#step-1-prepare-your-repository)
3. [Step 2: Set Up Fly.io Account](#step-2-set-up-flyio-account)
4. [Step 3: Install Required Tools](#step-3-install-required-tools)
5. [Step 4: Deploy to Fly.io](#step-4-deploy-to-flyio)
6. [Step 5: Configure Production Environment](#step-5-configure-production-environment)
7. [Step 6: Verify Your Deployment](#step-6-verify-your-deployment)
8. [Optional: Configure Media Storage](#optional-configure-media-storage)
9. [Local Development Setup](#local-development-setup)

---

## Before You Start

### Prerequisites

- A GitHub account (or able to work with Git)
- A computer with Git installed
- A web browser
- An email address for registering on Fly.io

### What You'll Get

After completing this deployment guide, you'll have:
- A live Django application running on Fly.io
- A managed PostgreSQL database
- Automatic HTTPS encryption
- A custom domain capability
- Free or low-cost hosting with Fly.io's pricing

---

## Step 1: Prepare Your Repository

Before deploying to production, clean up your repository to ensure no secrets are exposed.

### 1.1 Remove Local Database and Secrets

If the local database (`Gallery/db.sqlite3`) is currently tracked in Git, remove it:

```bash
cd /path/to/your/project
git rm --cached Gallery/db.sqlite3
git commit -m "Remove local database from tracking"
git push origin main
```

### 1.2 Verify `.gitignore` Contains Sensitive Files

Ensure your `.gitignore` file includes:

```
.env
.env.local
db.sqlite3
/media/
.venv/
```

If these are missing, add them and commit:

```bash
# Edit or create .gitignore
echo ".env
db.sqlite3
/media/" >> .gitignore
git add .gitignore
git commit -m "Ensure .gitignore protects sensitive files"
git push origin main
```

### 1.3 Verify No Secrets in Commit History

If you've accidentally committed secrets before, use a tool like `git filter-repo` to scrub them:

```bash
# Install git filter-repo if needed
pip install git-filter-repo

# Example: remove a file called .env from history
git filter-repo --path .env --invert-paths
git push --force-with-lease origin main
```

---

## Step 2: Set Up Fly.io Account

### 2.1 Sign Up for Fly.io

1. Go to https://fly.io
2. Click **"Sign Up"** in the top right corner
3. Enter your email address
4. Choose to sign up with GitHub (recommended) or create a new account
5. Verify your email address
6. Choose your plan (Free tier is available)

### 2.2 Log In to Fly.io Dashboard

After sign-up, go to https://fly.io/dashboard to verify you can access your account.

---

## Step 3: Install Required Tools

### 3.1 Install `flyctl` Command-Line Tool

**On macOS (with Homebrew):**
```bash
brew install flyctl
```

**On Linux (Ubuntu/Debian):**
```bash
curl -L https://fly.io/install.sh | sh
```

**On Windows:**
Download the installer from https://fly.io/docs/getting-started/installing-flyctl/ or use Chocolatey:
```bash
choco install flyctl
```

### 3.2 Verify Installation

```bash
flyctl version
```

You should see a version number (e.g., `0.1.xx`).

---

## Step 4: Deploy to Fly.io

### 4.1 Authenticate with Fly.io

Open your terminal and run:

```bash
flyctl auth login
```

This will open your browser to log in with your Fly.io account. After logging in, return to your terminal.

### 4.2 Launch Your App on Fly.io

Navigate to your project directory and run:

```bash
cd /path/to/your/project
flyctl launch --name client-gallery --copy-config --no-deploy
```

Replace `client-gallery` with a unique app name (Fly.io apps need globally unique names; consider adding a suffix like your username).

This command:
- Creates a `fly.toml` configuration file
- Sets up your app on Fly.io
- Does NOT deploy yet (the `--no-deploy` flag prevents immediate deployment)

### 4.3 Create a PostgreSQL Database

Run the following command to create a managed PostgreSQL database:

```bash
flyctl postgres create --name client-gallery-db
```

**Important:** Replace `client-gallery-db` with a unique name (e.g., `client-gallery-db-username`).

The output will show instructions for attaching the database. Follow the prompts:

```bash
flyctl postgres attach client-gallery-db
```

This automatically sets the `DATABASE_URL` secret on your app (you'll see instructions confirming this).

---

## Step 5: Configure Production Environment

### 5.1 Generate a Strong Django Secret Key

Run this Python command to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output (it's a long random string).

### 5.2 Set Environment Secrets on Fly.io

Use `flyctl` to set all required environment variables (secrets):

```bash
flyctl secrets set \
  DJANGO_SECRET_KEY="<paste-the-secret-key-here>" \
  DJANGO_DEBUG="False" \
  DJANGO_ALLOWED_HOSTS="client-gallery.fly.dev"
```

Replace:
- `<paste-the-secret-key-here>` with the secret key you generated above
- `client-gallery.fly.dev` with your actual Fly.io app URL (you can customize this later with a custom domain)

**Optional:** If you plan to use Backblaze B2 for media storage, also set:

```bash
flyctl secrets set \
  B2_KEY_ID="your-key-id" \
  B2_APP_KEY="your-app-key" \
  B2_BUCKET_NAME="your-bucket-name" \
  B2_ENDPOINT_URL="your-endpoint-url"
```

### 5.3 Verify Secrets Were Set

```bash
flyctl secrets list
```

You should see all the secrets you just set (values are hidden for security).

---

## Step 6: Deploy Your Application

### 6.1 Deploy the Docker Image

```bash
flyctl deploy
```

This command:
- Builds a Docker image from your `Dockerfile`
- Uploads it to Fly.io
- Deploys it to your app
- Takes 2-5 minutes to complete

Watch the output for any errors. Once complete, you'll see a message like:
```
Release v1 created and deployed successfully
```

### 6.2 Run Database Migrations

After deployment, run migrations on the production database:

```bash
flyctl ssh console -C "cd Gallery && python manage.py migrate --noinput"
```

This creates all database tables from Django models.

### 6.3 Collect Static Files

```bash
flyctl ssh console -C "cd Gallery && python manage.py collectstatic --noinput"
```

This prepares CSS, JavaScript, and admin assets for production serving.

### 6.4 Create a Superuser (Admin Account)

```bash
flyctl ssh console -C "cd Gallery && python manage.py createsuperuser"
```

Follow the prompts to create your admin username, email, and password. **Save these credentials securely.**

---

## Step 7: Verify Your Deployment

### 7.1 Check App Status

```bash
flyctl status
```

You should see your app as `Running` with at least one healthy instance.

### 7.2 View Your Live Site

```bash
flyctl open
```

Or manually visit: `https://client-gallery.fly.dev` (replace with your actual app name).

You should see the gallery homepage.

### 7.3 Access the Admin Panel

Visit: `https://client-gallery.fly.dev/admin`

Log in with the superuser credentials you created in Step 6.4. If successful, you can now:
- Add photo galleries
- Upload photos in bulk
- Create password-protected galleries
- Manage users and permissions

---

## Optional: Configure Media Storage

By default, uploaded photos are stored locally on the server. For production with multiple instances or persistent storage, configure Backblaze B2 or AWS S3.

### 8.1 Using Backblaze B2

1. **Create a Backblaze B2 Account:**
   - Go to https://www.backblaze.com/b2/cloud-storage.html
   - Sign up and create an account

2. **Create a B2 Bucket:**
   - In the B2 dashboard, click **"Buckets"** → **"Create a New Bucket"**
   - Name it something like `client-gallery-photos`
   - Set it to **Private**
   - Note the bucket name

3. **Generate API Credentials:**
   - Go to **Account Settings** → **Application Keys**
   - Click **"Create New Application Key"**
   - Set **Allowed Capabilities** to `readFiles`, `writeFiles`, `deleteFiles`
   - Copy the **Application Key ID** and **Application Key** (you won't see it again)

4. **Set Credentials on Fly.io:**
   ```bash
   flyctl secrets set \
     B2_KEY_ID="application-key-id" \
     B2_APP_KEY="application-key" \
     B2_BUCKET_NAME="client-gallery-photos" \
     B2_ENDPOINT_URL="https://f000.backblazeb2.com"
   ```

5. **Deploy:**
   ```bash
   flyctl deploy
   ```

After deployment, Django will automatically use Backblaze B2 for media uploads.

### 8.2 Using AWS S3

If you prefer AWS S3, configure these environment variables:

```bash
flyctl secrets set \
  AWS_ACCESS_KEY_ID="your-key" \
  AWS_SECRET_ACCESS_KEY="your-secret" \
  AWS_STORAGE_BUCKET_NAME="your-bucket-name" \
  AWS_S3_REGION_NAME="us-east-1"
```

Ensure the app's `settings.py` is configured to use S3 when these are set.

---

## Local Development Setup

If you want to run the application locally for testing or development:

### For Quick Local Testing (without Docker)

```bash
# 1. Clone and navigate to the project
cd /path/to/your/project

# 2. Create environment file
cp .env.template .env
# Edit .env and set:
#   DJANGO_SECRET_KEY="your-secret-key"
#   DJANGO_DEBUG="True"
#   DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"

# 3. Set up Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python Gallery/manage.py migrate

# 6. Create admin user (optional)
python Gallery/manage.py createsuperuser

# 7. Start development server
python Gallery/manage.py runserver
```

Visit http://localhost:8000 in your browser.

### For Local Testing with Docker

```bash
# 1. Create environment file
cp .env.template .env
# Edit .env as above

# 2. Build and run with Docker Compose
docker compose up --build

# 3. In another terminal, run migrations
docker compose exec web python Gallery/manage.py migrate

# 4. Create superuser (optional)
docker compose exec web python Gallery/manage.py createsuperuser
```

Visit http://localhost:8000 in your browser.

---

## Troubleshooting

### App Won't Deploy

- Check logs: `flyctl logs`
- Verify `fly.toml` has correct settings
- Ensure `DATABASE_URL` is set: `flyctl secrets list`

### Database Errors After Deployment

- Run migrations again: `flyctl ssh console -C "cd Gallery && python manage.py migrate"`
- Check if migrations succeeded: `flyctl logs`

### Admin Panel Not Accessible

- Verify superuser exists: `flyctl ssh console -C "cd Gallery && python manage.py createsuperuser"`
- Check `DJANGO_ALLOWED_HOSTS` includes your domain

### Static Files Missing (CSS/JS Not Loading)

- Run collectstatic: `flyctl ssh console -C "cd Gallery && python manage.py collectstatic --noinput"`
- Restart the app: `flyctl restart`

---

## Security Checklist

Before considering your deployment complete:

- [ ] No `.env` file committed to Git
- [ ] No `db.sqlite3` in version control
- [ ] `DJANGO_DEBUG=False` in production
- [ ] Strong `DJANGO_SECRET_KEY` generated and set
- [ ] All secrets set via `flyctl secrets`
- [ ] PostgreSQL database attached
- [ ] Superuser created with strong password
- [ ] HTTPS enabled (automatic on Fly.io)
- [ ] Custom domain configured (if desired)
- [ ] Media storage configured (optional but recommended)

---

## Next Steps

- **Add Your Domain:** In Fly.io dashboard, configure a custom domain
- **Set Up Monitoring:** Enable alerts in the Fly.io dashboard
- **Backup Strategy:** Plan regular database backups
- **Content Management:** Use the admin panel to add galleries and photos
