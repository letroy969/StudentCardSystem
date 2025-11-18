# Deploying to Fly.io - Step by Step Guide

## Prerequisites
- GitHub account (your repo is already there)
- Fly.io account (free)

## Step 1: Install Fly CLI

**Windows (PowerShell):**
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

## Step 2: Sign Up and Login

```bash
fly auth signup    # Creates account (use GitHub login)
fly auth login     # Login to your account
```

## Step 3: Initialize Your App

```bash
cd C:\card1
fly launch
```

When prompted:
- **App name**: `unione-digital-id` (or choose your own)
- **Region**: Choose closest to you (e.g., `iad` for US East, `lhr` for London)
- **PostgreSQL**: No (we'll use PlanetScale MySQL)
- **Redis**: No
- **Deploy now**: No (we'll set up environment variables first)

## Step 4: Create Persistent Volume for Uploads

```bash
fly volumes create uploads_volume --region iad --size 3
```

## Step 5: Set Environment Variables

```bash
# Set all environment variables
fly secrets set SECRET_KEY="your-super-secret-key-here"
fly secrets set FLASK_ENV="production"
fly secrets set DB_HOST="your-planetscale-host"
fly secrets set DB_PORT="3306"
fly secrets set DB_NAME="student_card_db"
fly secrets set DB_USER="your-planetscale-user"
fly secrets set DB_PASSWORD="your-planetscale-password"
fly secrets set MAIL_SERVER="smtp.gmail.com"
fly secrets set MAIL_PORT="587"
fly secrets set MAIL_USE_TLS="True"
fly secrets set MAIL_USERNAME="umpdigitalcard@gmail.com"
fly secrets set MAIL_PASSWORD="your-gmail-app-password"
fly secrets set MAIL_DEFAULT_SENDER="umpdigitalcard@gmail.com"
fly secrets set SUPPORT_RECIPIENT="umpdigitalcard@gmail.com"
```

**After first deploy, get your app URL and set:**
```bash
fly secrets set PROFILE_BASE_URL="https://unione-digital-id.fly.dev"
```

## Step 6: Deploy

```bash
fly deploy
```

## Step 7: Check Your App

```bash
fly open    # Opens your app in browser
fly logs    # View logs
fly status  # Check app status
```

## Important Notes

1. **Database**: Use PlanetScale (free MySQL) - set DB_HOST, DB_USER, DB_PASSWORD
2. **File Storage**: Persistent volume is mounted at `/app/static/uploads`
3. **Port**: Fly.io uses PORT env var (set to 8080 in fly.toml)
4. **Scaling**: Free tier includes 3 VMs - you can scale down to 1 for cost savings:
   ```bash
   fly scale count 1
   ```

## Troubleshooting

- **View logs**: `fly logs`
- **SSH into app**: `fly ssh console`
- **Check status**: `fly status`
- **Restart app**: `fly apps restart unione-digital-id`

## Cost

- **Free tier**: 3 shared VMs, 3GB storage, 160GB transfer/month
- **After free tier**: Pay-as-you-go, very affordable (~$1-5/month for small apps)

## Advantages of Fly.io

✅ Generous free tier (3 VMs, 3GB storage)
✅ Persistent file storage (volumes)
✅ Global edge deployment
✅ Automatic HTTPS
✅ Easy scaling
✅ Great documentation

