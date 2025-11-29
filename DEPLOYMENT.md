# 🚀 Production Deployment Checklist

## Pre-Deployment

### Security
- [ ] Set `DEBUG=False` in production `.env`
- [ ] Generate and set new `SECRET_KEY` (minimum 50 characters)
- [ ] Update `ALLOWED_HOSTS` with actual domain(s)
- [ ] Review and enable all security settings
- [ ] Remove any test/debug code
- [ ] Ensure no sensitive data in version control

### Database
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set `DATABASE_URL` environment variable
- [ ] Test database connection
- [ ] Plan backup strategy
- [ ] Set up automated backups

### Email
- [ ] Configure SMTP settings
- [ ] Test email sending functionality
- [ ] Set up email templates
- [ ] Configure "from" addresses

### Static & Media Files
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Verify WhiteNoise configuration
- [ ] Configure media file storage (consider AWS S3/Cloudinary)
- [ ] Test static file serving

### Environment Variables
- [ ] All required variables set in production
- [ ] No hardcoded secrets in code
- [ ] `.env` file not in version control
- [ ] Document all required environment variables

## Deployment

### Code Preparation
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Dependencies up to date in `requirements.txt`
- [ ] No merge conflicts
- [ ] Latest code pushed to repository

### Platform Setup
- [ ] Platform account created (Heroku/Railway/Render/etc.)
- [ ] Database addon/service created
- [ ] Domain configured (if applicable)
- [ ] SSL/HTTPS configured

### Deploy Steps
- [ ] Deploy application
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Load initial data (if applicable)

## Post-Deployment

### Verification
- [ ] Application accessible via URL
- [ ] Can log in to admin panel
- [ ] Static files loading correctly
- [ ] Media uploads working
- [ ] Email sending works
- [ ] Database operations work
- [ ] All main features functional

### Monitoring
- [ ] Set up error logging (Sentry recommended)
- [ ] Configure monitoring (uptime, performance)
- [ ] Set up SSL certificate monitoring
- [ ] Enable backup monitoring
- [ ] Configure alerting

### Performance
- [ ] Run performance tests
- [ ] Check page load times
- [ ] Optimize database queries
- [ ] Enable caching if needed
- [ ] Configure CDN for static files (optional)

### Documentation
- [ ] Update README with production URL
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document environment variables
- [ ] Update API documentation

## Security Audit

### Run Security Checks
```bash
python manage.py check --deploy
```

### Expected Results
All security warnings should be addressed:
- [ ] No DEBUG in production warning
- [ ] No SECRET_KEY warning
- [ ] No ALLOWED_HOSTS warning
- [ ] SSL/HTTPS properly configured
- [ ] Secure cookies enabled
- [ ] HSTS enabled

### Additional Security
- [ ] Configure CORS if using API
- [ ] Set up rate limiting
- [ ] Configure firewall rules
- [ ] Regular security updates scheduled
- [ ] Penetration testing completed (for production)

## Maintenance

### Regular Tasks
- [ ] Schedule database backups (daily recommended)
- [ ] Plan for dependency updates
- [ ] Monitor error logs
- [ ] Review security advisories
- [ ] Performance monitoring

### Emergency Contacts
- [ ] Document who to contact for issues
- [ ] Set up on-call rotation (if applicable)
- [ ] Create emergency rollback procedure

## Platform-Specific Notes

### Heroku
- [ ] Use at least "Basic" dyno for production
- [ ] Configure Heroku Postgres addon
- [ ] Set up Heroku Scheduler for periodic tasks
- [ ] Review Heroku logs: `heroku logs --tail`

### Railway
- [ ] Configure health check endpoint
- [ ] Set up custom domain
- [ ] Enable auto-deploy (optional)
- [ ] Review build and deploy logs

### Render
- [ ] Configure web service
- [ ] Set up PostgreSQL database
- [ ] Configure environment groups
- [ ] Set up auto-deploy from GitHub

### PythonAnywhere
- [ ] Configure WSGI file correctly
- [ ] Set static file mappings
- [ ] Configure scheduled tasks (if needed)
- [ ] Review error log location

### AWS/VPS
- [ ] Configure security groups/firewall
- [ ] Set up load balancer (if needed)
- [ ] Configure auto-scaling (optional)
- [ ] Set up CloudWatch/monitoring
- [ ] Configure backup scripts

## Troubleshooting

### If deployment fails:
1. Check build logs for errors
2. Verify all environment variables are set
3. Ensure database is accessible
4. Check Python version compatibility
5. Verify all dependencies install correctly

### If site is slow:
1. Check database query performance
2. Enable query logging temporarily
3. Consider adding caching
4. Optimize static file delivery
5. Check server resources

### If emails don't send:
1. Verify SMTP credentials
2. Check EMAIL_BACKEND setting
3. Test with console backend first
4. Verify firewall allows SMTP
5. Check for rate limiting

## Final Verification

Run this command to check everything:
```bash
python manage.py check --deploy
```

✅ **All checks passed? You're ready to go live!** 🎉

---

**Date Deployed:** _________________  
**Deployed By:** _________________  
**Platform:** _________________  
**Production URL:** _________________
