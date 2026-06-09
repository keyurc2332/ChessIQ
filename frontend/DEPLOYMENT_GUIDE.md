# ChessIQ Dashboard - Deployment Guide

## Step 1: Create GitHub Repository

```bash
cd /path/to/ChessIQ
git init
git add .
git commit -m "ChessIQ Dashboard - Ready for deployment"
git branch -M main
git remote add origin https://github.com/yourusername/chessiq-dashboard.git
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud (FREE!)

1. Go to: https://streamlit.io/cloud
2. Click "New app"
3. Connect your GitHub repo
4. Select branch: `main`
5. Select file path: `app.py`
6. Click "Deploy"

**That's it! Your app is now live!** 🎉

## Step 3: Share Your Dashboard

Your app will be available at: