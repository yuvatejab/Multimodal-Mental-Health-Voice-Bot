# Deployment Guide

This guide covers deploying the Mental Health Voice Bot to various platforms.

## Option 1: Render.com (Recommended - Free)

### Prerequisites
- GitHub account
- Groq API key
- Render.com account (free)

### Steps

1. **Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will detect `render.yaml` automatically
   - Click "Apply"

3. **Configure Environment Variables**
   - Go to the backend service
   - Add environment variable:
     - Key: `GROQ_API_KEY`
     - Value: Your Groq API key
   - Save changes

4. **Update Frontend API URL**
   - Go to the frontend service
   - Update `VITE_API_URL` environment variable:
     - Value: `https://mental-health-voice-bot-backend.onrender.com`
   - Save and redeploy

5. **Access Your App**
   - Frontend: `https://mental-health-voice-bot-frontend.onrender.com`
   - Backend: `https://mental-health-voice-bot-backend.onrender.com`

### Free Tier Limitations
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 750 hours/month of runtime (enough for 1 service running 24/7)

## Option 2: Vercel (Frontend) + Render (Backend)

### Backend on Render

1. Create a new Web Service
2. Connect GitHub repository
3. Configure:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add `GROQ_API_KEY` environment variable

### Frontend on Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd frontend
vercel
```

3. Set environment variable:
```bash
vercel env add VITE_API_URL production
# Enter your backend URL: https://your-backend.onrender.com
```

4. Redeploy:
```bash
vercel --prod
```

## Option 3: Railway.app

1. Go to [Railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Add two services:
   - Backend: Python service
   - Frontend: Static site
4. Configure environment variables
5. Deploy

## Option 4: Docker Deployment

### Build Images

**Backend:**
```bash
cd backend
docker build -t mental-health-bot-backend .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key mental-health-bot-backend
```

**Frontend:**
```bash
cd frontend
docker build -t mental-health-bot-frontend .
docker run -p 80:80 mental-health-bot-frontend
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://backend:8000
```

Run:
```bash
docker-compose up -d
```

## Option 5: AWS/GCP/Azure

### Backend (EC2/Compute Engine/VM)

1. Launch a VM instance
2. SSH into the instance
3. Install Python 3.11+
4. Clone repository
5. Set up virtual environment
6. Install dependencies
7. Set environment variables
8. Run with systemd or supervisor

### Frontend (S3/Cloud Storage + CloudFront/CDN)

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Upload `dist/` contents to S3/Cloud Storage
3. Configure bucket for static website hosting
4. Set up CloudFront/CDN for HTTPS
5. Update CORS settings on backend

## Post-Deployment Checklist

- [ ] Backend health check works: `/api/health`
- [ ] Frontend loads correctly
- [ ] Voice recording works (requires HTTPS)
- [ ] API calls succeed from frontend to backend
- [ ] Multiple languages work
- [ ] Audio playback works
- [ ] Crisis detection triggers correctly
- [ ] Mobile responsive design works
- [ ] HTTPS enabled (required for microphone access)

## Monitoring

### Render.com
- View logs in Render dashboard
- Set up email alerts for service failures

### Custom Monitoring
- Add application logging
- Use services like Sentry for error tracking
- Monitor API response times
- Track Groq API usage

## Scaling

### If You Exceed Free Tier Limits

1. **Groq API**: Upgrade to paid plan or use alternative LLM APIs
2. **Hosting**: Upgrade to paid tiers on Render/Vercel
3. **Caching**: Implement Redis for session storage
4. **Database**: Add PostgreSQL for conversation history
5. **CDN**: Use CloudFlare for static assets

## Security Considerations

- Never commit `.env` files
- Use environment variables for all secrets
- Enable HTTPS (required for microphone access)
- Implement rate limiting
- Add authentication if needed
- Regular dependency updates
- Monitor for suspicious activity

## Troubleshooting

### "Service Unavailable" on Render
- Free tier services spin down after 15 minutes
- First request wakes up the service (~30s delay)
- Consider upgrading to paid tier for always-on

### CORS Errors
- Verify backend CORS_ORIGINS includes frontend URL
- Check that frontend VITE_API_URL is correct
- Ensure both services are deployed and running

### Microphone Not Working
- HTTPS is required for microphone access
- Check browser permissions
- Verify SSL certificate is valid

## Cost Estimates

### Free Tier (Current Setup)
- Groq API: Free (14,400 requests/day)
- Edge TTS: Free (unlimited)
- Render.com: Free (750 hours/month)
- **Total: $0/month**

### Paid Tier (If Scaling)
- Groq API: Pay-as-you-go (~$0.10/1M tokens)
- Render.com: $7/month per service
- Domain: ~$12/year
- **Total: ~$14-20/month**

## Support

For deployment issues:
1. Check service logs
2. Verify environment variables
3. Test API endpoints directly
4. Check GitHub Issues
5. Open a new issue with deployment logs

