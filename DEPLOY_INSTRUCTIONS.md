# 🚀 JobShell Deployment Instructions

Your JobShell terminal is ready for deployment! Follow these steps:

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon and select "New repository"
3. Repository name: `JobShell` or `swelist-terminal`
4. Description: `🚀 JobShell - Enhanced terminal interface for job hunting`
5. Keep it **Public** for free deployment options
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

## Step 2: Push to GitHub

Run these commands in your terminal:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual values.

## Step 3: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. GitHub will automatically detect the workflow file
4. The deployment will run automatically on every push

## Step 4: Enable GitHub Pages (Optional)

**Important**: You need to enable Pages manually in your repository settings.

1. Go to your repository on GitHub
2. Click "Settings" tab (top of repository page)
3. Scroll down to "Pages" section (left sidebar under "Code and automation")
4. Under "Source", select "GitHub Actions"
5. Click "Save"
6. Your documentation will be available at: `https://YOUR_USERNAME.github.io/JobShell`

**Note**: It may take a few minutes for your site to be published after enabling Pages.

## Step 5: Deploy to Cloud Platform

Choose one of these options:

### 🟢 Vercel (Recommended)
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Import your repository
4. Deploy automatically - no configuration needed!


## Step 6: Configure Environment Variables

For production deployment, set these variables in your platform:

- `FLASK_ENV=production`
- `FLASK_DEBUG=false`
- `PORT=5000` (or platform default)

## 🎉 Your Terminal is Live!

Once deployed, your terminal will be available at your deployment URL.

### Features Available:
- ✅ Multi-theme interface
- ✅ Tab auto-completion
- ✅ Job bookmarking
- ✅ Data export
- ✅ Session persistence
- ✅ Real-time updates

### Test Commands:
```
help
fetch internships
theme blue
bookmark 1
export json bookmarks
```

## 🔧 Troubleshooting

### Common Issues:
1. **Build fails**: Check Python version (3.11 recommended)
2. **Dependencies fail**: Ensure requirements.txt is correct
3. **Socket issues**: Some platforms may need WebSocket configuration
4. **Port issues**: Platform may override PORT environment variable

### Getting Help:
- Check GitHub Actions logs for build errors
- Review platform deployment logs
- Ensure all files are committed and pushed
- Verify environment variables are set correctly

## 🚀 Next Steps

1. **Custom Domain**: Add your own domain in platform settings
2. **SSL Certificate**: Most platforms provide free SSL
3. **Monitoring**: Set up uptime monitoring
4. **Analytics**: Add usage tracking if desired
5. **Backup**: Regular database backups if you add persistence

Enjoy your deployed JobShell terminal! 🎯
