# Shree Nebula English School Website

A complete, modern, production-ready school website and CMS built with Flask + PostgreSQL.

**School:** Shree Nebula English School  
**Tagline:** Inspiring Minds. Building Futures.  
**Location:** Nepal  
**Developer:** Nebula School Team

---

## Features

### Public Website
- Premium responsive homepage with hero, statistics, about, programs, facilities
- Academic programs, admissions form, gallery with lightbox
- News, events, notices with detail pages
- Contact form, testimonials carousel
- SEO (meta tags, sitemap.xml, robots.txt, Schema.org)
- Mobile-first responsive design

### Admin CMS (`/admin`)
- Secure login with password hashing
- Dashboard with key statistics
- Full CRUD for: Notices, News, Events, Gallery, Facilities, Teachers, Testimonials
- Admission applications management (status workflow)
- Contact messages inbox
- Site settings (editable without code changes)
- Image upload with security

---

## Technology Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | HTML5, CSS3, Vanilla JS, Jinja2     |
| Backend  | Python 3, Flask                     |
| Database | PostgreSQL (SQLite for local demo)  |
| ORM      | Flask-SQLAlchemy + Flask-Migrate    |
| Forms    | Flask-WTF + WTForms                 |
| Auth     | Werkzeug password hashing           |
| Server   | Gunicorn (production)               |

**No React, Vue, Angular, Tailwind, or Bootstrap.**

---

## Installation

### 1. Clone / Extract

```bash
cd school-website
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-long-random-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/school_db
MAX_CONTENT_LENGTH=5242880
FLASK_ENV=development
FLASK_APP=app.py
```

> For local testing without PostgreSQL, leave `DATABASE_URL` unset — the app falls back to SQLite (`school.db`).

### 5. Create Database (PostgreSQL)

```sql
CREATE DATABASE school_db;
```

### 6. Run Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

Or simply start the app once — tables are created via models if using SQLite for demo.

### 7. Create Admin User

```bash
python create_admin.py
```

Follow the prompts for name, email, and password.

### 8. (Optional) Seed Sample Data

```bash
python seed_data.py
```

### 9. Run the Application

```bash
python app.py
```

Or:

```bash
flask run
```

Open: **http://localhost:5000**

Admin panel: **http://localhost:5000/admin/login**

---

## Production Deployment

```bash
# Set production environment variables
export FLASK_ENV=production
export SECRET_KEY=strong-random-key
export DATABASE_URL=postgresql://user:pass@host:5432/school_db

# Run with Gunicorn
gunicorn app:app -b 0.0.0.0:8000 -w 4
```

- Never use Flask debug mode in production
- Use HTTPS and secure session cookies
- Serve static files via Nginx/CDN
- Set proper `MAX_CONTENT_LENGTH` and file upload limits

---

## Project Structure

```
school-website/
├── app.py                 # Application factory
├── config.py              # Configuration
├── create_admin.py        # Admin creation CLI
├── seed_data.py           # Sample data seeder
├── requirements.txt
├── .env.example
├── models/                # SQLAlchemy models
├── routes/                # Blueprints (public, auth, admin)
├── forms/                 # WTForms
├── templates/
│   ├── public/            # Public pages
│   └── admin/             # Admin CMS
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
└── utils/                 # Helpers
```

---

## Color Palette

| Color        | Hex       | Usage                |
|--------------|-----------|----------------------|
| Deep Navy    | `#0B1F3A` | Primary brand        |
| Royal Blue   | `#2563EB` | Links, accents       |
| Golden Yellow| `#F4B400` | Buttons, highlights  |
| Light BG     | `#F5F7FA` | Section backgrounds  |
| Dark Text    | `#172033` | Body text            |
| Muted Text   | `#667085` | Secondary text       |

---

## License

Designed & Developed by **Nebula School Team**.  
© 2026 Shree Nebula English School. All Rights Reserved.


## Production: Vercel + PostgreSQL + Cloudinary

### 1. PostgreSQL (Neon / Supabase / Railway)

Create a free Postgres database and copy the connection string:

```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

### 2. Cloudinary (images)

1. Sign up at https://cloudinary.com
2. Dashboard → copy **Cloud name**, **API Key**, **API Secret**
3. Set env vars:

```
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

When these are set, uploaded images go to Cloudinary automatically.

### 3. Vercel

```bash
npm i -g vercel
vercel
```

Set environment variables in Vercel project settings:

- `SECRET_KEY`
- `DATABASE_URL`
- `CLOUDINARY_CLOUD_NAME` / `CLOUDINARY_API_KEY` / `CLOUDINARY_API_SECRET`
- `FLASK_ENV=production`

### 4. Google Maps embed

Admin → **Site Settings** → **Google Maps Embed**:

1. Open [Google Maps](https://maps.google.com)
2. Search: **Urlabari-8, Rajghat, Morang, Nepal**
3. **Share** → **Embed a map** → copy the `<iframe ...>` HTML
4. Paste into Site Settings and Save

The map appears on the Contact page.
