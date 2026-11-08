# 🚀 Quick Start Guide

## Running the Website

### Windows
```bash
run.bat
```

### Mac/Linux
```bash
bash run.sh
```

### Manual
```bash
cd config
python manage.py runserver
```

## Access

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Username**: admin
- **Password**: admin123

## ⚠️ First Time Setup Complete!

Your website is now running with:

✅ 6 sample services  
✅ 3 sample testimonials  
✅ 6 FAQ entries  
✅ Working booking system  
✅ Working quote request system  
✅ Working contact form  
✅ Admin dashboard  
✅ Professional design  

## Next Steps

1. **Change Admin Password**
   - Go to http://localhost:8000/admin/auth/user/
   - Click on "admin"
   - Change password immediately

2. **Update Business Information**
   - Edit `.env` file with your details
   - Restart the server

3. **Add Your Services**
   - Go to Admin Panel → Services
   - Edit or add services
   - Upload your images

4. **Customize Content**
   - Edit testimonials
   - Update FAQs
   - Customize pages

## Database

SQLite database is at: `config/db.sqlite3`

To backup:
```bash
cd config
python manage.py dumpdata > backup.json
```

## Common Commands

From the `config/` directory:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword admin

# Backup data
python manage.py dumpdata > backup.json

# Restore data
python manage.py loaddata backup.json
```

## Documentation

- `README.md` - Project overview
- `SETUP_GUIDE.md` - Detailed setup
- `ARCHITECTURE.md` - System design
- `COMMANDS.md` - All Django commands
- `COMPLETION_SUMMARY.md` - Full feature list

## Troubleshooting

**Issue**: Server won't start  
**Solution**: Make sure you're in the `config/` directory when running commands

**Issue**: Templates not found  
**Solution**: Restart the server - it caches template paths

**Issue**: Static files missing  
**Solution**: Run from root, not config directory for admin panel

**Issue**: Admin panel broken  
**Solution**: Run migrations: `python manage.py migrate`

---

**Enjoy your new professional cleaning services website!** 🎉

Visit http://localhost:8000 now!
